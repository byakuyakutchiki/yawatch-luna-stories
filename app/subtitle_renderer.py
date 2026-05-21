"""Incrustation professionnelle des sous-titres dans la vidéo."""

import logging
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

from app.utils import get_logger

logger = get_logger(__name__)

STYLE = (
    "FontName=Arial,"
    "FontSize=26,"
    "Bold=1,"
    "PrimaryColour=&H00FFFFFF,"
    "OutlineColour=&H00000000,"
    "BackColour=&H80000000,"
    "BorderStyle=1,"
    "Outline=2,"
    "Alignment=2,"
    "MarginV=60"
)


class SubtitleRenderer:
    def __init__(self):
        self._ffmpeg = shutil.which("ffmpeg")

    def burn(self, video_path: Path, srt_path: Path, output_path: Path) -> Path:
        """Incruste les sous-titres SRT dans la vidéo."""
        if not self._ffmpeg:
            logger.warning("FFmpeg absent — sous-titres non incrustés")
            return video_path

        cmd = [
            self._ffmpeg, "-y",
            "-i", str(video_path),
            "-vf", f"subtitles={srt_path}:force_style='{STYLE}'",
            "-c:a", "copy",
            "-c:v", "libx264", "-crf", "23", "-preset", "fast",
            str(output_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("Burn subtitles failed: %s", result.stderr[-300:])
            return video_path
        logger.info("Sous-titres incrustés: %s", output_path.name)
        return output_path

    def create_ass(self, overlays: List[Dict], output_path: Path) -> Path:
        """Crée un fichier ASS (Advanced SubStation Alpha) pour contrôle fin."""
        content = [
            "[Script Info]",
            "ScriptType: v4.00+",
            "PlayResX: 1080",
            "PlayResY: 1920",
            "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Alignment, MarginV, Encoding",
            "Style: Default,Arial,26,&H00FFFFFF,&H00000000,&H80000000,1,1,2,2,60,1",
            "",
            "[Events]",
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        ]
        for ov in overlays:
            content.append(
                f"Dialogue: 0,{self._ass_time(ov['start'])},{self._ass_time(ov['end'])},"
                f"Default,,0,0,0,,{ov['text'].replace(chr(10), ' ').strip()}"
            )
        output_path.write_text("\n".join(content), encoding="utf-8")
        logger.info("Fichier ASS créé: %s", output_path.name)
        return output_path

    def _ass_time(self, seconds: float) -> str:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60
        cs = int((s % 1) * 100)
        return f"{h}:{m:02d}:{int(s):02d}.{cs:02d}"
