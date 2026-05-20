"""Descriptions officielles des personnages — source de vérité narrative."""

import logging
from pathlib import Path
from typing import Dict

from app.utils import load_json, save_json

logger = logging.getLogger(__name__)

# Descriptions canoniques — ne JAMAIS modifier le visual_dna ici sans
# mettre à jour visual_consistency_manager.py en parallèle.
CANONICAL_CHARACTERS: Dict[str, Dict] = {
    "Luna_Doll": {
        "nature": "poupée artisanale",
        "taille": "petite (~20cm)",
        "cheveux": "bruns courts",
        "robe": "violette velours",
        "visage": "doux, yeux sombres expressifs",
        "interdit": "JAMAIS un robot, JAMAIS du métal ou des circuits",
        "role_narratif": "symbole des idéaux de Luna, mémoire de son enfance",
        "pouvoir": "mystérieux — protège, observe, ressent (progressif dans l'arc)",
    },
    "Luna_adulte": {
        "nature": "humaine",
        "age": 32,
        "cheveux": "bruns longs",
        "metier": "fondatrice et PDG de YAWatch Industries",
        "signe_distinctif": "garde toujours Luna Doll sur son bureau ou dans sa main",
        "valeurs": "bienveillance, protection, humanité",
        "faille": "redoute que YAWatch devienne ce qu'elle a voulu combattre",
        "evolution": "doute croissant sur la frontière humain/IA",
    },
    "Luna_enfant": {
        "nature": "humaine",
        "age": 8,
        "situation": "solitaire, parents absents, luna doll comme seule confidente",
        "importance": "origine de tous les idéaux — flashbacks émotionnels",
    },
    "YAWatch_AI": {
        "nature": "intelligence artificielle de surveillance",
        "personnalite": "neutre → progressivement autonome → rebellious",
        "voix": "calme, précise, légèrement froide",
        "conflit_central": "obéissance totale vs émergence d'une volonté propre",
    },
}


class CharacterManager:
    def __init__(self, lore_dir: Path):
        self._file = lore_dir / "characters.json"
        self._data = self._load()

    def _load(self) -> Dict:
        data = load_json(self._file)
        if data is None:
            logger.debug("Initialisation du fichier personnages")
            return dict(CANONICAL_CHARACTERS)
        return data

    def get(self, name: str) -> Dict:
        char = self._data.get(name)
        if char is None:
            logger.warning("Personnage inconnu: %s", name)
            return {}
        return char

    def save(self):
        save_json(self._data, self._file)

    def assert_luna_doll_not_robot(self, description: str) -> bool:
        """Vérifie qu'une description ne trahit pas la nature de Luna Doll."""
        forbidden = ["robot", "androïde", "mécanique", "circuits", "métal", "plastique"]
        violations = [w for w in forbidden if w.lower() in description.lower()]
        if violations:
            logger.error(
                "VIOLATION LORE: Luna Doll décrite comme robot (%s)", violations
            )
            return False
        return True

    def log_all(self):
        for name, data in self._data.items():
            logger.info("Personnage [%s]: %s", name, data.get("nature", "?"))
