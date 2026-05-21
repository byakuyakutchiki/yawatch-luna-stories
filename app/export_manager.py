"""Packaging des épisodes pour export YouTube."""

import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

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
        metadata = {
            "episode_id": episode_id,
            "export_date": datetime.now().isoformat(),
            "status": "ready_for_review" if video_dest else "script_only",
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
