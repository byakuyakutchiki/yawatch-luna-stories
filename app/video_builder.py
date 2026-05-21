"""Assembly vidéo Shorts 9:16 — FFmpeg (prod) ou manifest JSON (fallback)."""

import logging
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

from app.utils import ensure_dir, get_logger, save_json

logger = get_logger(__name__)

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

        if self._ffmpeg and audio_path and audio_path.suffix == ".mp3" and image_paths:
            real_images = [p for p in image_paths if p.exists() and p.suffix in (".png", ".jpg", ".jpeg")]
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
            nxt = f"vx{i}" if i < n - 1 else "outv"
            filters.append(f"[{prev}][v{i}]xfade=transition=fade:duration=0.5:offset={offset:.2f}[{nxt}]")
            prev = nxt

        filter_str = ";".join(filters)

        sub_filter = ""
        if subs and subs.exists():
            sub_filter = f",subtitles={subs}:force_style='FontName=Arial,FontSize=24,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=3,MarginV=60'"

        cmd += [
            "-filter_complex", filter_str,
            "-map", "[outv]",
            "-map", f"{n}:a",
            "-vf", f"scale={w}:{h}{sub_filter}",
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
                "status": "prototype",
                "resolution": list(RESOLUTION),
                "format": "9:16 Shorts",
                "images": [str(p) for p in images],
                "audio": str(audio) if audio else None,
                "subtitles": str(subs) if subs else None,
                "ffmpeg_hint": (
                    f"ffmpeg -loop 1 -t 35 -i image.jpg -i {audio} "
                    f"-vf subtitles={subs} -c:v libx264 -c:a aac luna_{story_id}.mp4"
                ),
            },
            out,
        )
        logger.info("Manifest vidéo créé: %s", out.name)
        return out
