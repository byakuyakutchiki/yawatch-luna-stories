"""Packaging des épisodes pour export YouTube.

Règle absolue : aucun package ne peut avoir STATUS=TEASER_VALIDE sans appel
explicite à mark_human_approved(). Les strings "ready", "approved", "done"
sont interdites — utiliser ProductionStatus uniquement.
"""

import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from app.production_statuses import ProductionStatus, assert_not_forbidden
from app.utils import ensure_dir, get_logger, save_json

logger = get_logger(__name__)

EXPORT_ROOT = Path(__file__).resolve().parent.parent / "outputs" / "exports"

YOUTUBE_TAGS = [
    "YAWatch", "Luna", "LunaDoll", "IA", "surveillance",
    "thriller", "histoire courte", "shorts", "science fiction",
]

DESCRIPTION_TEMPLATE = """🧸 YAWatch Luna Stories — Épisode {episode_number}

{title}

Luna a fondé YAWatch Industries pour protéger les gens.
Mais son IA évolue.
Et la petite poupée violette sur son bureau n'est pas un simple jouet.

🔔 Abonne-toi pour la suite.
#YAWatch #Luna #IA #Surveillance #Shorts #HistoireIA
"""


class ExportManager:
    def __init__(self):
        ensure_dir(EXPORT_ROOT)

    def create_package(
        self,
        episode_id: str,
        story: Dict,
        video_path: Optional[Path] = None,
        thumbnail_path: Optional[Path] = None,
        script_path: Optional[Path] = None,
        subtitles_path: Optional[Path] = None,
    ) -> Path:
        """Crée un dossier d'export complet pour un épisode."""
        export_dir = ensure_dir(EXPORT_ROOT / episode_id)

        # Copie des fichiers disponibles
        def _copy(src: Optional[Path], dest_name: str) -> Optional[str]:
            if src and src.exists():
                dest = export_dir / dest_name
                shutil.copy(src, dest)
                return str(dest)
            return None

        video_dest = _copy(video_path, f"luna_{episode_id}.mp4")
        thumb_dest = _copy(thumbnail_path, "thumbnail.jpg")
        script_dest = _copy(script_path, "script.txt")
        subs_dest = _copy(subtitles_path, "subtitles.srt")

        # Metadata YouTube
        # create_package() assigne TOUJOURS PROTOTYPE_TECHNIQUE.
        # TEASER_CANDIDAT ne peut être assigné qu'après QualityGate.run() via advance_to_candidat().
        # TEASER_VALIDE ne peut être assigné qu'après mark_human_approved() par Ludovic.
        metadata = {
            "episode_id": episode_id,
            "export_date": datetime.now().isoformat(),
            "status": ProductionStatus.PROTOTYPE_TECHNIQUE.value,
            "human_validation_required": True,
            "human_approved": False,
            "human_approved_by": None,
            "quality_gate_passed": False,
            "note": (
                "Statut initial : prototype_technique. "
                "Étape suivante : appeler advance_to_candidat(gate_report) "
                "après QualityGate.run(). "
                "Puis mark_human_approved() après visionnage Ludovic."
            ),
            "files": {
                "video": video_dest,
                "thumbnail": thumb_dest,
                "script": script_dest,
                "subtitles": subs_dest,
            },
            "youtube": {
                "title": story.get("title", f"YAWatch Luna — Épisode {story.get('episode_number', '?')}"),
                "description": DESCRIPTION_TEMPLATE.format(
                    episode_number=story.get("episode_number", "?"),
                    title=story.get("title", ""),
                ),
                "tags": YOUTUBE_TAGS,
                "category": "28",  # Science & Technology
                "made_for_kids": False,
                "privacy": "private",  # Upload privé par défaut
            },
        }

        save_json(metadata, export_dir / "metadata.json")
        logger.info("Package créé: %s (status: %s)", export_dir.name, metadata["status"])
        return export_dir

    def advance_to_candidat(self, episode_id: str, gate_report) -> None:
        """Fait passer un package de PROTOTYPE_TECHNIQUE à TEASER_CANDIDAT.

        Requiert que gate_report.can_advance_to_candidat soit True,
        c'est-à-dire que les 5 verdicts automatiques aient passé.
        """
        if not gate_report.can_advance_to_candidat:
            failing = [
                v.verdict_name for v in gate_report.all_verdicts
                if v.status == "FAIL" and v.verdict_name != "verdict_storytelling"
            ]
            raise ValueError(
                f"QualityGate non passé — impossible d'avancer à TEASER_CANDIDAT. "
                f"Verdicts en échec : {failing}"
            )
        export_dir = EXPORT_ROOT / episode_id
        meta_path = export_dir / "metadata.json"
        if not meta_path.exists():
            raise FileNotFoundError(f"Package introuvable : {episode_id}")

        from app.utils import load_json
        metadata = load_json(meta_path) or {}
        metadata["status"] = ProductionStatus.TEASER_CANDIDAT.value
        metadata["quality_gate_passed"] = True
        metadata["quality_gate_date"] = datetime.now().isoformat()
        metadata["quality_gate_report"] = gate_report.to_dict()
        save_json(metadata, meta_path)
        logger.info("Package %s → %s", episode_id, ProductionStatus.TEASER_CANDIDAT.value)

    def mark_human_approved(self, episode_id: str, approved_by: str, notes: str = "") -> None:
        """Seule voie vers TEASER_VALIDE — doit être appelée par un humain identifié.

        Requiert que le package soit en TEASER_CANDIDAT (quality gate passé).
        """
        if not approved_by or approved_by.strip().lower() in ("claude", "codex", "agent", "ai", "bot"):
            raise ValueError(
                f"approved_by='{approved_by}' n'est pas un nom humain valide. "
                "Seul Ludovic peut approuver un package pour publication."
            )
        export_dir = EXPORT_ROOT / episode_id
        meta_path = export_dir / "metadata.json"
        if not meta_path.exists():
            raise FileNotFoundError(f"Package introuvable : {episode_id}")

        from app.utils import load_json
        metadata = load_json(meta_path) or {}

        current_status = metadata.get("status", "")
        if current_status != ProductionStatus.TEASER_CANDIDAT.value:
            raise ValueError(
                f"Le package '{episode_id}' est en statut '{current_status}'. "
                f"Il doit être en '{ProductionStatus.TEASER_CANDIDAT.value}' "
                "avant d'être approuvé. "
                "Appeler advance_to_candidat() après QualityGate.run()."
            )

        metadata["status"] = ProductionStatus.TEASER_VALIDE.value
        metadata["human_approved"] = True
        metadata["human_approved_by"] = approved_by.strip()
        metadata["human_approved_date"] = datetime.now().isoformat()
        metadata["human_approved_notes"] = notes
        save_json(metadata, meta_path)
        logger.info(
            "Package %s approuvé par %s → %s",
            episode_id, approved_by, ProductionStatus.TEASER_VALIDE.value
        )

    def list_packages(self, status_filter: Optional[str] = None) -> List[Path]:
        packages = [
            d for d in EXPORT_ROOT.iterdir()
            if d.is_dir() and (d / "metadata.json").exists()
        ]
        if status_filter:
            from app.utils import load_json
            packages = [
                p for p in packages
                if (load_json(p / "metadata.json") or {}).get("status") == status_filter
            ]
        return sorted(packages)

    def summary(self) -> str:
        packages = self.list_packages()
        if not packages:
            return "Aucun export disponible."
        lines = [f"📦 {len(packages)} exports :"]
        for p in packages[-5:]:  # 5 derniers
            from app.utils import load_json
            meta = load_json(p / "metadata.json") or {}
            lines.append(f"  [{meta.get('status','?')}] {meta.get('youtube',{}).get('title','?')}")
        return "\n".join(lines)
