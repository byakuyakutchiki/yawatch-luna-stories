"""Découpage d'un script en scènes avec timings précis."""

import re
import logging
from pathlib import Path
from typing import Dict, List

from app.utils import get_logger, save_json

logger = get_logger(__name__)

WORDS_PER_SECOND = 2.3
SECTION_NAMES = ["HOOK", "STORY", "TWIST", "CTA"]


class SceneComposer:
    def __init__(self, total_duration: float = 35.0):
        self.total_duration = total_duration

    def parse_script(self, script: str) -> Dict[str, str]:
        """Extrait HOOK/STORY/TWIST/CTA — gère 'HOOK:' et 'HOOK' indifféremment."""
        sections: Dict[str, str] = {}
        current: str = None
        buf: List[str] = []

        for raw_line in script.split("\n"):
            line = raw_line.strip()
            if not line:
                continue

            # Ignorer les méta-headers [Épisode N — ...]
            if line.startswith("[") and line.endswith("]"):
                continue

            # Détection section : "HOOK:" ou "HOOK"
            candidate = line.rstrip(":").upper()
            if candidate in SECTION_NAMES:
                if current:
                    sections[current] = "\n".join(buf).strip()
                current = candidate
                buf = []
            else:
                if current:
                    buf.append(line)

        if current:
            sections[current] = "\n".join(buf).strip()

        for s in SECTION_NAMES:
            if s not in sections:
                logger.warning("Section manquante dans le script: %s", s)
                sections[s] = ""

        return sections

    def build_timings(self, sections: Dict[str, str]) -> List[Dict]:
        """Calcule le timing de chaque scène proportionnellement au nombre de mots."""
        word_counts = {s: len(sections[s].split()) for s in SECTION_NAMES}
        total_words = sum(word_counts.values()) or 1

        scenes = []
        current_time = 0.0
        for s in SECTION_NAMES:
            duration = self.total_duration * word_counts[s] / total_words
            duration = max(3.0, duration)  # minimum 3s par scène
            scenes.append({
                "type": s,
                "text": sections[s],
                "start": round(current_time, 2),
                "end": round(current_time + duration, 2),
                "duration": round(duration, 2),
            })
            current_time += duration

        return scenes

    def build_overlays(self, scenes: List[Dict]) -> List[Dict]:
        """Génère les blocs de sous-titres depuis les scènes."""
        overlays = []
        for scene in scenes:
            sentences = self._split_sentences(scene["text"])
            if not sentences:
                continue
            seg_dur = scene["duration"] / len(sentences)
            t = scene["start"]
            for sent in sentences:
                overlays.append({
                    "text": sent,
                    "start": round(t, 2),
                    "end": round(t + seg_dur, 2),
                    "scene_type": scene["type"],
                })
                t += seg_dur
        return overlays

    def compose(self, script: str) -> Dict:
        sections = self.parse_script(script)
        scenes = self.build_timings(sections)
        overlays = self.build_overlays(scenes)
        return {
            "sections": sections,
            "scenes": scenes,
            "overlays": overlays,
            "total_duration": self.total_duration,
        }

    def save(self, composition: Dict, output_dir: Path, episode_id: str) -> Path:
        path = output_dir / f"composition_{episode_id}.json"
        save_json(composition, path)
        return path

    def _split_sentences(self, text: str) -> List[str]:
        parts = re.split(r"[.!?;:]+", text)
        result = []
        for part in parts:
            part = part.strip()
            if not part:
                continue
            words = part.split()
            if len(words) > 10:
                for i in range(0, len(words), 8):
                    chunk = " ".join(words[i : i + 8])
                    result.append(chunk)
            else:
                result.append(part)
        return result or [text]
