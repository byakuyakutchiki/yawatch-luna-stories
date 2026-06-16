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
        "saison_1": "fausse suspecte: le public croit qu'elle cache ou provoque les événements sombres",
        "evolution": "comprend progressivement que certains indices l'accusent alors qu'Aby agit dans l'ombre",
    },
    "Luna_enfant": {
        "nature": "humaine",
        "age": 8,
        "situation": "solitaire, parents absents, luna doll comme seule confidente",
        "importance": "origine de tous les idéaux — flashbacks émotionnels",
    },
    "Aby_adulte": {
        "nature": "humaine",
        "age": 28,
        "cheveux": "blonds",
        "role_narratif": "miroir stratégique de Luna, manipulatrice cachée de la saison 1",
        "apparence": "élégante, froide, tailleur sombre, regard contrôlé",
        "motivation": "pense protéger Luna ou empêcher l'héritage du père de recommencer",
        "interdit": "ne jamais la révéler comme méchante évidente avant le final de saison 1",
    },
    "Aby_enfant": {
        "nature": "humaine",
        "age": 8,
        "cheveux": "blonds",
        "canon": "petite blonde APK avec maquette de ville; ne pas confondre avec Luna enfant",
        "role_narratif": "enfant lucide trop tôt, associe la maquette au contrôle plutôt qu'au refuge",
        "motifs": "maquette, jeton noir, regard fixe, silence stratégique",
    },
    "Pere_Luna_Aby": {
        "nature": "humain",
        "age": 50,
        "role_narratif": "blessure d'enfance de Luna et Aby, figure mafieuse respectable et terrifiante",
        "apparence": "homme élégant, costume sombre, calme menaçant, nerveux sous la surface",
        "croyance": "pense avoir préparé Luna et Aby à survivre",
        "interdit": "pas de méchant cartoon, pas de violence graphique, pas de cris permanents",
    },
    "Malik_adulte": {
        "nature": "humain",
        "role_narratif": "premier cas humain révélant que Luna comprend ce que les gens ne disent pas",
        "apparence": "homme noir adulte, fatigué, retenu, appartement parisien",
        "faille": "silence émotionnel, blessure familiale non verbalisée",
    },
    "Thomas_assistant": {
        "nature": "humain",
        "role_narratif": "assistant YAWatch discret, témoin du quotidien de l'entreprise",
        "apparence": "homme adulte 25-35 ans, professionnel simple, badge discret",
        "fonction": "assistant de direction ou assistant opérationnel",
        "interdit": "pas de personnage comique, pas de sous-fifre caricatural",
    },
    "Sophie_DRH": {
        "nature": "humaine",
        "role_narratif": "DRH de YAWatch, relais humain des tensions internes",
        "apparence": "femme 42-50 ans, cheveux courts ou mi-courts poivre et sel, style RH sobre",
        "fonction": "responsable des ressources humaines",
        "interdit": "ne pas la confondre avec Luna, pas de longs cheveux bruns ondulés",
    },
    "YAWatch_AI": {
        "nature": "intelligence artificielle de surveillance",
        "personnalite": "calme, précise, protectrice mais ambiguë",
        "voix": "calme, précise, légèrement froide",
        "conflit_central": "système créé comme conséquence du traumatisme familial, perçu à tort comme source du danger",
    },
    "Paris_reel": {
        "nature": "décor principal",
        "lieux": "La Défense, bureaux, appartements, métro/RER, quais, cafés, rues",
        "role_narratif": "ancrer le thriller dans une réalité quotidienne lumineuse",
        "interdit": "pas de New York, pas de ville générique américaine, pas de cyberpunk permanent",
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
