"""Génération de sous-titres SRT depuis un script Luna."""

import logging
from pathlib import Path

from app.utils import save_text

logger = logging.getLogger(__name__)

WORDS_PER_SECOND = 2.3  # débit naturel légèrement lent (mystérieux)


def _format_srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


class SubtitleGenerator:
    def generate(self, script: str, story_id: str, output_dir: Path) -> Path:
        lines = [
            ln.strip()
            for ln in script.split("\n")
            if ln.strip() and not ln.startswith("[") and ":" not in ln[:10]
        ]

        blocks = []
        current_time = 0.0
        for i, line in enumerate(lines, 1):
            word_count = len(line.split())
            duration = max(1.5, word_count / WORDS_PER_SECOND)
            start = current_time
            end = current_time + duration
            blocks.append(
                f"{i}\n"
                f"{_format_srt_time(start)} --> {_format_srt_time(end)}\n"
                f"{line}\n"
            )
            current_time = end + 0.3  # pause entre phrases

        srt_content = "\n".join(blocks)
        filepath = output_dir / f"subs_{story_id}.srt"
        save_text(srt_content, filepath)
        logger.info("Sous-titres générés: %s (%d blocs)", filepath.name, len(blocks))
        return filepath
