"""Assembly vidéo Shorts 9:16 — FFmpeg (assemblage) ou manifest JSON (fallback).

IMPORTANT : VideoBuilder est un outil d'ASSEMBLAGE, pas de génération de mouvement.
Il concatène des clips existants. Il ne génère pas de clips IA.
Voir docs/AI_VIDEO_ENGINE_KNOWLEDGE/VIDEO_ENGINE_ARCHITECTURE.md — Règle 0.

Tout appel à build() assigne STATUS=PROTOTYPE_TECHNIQUE.
TEASER_VALIDE ne peut être assigné que par QualityGate.record_human_verdict().
"""

import logging
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

from app.production_statuses import ProductionStatus, assert_not_forbidden
from app.utils import ensure_dir, get_logger, save_json

logger = get_logger(__name__)

_PLACEHOLDER_PATTERNS = frozenset({
    "scene_hook", "scene_story", "scene_climax", "scene_resolution",
    "episode_test", "placeholder", "test_image", "demo_",
})

RESOLUTION = (1080, 1920)


@dataclass
class VideoManifest:
    episode_id: str
    title: str
    image_paths: List[Path]
    audio_path: Path
    subtitles_path: Path
    output_path: Path
    duration: float = 35.0
    resolution: Tuple[int, int] = field(default_factory=lambda: RESOLUTION)
    transition_duration: float = 0.5
    background_music_path: Optional[Path] = None
    music_volume: float = 0.15


class VideoBuilder:
    """Assembly vidéo — FFmpeg si disponible, sinon manifest JSON."""

    def __init__(self):
        self._ffmpeg = shutil.which("ffmpeg")
        if self._ffmpeg:
            logger.info("FFmpeg trouvé: %s", self._ffmpeg)
        else:
            logger.info("FFmpeg absent — mode manifest JSON")

    # ── API publique ───────────────────────────────────────────────────────────

    def build(
        self,
        story_id: str,
        image_paths: List[Path],
        audio_path: Optional[Path],
        subtitles_path: Optional[Path],
        output_dir: Path,
    ) -> Path:
        output_dir = ensure_dir(output_dir)

        # Avertissement explicite : VideoBuilder produit toujours un prototype
        logger.warning(
            "VideoBuilder.build() — résultat = %s. "
            "Pour le teaser, utiliser Kling (voir IMAGE_TO_VIDEO_ENGINE_RULES.md).",
            ProductionStatus.PROTOTYPE_TECHNIQUE.value,
        )

        if self._ffmpeg and audio_path and audio_path.suffix == ".mp3" and image_paths:
            real_images = [
                p for p in image_paths
                if p.exists() and p.suffix in (".png", ".jpg", ".jpeg")
                and not _is_placeholder(p)
            ]
            if real_images:
                return self._build_ffmpeg(story_id, real_images, audio_path, subtitles_path, output_dir)

        return self._build_manifest(story_id, image_paths, audio_path, subtitles_path, output_dir)

    def build_from_manifest(self, manifest: VideoManifest) -> Path:
        return self.build(
            story_id=manifest.episode_id,
            image_paths=manifest.image_paths,
            audio_path=manifest.audio_path,
            subtitles_path=manifest.subtitles_path,
            output_dir=manifest.output_path.parent,
        )

    # ── FFmpeg ─────────────────────────────────────────────────────────────────

    def _build_ffmpeg(
        self,
        story_id: str,
        images: List[Path],
        audio: Path,
        subs: Optional[Path],
        output_dir: Path,
    ) -> Path:
        out = output_dir / f"luna_{story_id}.mp4"
        n = len(images)
        seg = 35.0 / n

        cmd = [self._ffmpeg, "-y"]
        for img in images:
            cmd += ["-loop", "1", "-t", str(seg), "-i", str(img)]
        cmd += ["-i", str(audio)]

        # filter_complex : scale + xfade entre chaque image
        w, h = RESOLUTION
        filters = []
        for i in range(n):
            filters.append(
                f"[{i}:v]scale={w}:{h}:force_original_aspect_ratio=1,"
                f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p[v{i}]"
            )

        prev = "v0"
        for i in range(1, n):
            offset = seg * i - 0.5
            last = i == n - 1
            nxt = "prevout" if not last else "outv"
            if n == 1:
                filters[0] = filters[0].replace(f"[v0]", "[outv]")
            else:
                filters.append(
                    f"[{prev}][v{i}]xfade=transition=fade:duration=0.5:offset={offset:.2f}[{nxt}]"
                )
            prev = nxt

        # Les sous-titres sont intégrés dans filter_complex pour éviter le conflit -vf/-filter_complex
        if subs and subs.exists():
            subs_escaped = str(subs).replace(":", "\\:")
            filters.append(
                f"[outv]subtitles={subs_escaped}:force_style="
                f"'FontName=Arial,FontSize=24,Bold=1,PrimaryColour=&H00FFFFFF,"
                f"OutlineColour=&H00000000,Outline=3,MarginV=60'[finalv]"
            )
            video_out = "[finalv]"
        else:
            video_out = "[outv]"

        filter_str = ";".join(filters)

        cmd += [
            "-filter_complex", filter_str,
            "-map", video_out,
            "-map", f"{n}:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-shortest", "-movflags", "+faststart",
            str(out),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("FFmpeg error: %s", result.stderr[-500:])
            return self._build_manifest(story_id, images, audio, subs, output_dir)

        logger.info("Vidéo assemblée: %s", out.name)
        return out

    # ── Manifest JSON (fallback) ───────────────────────────────────────────────

    def _build_manifest(
        self,
        story_id: str,
        images: List[Path],
        audio: Optional[Path],
        subs: Optional[Path],
        output_dir: Path,
    ) -> Path:
        out = output_dir / f"luna_{story_id}_manifest.json"
        save_json(
            {
                "story_id": story_id,
                "status": ProductionStatus.PROTOTYPE_TECHNIQUE.value,
                "resolution": list(RESOLUTION),
                "format": "9:16 Shorts",
                "images": [str(p) for p in images],
                "audio": str(audio) if audio else None,
                "subtitles": str(subs) if subs else None,
                "quality_gate_required": True,
                "human_validation_required": True,
                "note": (
                    "Ce manifest est un prototype. "
                    "Pour le teaser final, générer les clips avec Kling "
                    "puis exécuter QualityGate. "
                    "Voir docs/AI_VIDEO_ENGINE_KNOWLEDGE/VIDEO_ENGINE_ARCHITECTURE.md."
                ),
            },
            out,
        )
        logger.info("Manifest prototype créé: %s (status=%s)", out.name, ProductionStatus.PROTOTYPE_TECHNIQUE.value)
        return out


def _is_placeholder(path: Path) -> bool:
    name = path.stem.lower()
    for pattern in _PLACEHOLDER_PATTERNS:
        if pattern in name:
            logger.warning("Image placeholder ignorée : %s", path.name)
            return True
    return False
