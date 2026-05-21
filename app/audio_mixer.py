"""Mixage audio — voix + musique de fond + ambiance YAWatch."""

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from app.utils import ensure_dir, get_logger

logger = get_logger(__name__)

AMBIANCE_DIR = Path(__file__).resolve().parent.parent / "assets" / "ambiance"


class AudioMixer:
    """Mixe la voix TTS avec une couche musicale et/ou d'ambiance."""

    AMBIANCE_FILES = {
        "yawatch_control_room": "control_room_ambience.mp3",
        "lonely_room": "lonely_room_ambience.mp3",
        "alarm_phase": "alarm_phase.mp3",
    }

    def __init__(self):
        self._ffmpeg = shutil.which("ffmpeg")
        if not self._ffmpeg:
            logger.warning("FFmpeg absent — AudioMixer en mode copie simple")

    def mix(
        self,
        voice_path: Path,
        output_path: Path,
        background_music: Optional[Path] = None,
        music_volume: float = 0.15,
        ambiance_type: Optional[str] = None,
        ambiance_volume: float = 0.12,
    ) -> Path:
        """Mixe voix + musique de fond optionnelle."""
        ensure_dir(output_path.parent)

        if not self._ffmpeg:
            shutil.copy(voice_path, output_path)
            return output_path

        bg = background_music or self._default_music()

        if bg and bg.exists():
            inputs = ["-i", str(voice_path), "-i", str(bg)]
            filter_str = (
                f"[0:a]volume=1.0[a0];"
                f"[1:a]volume={music_volume}[a1];"
                f"[a0][a1]amix=inputs=2:duration=first:dropout_transition=2[out]"
            )
            cmd = [
                self._ffmpeg, "-y",
                *inputs,
                "-filter_complex", filter_str,
                "-map", "[out]",
                "-c:a", "aac", "-b:a", "128k",
                str(output_path),
            ]
        else:
            # Pas de musique : simple normalisation
            cmd = [
                self._ffmpeg, "-y",
                "-i", str(voice_path),
                "-af", "loudnorm=I=-14:TP=-1:LRA=11",
                "-c:a", "aac", "-b:a", "128k",
                str(output_path),
            ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("FFmpeg mix error: %s", result.stderr[-300:])
            shutil.copy(voice_path, output_path)
        else:
            logger.info("Audio mixé: %s", output_path.name)

        return output_path

    def add_ambiance(
        self,
        audio_path: Path,
        ambiance_type: str = "yawatch_control_room",
        volume: float = 0.12,
    ) -> Path:
        """Ajoute une couche d'ambiance (sons de salle de contrôle, etc.)."""
        ambiance_file = AMBIANCE_DIR / self.AMBIANCE_FILES.get(ambiance_type, "")
        if not ambiance_file.exists():
            logger.debug("Fichier ambiance absent: %s — ignoré", ambiance_file)
            return audio_path

        out = audio_path.parent / f"{audio_path.stem}_ambient{audio_path.suffix}"
        cmd = [
            self._ffmpeg, "-y",
            "-i", str(audio_path), "-i", str(ambiance_file),
            "-filter_complex",
            f"[0:a]volume=0.9[a0];[1:a]volume={volume}[a1];[a0][a1]amix=inputs=2:duration=first",
            "-c:a", "aac", str(out),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.warning("Ambiance mix failed: %s", result.stderr[-200:])
            return audio_path
        logger.info("Ambiance ajoutée: %s", out.name)
        return out

    def _default_music(self) -> Optional[Path]:
        candidate = AMBIANCE_DIR / "yawatch_ambient.mp3"
        return candidate if candidate.exists() else None
