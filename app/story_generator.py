"""Génération d'histoires cohérentes avec l'univers YAWatch-Luna."""

import logging
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from app.lore_manager import LoreManager
from app.utils import save_json

logger = logging.getLogger(__name__)

STORY_TYPES = ["emotionnelle", "mysterieuse", "inquietante", "protection", "philosophique"]

_TITLES: Dict[str, List[str]] = {
    "emotionnelle": [
        "La photo que Luna refusait de regarder",
        "Tout a commencé bien avant YAWatch",
        "Certaines blessures ne disparaissent jamais",
        "La promesse que Luna n'a jamais dite",
        "La nuit où Paris a semblé trop calme",
    ],
    "mysterieuse": [
        "Luna savait une phrase qu'il n'avait jamais dite",
        "Ce que la photo cachait vraiment",
        "Aby était déjà là",
        "Pourquoi Luna connaît-elle ce secret ?",
        "Le jeton noir avait changé de place",
    ],
    "inquietante": [
        "Aby souriait avant de mentir",
        "Le père n'élevait pas ses filles. Il les préparait.",
        "La phrase que Luna n'aurait jamais dû répéter",
        "Le dossier était déjà ouvert",
        "Dans cette famille, on survivait d'abord",
    ],
    "protection": [
        "Malik disait que ça allait",
        "Luna a entendu ce qu'il n'a jamais dit",
        "La protection ressemble parfois au contrôle",
        "Elle voulait sauver les silences",
        "Le premier signal de détresse",
    ],
    "philosophique": [
        "Protéger, est-ce déjà contrôler ?",
        "Luna se souvient d'un refuge. Aby se souvient d'une prison.",
        "Ce que la douceur coûte",
        "La différence entre sauver et posséder",
        "Ce que YAWatch a hérité du père",
    ],
}

_CHARACTERS_BY_TYPE: Dict[str, List[str]] = {
    "emotionnelle": ["Luna_adulte", "Luna_Doll", "Paris_reel"],
    "mysterieuse": ["Luna_adulte", "Aby_adulte", "Paris_reel"],
    "inquietante": ["Aby_adulte", "Pere_Luna_Aby", "Paris_reel"],
    "protection": ["Malik_adulte", "Luna_adulte", "Paris_reel"],
    "philosophique": ["Luna_adulte", "Aby_adulte", "Pere_Luna_Aby"],
}


class StoryGenerator:
    def __init__(self, lore: LoreManager):
        self.lore = lore

    def generate(self, story_type: Optional[str] = None) -> Dict:
        if story_type is None or story_type not in STORY_TYPES:
            story_type = random.choice(STORY_TYPES)

        lore_prompt = self.lore.get_next_story_prompt(story_type)
        characters = _CHARACTERS_BY_TYPE.get(story_type, ["Luna_adulte", "Luna_Doll"])

        story = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "type": story_type,
            "title": random.choice(_TITLES.get(story_type, ["Histoire Luna"])),
            "hook": lore_prompt["hook"],
            "context": lore_prompt["context"],
            "characters": characters,
            "arc": self.lore.current_arc,
            "episode_number": self.lore.episode_count + 1,
            "mystery_level": self.lore.doll_mystery_level,
            "next_secret_hint": self.lore.get_next_secret(),
        }

        logger.info(
            "Histoire générée — type: %s | titre: %s | ep.%d",
            story_type,
            story["title"],
            story["episode_number"],
        )
        return story

    def save(self, story: Dict, output_dir: Path) -> Path:
        filepath = output_dir / f"story_{story['id']}.json"
        save_json(story, filepath)
        logger.debug("Histoire sauvegardée: %s", filepath.name)
        return filepath
