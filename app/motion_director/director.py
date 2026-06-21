"""MotionDirector — prépare les VideoJob à partir des bibliothèques.

────────────────────────────────────────────────────────────────────────────
RÔLE (principe de gouvernance de Ludovic)
────────────────────────────────────────────────────────────────────────────
Le MotionDirector est le PRÉPARATEUR manquant. Il transforme la connaissance
en job exécutable :

    bibliothèques → [MotionDirector] → VideoJob → backend ComfyUI → Quality Gate → humain

Ce qu'il FAIT :
  - vérifie que les bibliothèques requises sont présentes (sinon il refuse) ;
  - lit le registre des plans (TEASER_S01E00_PRODUCTION_PACK) ;
  - lit les profils de mouvement (MOTION_CONTROL_RULES) ;
  - choisit le profil selon le type de plan ;
  - assemble le prompt (positif + négatif anti-déformation/identité) ;
  - décide l'usage de l'IPAdapter selon le personnage ;
  - produit un VideoJob.

Ce qu'il NE FAIT PAS :
  - il ne génère aucune vidéo (c'est le backend) ;
  - il ne valide aucun clip (c'est le Quality Gate) ;
  - il n'assigne aucun statut (c'est ExportManager après validation humaine).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath

from app.i2v_engine.comfyui_backend import (
    VideoJob,
    compute_job_hash,
    GOVERNED_SOURCE,
    DEFAULT_LOCKED_PARAMETERS,
    SUPPORTED_ENGINES,
    ENGINE_ANIMATEDIFF,
)

# Racine du repo (…/app/motion_director/director.py → remonte de 2)
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_KNOWLEDGE_DIR = _REPO_ROOT / "docs" / "AI_VIDEO_ENGINE_KNOWLEDGE"

# Bibliothèques que le MotionDirector DOIT pouvoir consulter (cf. MOTION_CONTROL_RULES.md)
REQUIRED_LIBRARIES = [
    _REPO_ROOT / "docs" / "CHARACTER_BIBLE.md",
    _REPO_ROOT / "docs" / "VISUAL_DIRECTION.md",
    _REPO_ROOT / "docs" / "TEASER_S01E00_PRODUCTION_PACK.md",
    _KNOWLEDGE_DIR / "IMAGE_TO_VIDEO_ENGINE_RULES.md",
    _KNOWLEDGE_DIR / "MOTION_CONTROL_RULES.md",
]

_PROFILES_PATH = Path(__file__).resolve().parent / "motion_profiles.json"
_PLANS_PATH = Path(__file__).resolve().parent / "teaser_s01e00_plans.json"


class LibrariesNotAvailable(RuntimeError):
    """Levée si une bibliothèque requise est absente — on ne prépare rien sans la connaissance."""


@dataclass
class TargetPaths:
    """Où l'image sera mise à disposition et où le clip sera déposé (host d'exécution).

    `posix=True` pour un host Linux (pod RunPod) ; défaut Windows (pont local).
    """

    sources_dir: str   # dossier où les images canoniques sont mises à disposition
    deposit_dir: str   # dossier où le clip final est déposé
    posix: bool = False  # True = chemins Linux (pod), False = chemins Windows (pont)

    def staged_image(self, image_stem: str, suffix: str = ".png") -> str:
        flavor = PurePosixPath if self.posix else PureWindowsPath
        return str(flavor(self.sources_dir) / f"{image_stem}{suffix}")


class MotionDirector:
    """Prépare les VideoJob à partir des bibliothèques et des profils de mouvement."""

    def __init__(self, strict: bool = True):
        self._libraries_ok = self._check_libraries(strict=strict)
        self._profiles_data = json.loads(_PROFILES_PATH.read_text(encoding="utf-8"))
        self._profiles = self._profiles_data["profiles"]
        self._negative_base = self._profiles_data["negative_base"]
        self._plans_data = json.loads(_PLANS_PATH.read_text(encoding="utf-8"))
        self._plans = self._plans_data["plans"]

    # ── Gouvernance : la connaissance d'abord ──────────────────────────────

    @staticmethod
    def _check_libraries(strict: bool) -> bool:
        missing = [p.name for p in REQUIRED_LIBRARIES if not p.exists()]
        if missing and strict:
            raise LibrariesNotAvailable(
                f"Bibliothèques requises absentes : {missing}. "
                "Le MotionDirector ne prépare aucun job sans la connaissance."
            )
        return not missing

    @property
    def libraries_loaded(self) -> bool:
        return self._libraries_ok

    def available_plans(self) -> list[str]:
        return sorted(self._plans.keys())

    def profile_for_type(self, plan_type: str) -> dict:
        if plan_type not in self._profiles:
            raise KeyError(
                f"Type de plan inconnu : '{plan_type}'. "
                f"Types disponibles : {sorted(self._profiles)}"
            )
        return self._profiles[plan_type]

    # ── Préparation d'un VideoJob ──────────────────────────────────────────

    def prepare_job(
        self, plan_id: str, target: TargetPaths, engine: str = ENGINE_ANIMATEDIFF
    ) -> VideoJob:
        """Construit le VideoJob pour un plan. Ne génère ni ne valide rien.

        `engine` choisit le moteur I2V (animatediff prouvé par défaut ;
        framepack / wan21 pour la comparaison gouvernée). Le job est scellé
        (source + locked_parameters + job_hash) pour que le backend puisse
        refuser toute altération manuelle ultérieure.
        """
        if not self._libraries_ok:
            raise LibrariesNotAvailable(
                "Bibliothèques non chargées — préparation refusée."
            )
        if engine not in SUPPORTED_ENGINES:
            raise ValueError(
                f"Moteur inconnu : '{engine}'. Moteurs supportés : {SUPPORTED_ENGINES}."
            )
        if plan_id not in self._plans:
            raise KeyError(
                f"Plan inconnu : '{plan_id}'. Plans disponibles : {self.available_plans()}"
            )

        plan = self._plans[plan_id]
        plan_type = plan["plan_type"]
        profile = self.profile_for_type(plan_type)

        character = plan.get("character", "none")
        use_ipadapter = (profile["ipadapter_weight"] > 0.0) and (character != "none")

        image_path = target.staged_image(plan["image_stem"])

        # Paramètres spécifiques au moteur (FramePack / Wan), lus dans les
        # bibliothèques (profils). AnimateDiff n'en a pas besoin (champs dédiés).
        engine_params = dict(self._profiles_data.get("engines", {}).get(engine, {}))

        job = VideoJob(
            output_name=f"{plan_id}_{plan['image_stem'].replace('yawatch_' + plan_id + '_', '')}.mp4"
            if plan["image_stem"].startswith(f"yawatch_{plan_id}_")
            else f"{plan_id}_{plan['image_stem']}.mp4",
            deposit_dir=target.deposit_dir,
            image_path=image_path,
            prompt_positive=plan["prompt_positive"],
            prompt_negative=self._negative_base,
            # Moteur I2V
            engine=engine,
            engine_params=engine_params,
            # Valeurs pilotées par le profil (MOTION_CONTROL_RULES.md)
            num_frames=profile["num_frames"],
            fps=profile["fps"],
            steps=profile["steps"],
            cfg=profile["cfg"],
            denoise=profile["denoise"],
            # Identité personnage
            use_ipadapter=use_ipadapter,
            ipadapter_weight=profile["ipadapter_weight"],
            ipadapter_image=image_path if use_ipadapter else "",
            # Métadonnée de mouvement (appliquée par le backend si le nœud est dispo)
            motion_scale=profile["motion_scale"],
            # Traçabilité
            plan_id=plan_id,
            plan_type=plan_type,
            character=character,
        )

        # Sceau de gouvernance : le job est signé par le rôle métier. Toute
        # modification d'un paramètre verrouillé après ce point casse le hash
        # et fait refuser le job par le backend.
        job.source_generatrice = GOVERNED_SOURCE
        job.locked_parameters = tuple(DEFAULT_LOCKED_PARAMETERS)
        job.job_hash = compute_job_hash(job)
        return job

    def describe_plan(self, plan_id: str) -> str:
        """Résumé lisible de ce qui sera préparé pour un plan (gouvernance / debug)."""
        plan = self._plans[plan_id]
        profile = self.profile_for_type(plan["plan_type"])
        use_ip = (profile["ipadapter_weight"] > 0.0) and (plan.get("character") != "none")
        return (
            f"{plan_id} [{plan['plan_type']}] perso={plan.get('character')}\n"
            f"  mouvement   : {plan['movement']}\n"
            f"  denoise={profile['denoise']} cfg={profile['cfg']} steps={profile['steps']} "
            f"frames={profile['num_frames']}\n"
            f"  IPAdapter   : {'OUI poids=' + str(profile['ipadapter_weight']) if use_ip else 'non'}"
        )
