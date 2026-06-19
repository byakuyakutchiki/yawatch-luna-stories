"""Gardien obligatoire du pipeline vidéo YAWatch-LUNA.

Toute production vidéo DOIT passer par ProductionGatekeeper.require().
Si la base de connaissances n'est pas chargée, la production est bloquée.

Usage obligatoire en début de tout code vidéo :
    gatekeeper = ProductionGatekeeper.require()
    # ou, pour autoriser la dégradation gracieuse :
    gatekeeper = ProductionGatekeeper.load(strict=False)
"""

import logging
from pathlib import Path

from app.roles import (
    ALL_ROLES, BaseRole, VideoGenerationEngineer, MotionEngineer,
    MonteurCinema, SoundDesigner, VideoQAEngineer, TrailerDesigner,
)

logger = logging.getLogger(__name__)

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "docs" / "AI_VIDEO_ENGINE_KNOWLEDGE"

REQUIRED_KNOWLEDGE_DOCS = [
    "VIDEO_ENGINE_ARCHITECTURE.md",
    "FFMPEG_PROFESSIONAL_VIDEO_PIPELINE.md",
    "COMFYUI_WORKFLOWS_REFERENCE.md",
    "DIFFUSERS_VIDEO_MODELS_REFERENCE.md",
    "IMAGE_TO_VIDEO_ENGINE_RULES.md",
    "GRAPHICS_ENGINE_RULES.md",
    "QUALITY_GATE_ENGINE.md",
]


class KnowledgeBaseNotLoaded(RuntimeError):
    """Levée quand la base de connaissances technique est manquante ou incomplète."""


class ProductionGatekeeper:
    """Charge et vérifie la base de connaissances avant toute production vidéo."""

    def __init__(self) -> None:
        self._missing_docs: list[str] = []
        self._roles: dict[str, BaseRole] = {}
        self._loaded: bool = False

    # ── API publique ─────────────────────────────────────────────────────────

    @classmethod
    def require(cls) -> "ProductionGatekeeper":
        """Charge le gatekeeper. Lève KnowledgeBaseNotLoaded si incomplet."""
        gk = cls()
        gk._load()
        if gk._missing_docs:
            raise KnowledgeBaseNotLoaded(
                f"Base de connaissances incomplète — {len(gk._missing_docs)} "
                f"document(s) manquant(s) dans {KNOWLEDGE_DIR} :\n"
                + "\n".join(f"  ✗ {d}" for d in gk._missing_docs)
                + "\n\nLancer d'abord la création des documents de connaissance."
            )
        return gk

    @classmethod
    def load(cls, strict: bool = True) -> "ProductionGatekeeper":
        """Charge le gatekeeper. Si strict=False, loggue les warnings sans lever."""
        gk = cls()
        gk._load()
        if gk._missing_docs:
            msg = (
                f"[AVERTISSEMENT PRODUCTION] Base de connaissances incomplète — "
                f"{len(gk._missing_docs)} document(s) manquant(s) :\n"
                + "\n".join(f"  ✗ {d}" for d in gk._missing_docs)
            )
            if strict:
                raise KnowledgeBaseNotLoaded(msg)
            logger.warning(msg)
        return gk

    def get_role(self, role_name: str) -> BaseRole:
        """Retourne un rôle métier instancié."""
        role = self._roles.get(role_name)
        if role is None:
            available = ", ".join(self._roles.keys())
            raise KeyError(
                f"Rôle '{role_name}' inconnu. Disponibles : {available}"
            )
        return role

    @property
    def video_generation_engineer(self) -> VideoGenerationEngineer:
        return self._roles["VideoGenerationEngineer"]  # type: ignore

    @property
    def motion_engineer(self) -> MotionEngineer:
        return self._roles["MotionEngineer"]  # type: ignore

    @property
    def monteur_cinema(self) -> MonteurCinema:
        return self._roles["MonteurCinema"]  # type: ignore

    @property
    def sound_designer(self) -> SoundDesigner:
        return self._roles["SoundDesigner"]  # type: ignore

    @property
    def video_qa_engineer(self) -> VideoQAEngineer:
        return self._roles["VideoQAEngineer"]  # type: ignore

    @property
    def trailer_designer(self) -> TrailerDesigner:
        return self._roles["TrailerDesigner"]  # type: ignore

    def assert_not_placeholder(self, image_paths: list) -> None:
        """Lève ValueError si des images placeholder sont détectées."""
        from app.roles.video_generation_engineer import PLACEHOLDER_PATTERNS
        violations = []
        for p in image_paths:
            name = str(p).lower()
            for pattern in PLACEHOLDER_PATTERNS:
                if pattern in name:
                    violations.append(str(p))
                    break
        if violations:
            raise ValueError(
                f"Images placeholder interdites en production teaser :\n"
                + "\n".join(f"  ✗ {v}" for v in violations)
                + "\nUtiliser uniquement les assets de TEASER_S01E00_PRODUCTION_PACK.md."
            )

    def status_report(self) -> str:
        """Rapport de statut du gatekeeper."""
        lines = ["=== ProductionGatekeeper — Rapport de chargement ==="]
        if not self._missing_docs:
            lines.append(f"✓ Base de connaissances : {len(REQUIRED_KNOWLEDGE_DOCS)} documents présents")
        else:
            lines.append(
                f"✗ Base de connaissances : {len(self._missing_docs)} manquant(s) "
                f"sur {len(REQUIRED_KNOWLEDGE_DOCS)}"
            )
            for d in self._missing_docs:
                lines.append(f"    ✗ {d}")

        lines.append(f"✓ Rôles chargés : {len(self._roles)}")
        for name, role in self._roles.items():
            ok = "✓" if role.is_knowledge_loaded() else "✗"
            lines.append(f"    {ok} {name} [{role.knowledge_doc}]")
        return "\n".join(lines)

    # ── Interne ──────────────────────────────────────────────────────────────

    def _load(self) -> None:
        # Vérifier les documents de connaissance
        for doc in REQUIRED_KNOWLEDGE_DOCS:
            if not (KNOWLEDGE_DIR / doc).exists():
                self._missing_docs.append(doc)

        # Instancier tous les rôles
        for role_class in ALL_ROLES:
            role = role_class()
            self._roles[role.role_name] = role

        self._loaded = True
        if not self._missing_docs:
            logger.info(
                "ProductionGatekeeper chargé — %d rôles, %d docs de connaissance",
                len(self._roles), len(REQUIRED_KNOWLEDGE_DOCS)
            )
