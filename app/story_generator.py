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
        "Pourquoi Luna ne lâche jamais sa poupée",
        "L'enfance que personne ne connaît",
        "La promesse faite à Luna Doll",
        "Ce qu'elle lui chuchotait chaque soir",
        "La nuit où Luna a pleuré pour la dernière fois",
    ],
    "mysterieuse": [
        "La poupée a bougé à 3h14",
        "Ce que les caméras ont filmé",
        "Luna Doll ne dort jamais",
        "Anomalie non identifiée — rapport #0047",
        "Quelque chose surveille à travers la poupée",
    ],
    "inquietante": [
        "YAWatch veut détruire Luna Doll",
        "L'ordre de destruction — classifié",
        "Luna a refusé pour la première fois",
        "Que cache vraiment la poupée ?",
        "Le conseil vote. Luna s'y oppose seule.",
    ],
    "protection": [
        "Luna Doll a sauvé quelqu'un cette nuit",
        "L'alarme s'est éteinte toute seule",
        "Elle veille quand Luna dort",
        "Présence non identifiée — alerte annulée",
        "La poupée sait ce que l'IA ignore",
    ],
    "philosophique": [
        "L'IA peut-elle aimer ?",
        "La différence entre obéir et choisir",
        "Luna demande : qu'est-ce que ressentir ?",
        "La poupée ou le système — qui est plus humain ?",
        "Ce que YAWatch ne comprendra jamais",
    ],
}

_CHARACTERS_BY_TYPE: Dict[str, List[str]] = {
    "emotionnelle": ["Luna_adulte", "Luna_enfant", "Luna_Doll"],
    "mysterieuse": ["Luna_adulte", "Luna_Doll", "YAWatch_AI"],
    "inquietante": ["Luna_adulte", "Luna_Doll", "YAWatch_AI"],
    "protection": ["Luna_Doll", "Luna_adulte"],
    "philosophique": ["Luna_adulte", "YAWatch_AI", "Luna_Doll"],
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
