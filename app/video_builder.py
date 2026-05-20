"""Assemblage vidéo Shorts 9:16 — MoviePy si disponible, sinon manifest JSON."""

import logging
from pathlib import Path
from typing import List, Optional

from app.utils import save_json

logger = logging.getLogger(__name__)

RESOLUTION = (1080, 1920)  # 9:16 Shorts


class VideoBuilder:
    def __init__(self):
        self._moviepy_available = self._check_moviepy()

    def _check_moviepy(self) -> bool:
        try:
            import moviepy  # noqa: F401
            return True
        except ImportError:
            logger.info("MoviePy non installé — génération manifest JSON uniquement")
            return False

    def build(
        self,
        story_id: str,
        image_paths: List[Path],
        audio_path: Optional[Path],
        subtitles_path: Optional[Path],
        output_dir: Path,
    ) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)

        if self._moviepy_available and audio_path and audio_path.suffix == ".mp3":
            return self._build_moviepy(story_id, image_paths, audio_path, subtitles_path, output_dir)
        return self._build_manifest(story_id, image_paths, audio_path, subtitles_path, output_dir)

    def _build_moviepy(
        self,
        story_id: str,
        image_paths: List[Path],
        audio_path: Path,
        subtitles_path: Optional[Path],
        output_dir: Path,
    ) -> Path:
        try:
            from moviepy import AudioFileClip, ImageClip, concatenate_videoclips

            clips = []
            duration_per_image = 8.0
            for img in image_paths:
                if img.exists() and img.suffix in (".png", ".jpg", ".jpeg"):
                    clip = ImageClip(str(img)).with_duration(duration_per_image)
                    clips.append(clip)

            if not clips:
                logger.warning("Aucune image réelle — fallback manifest")
                return self._build_manifest(story_id, image_paths, audio_path, subtitles_path, output_dir)

            video = concatenate_videoclips(clips, method="compose")
            audio = AudioFileClip(str(audio_path))
            video = video.with_audio(audio)

            out_path = output_dir / f"luna_{story_id}.mp4"
            video.write_videofile(
                str(out_path),
                fps=30,
                codec="libx264",
                audio_codec="aac",
                threads=2,
                logger=None,
            )
            logger.info("Vidéo assemblée: %s", out_path.name)
            return out_path
        except Exception as e:
            logger.error("Erreur MoviePy: %s — fallback manifest", e)
            return self._build_manifest(story_id, image_paths, audio_path, subtitles_path, output_dir)

    def _build_manifest(
        self,
        story_id: str,
        image_paths: List[Path],
        audio_path: Optional[Path],
        subtitles_path: Optional[Path],
        output_dir: Path,
    ) -> Path:
        manifest = {
            "story_id": story_id,
            "resolution": list(RESOLUTION),
            "format": "9:16 Shorts",
            "images": [str(p) for p in image_paths],
            "audio": str(audio_path) if audio_path else None,
            "subtitles": str(subtitles_path) if subtitles_path else None,
            "instruction": "Assembler manuellement ou via FFmpeg",
            "ffmpeg_hint": (
                f"ffmpeg -framerate 0.125 -pattern_type glob -i 'images/*.jpg' "
                f"-i {audio_path} -c:v libx264 -c:a aac -shortest luna_{story_id}.mp4"
            ),
        }
        out_path = output_dir / f"luna_{story_id}_manifest.json"
        save_json(manifest, out_path)
        logger.info("Manifest vidéo créé: %s", out_path.name)
        return out_path
