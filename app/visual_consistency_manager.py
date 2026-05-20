"""Garant de la cohérence visuelle de l'univers YAWatch-Luna.

Ce module est la source de vérité pour l'apparence de chaque entité.
Tout module générant des prompts d'images DOIT passer par ici.
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

# ── DNA visuel officiel ────────────────────────────────────────────────────────

LUNA_DOLL_DNA: Dict[str, str] = {
    "type": "poupée artisanale",
    "taille": "petite, environ 20cm",
    "cheveux": "bruns courts, lisses",
    "robe": "violette, velours, col rond, légèrement usée",
    "visage": "doux, yeux sombres expressifs, pas de maquillage",
    "texture": "tissu, coutures visibles, artisanal",
    "ambiance": "chaleureuse, émotionnelle, mystérieuse",
    "interdit": "pas de robot, pas de métal, pas de circuits, pas de LED, pas de plastique",
}

LUNA_ADULTE_DNA: Dict[str, str] = {
    "type": "femme humaine réelle",
    "age_apparent": "30-35 ans",
    "cheveux": "bruns longs ondulés",
    "tenue": "sobre, tenue professionnelle sombre (gris anthracite ou noir)",
    "regard": "déterminé, empathique, légèrement mélancolique",
    "accessoire_signature": "tient ou pose la poupée violette",
    "ambiance": "protectrice, crédible, cinématique",
    "interdit": "pas de super-héroïne, pas d'uniforme, pas d'armure",
}

YAWATCH_ENV_DNA: Dict[str, str] = {
    "type": "environnement futuriste froid",
    "eclairage": "bleu-vert froid, néons distants, reflets sur acier",
    "elements": "écrans de monitoring, feeds caméra, terminaux CLI, couloirs épurés",
    "atmosphere": "surveillance, silence, efficacité clinique",
    "palette": "bleu acier, gris anthracite, blanc froid, accents cyan",
    "interdit": "pas de couleurs chaudes dominantes, pas de nature, pas de chaleur",
}

SCENE_EMOTIONAL_DNA: Dict[str, str] = {
    "eclairage": "lumière chaude douce, un unique point de lumière",
    "composition": "gros plan sur les mains tenant la poupée, profondeur de champ réduite",
    "palette": "teintes sépia légères, violette de la robe en accent",
    "ambiance": "intime, nostalgie, bienveillance",
}

SCENE_MYSTERY_DNA: Dict[str, str] = {
    "eclairage": "contre-jour, ombre portée, rayon de lumière unique",
    "composition": "angle bas, poupée en premier plan floue, personnage en arrière-plan net",
    "palette": "noir dominant, violette saturé sur la robe, cyan sur les écrans",
    "ambiance": "tension, secret, présence inquiète",
}

NEGATIVE_PROMPTS: Dict[str, List[str]] = {
    "Luna_Doll": [
        "robot", "cyborg", "circuits", "metal", "plastic", "LED",
        "screen face", "screen eyes", "digital face",
        "futuristic doll", "android", "blonde", "red dress", "green dress",
        "big", "tall", "realistic human", "3D render",
    ],
    "Luna_adulte": [
        "superhero", "armor", "weapon", "cartoon", "anime", "blonde",
        "old woman", "child",
    ],
    "YAWatch_env": [
        "nature", "trees", "warm colors", "rustic", "vintage",
    ],
}

# ── API publique ───────────────────────────────────────────────────────────────


class VisualConsistencyManager:
    """Valide et renforce la cohérence visuelle de tous les prompts générés."""

    def get_character_dna(self, character: str) -> Dict[str, str]:
        mapping = {
            "Luna_Doll": LUNA_DOLL_DNA,
            "Luna_adulte": LUNA_ADULTE_DNA,
            "YAWatch": YAWATCH_ENV_DNA,
        }
        dna = mapping.get(character)
        if dna is None:
            logger.warning("Personnage inconnu: %s — DNA vide retourné", character)
            return {}
        return dna

    def get_negative_prompt(self, character: str) -> str:
        return ", ".join(NEGATIVE_PROMPTS.get(character, []))

    def get_scene_dna(self, scene_type: str) -> Dict[str, str]:
        mapping = {
            "emotionnelle": SCENE_EMOTIONAL_DNA,
            "mysterieuse": SCENE_MYSTERY_DNA,
            "inquietante": SCENE_MYSTERY_DNA,
            "protection": SCENE_EMOTIONAL_DNA,
            "philosophique": SCENE_EMOTIONAL_DNA,
        }
        return mapping.get(scene_type, SCENE_EMOTIONAL_DNA)

    def enforce_luna_doll(self, prompt: str) -> str:
        """Injecte les attributs obligatoires de Luna Doll dans un prompt."""
        dna = LUNA_DOLL_DNA
        enforced = (
            f"{prompt}, {dna['type']}, {dna['taille']}, "
            f"cheveux {dna['cheveux']}, robe {dna['robe']}, "
            f"visage {dna['visage']}, texture {dna['texture']}"
        )
        logger.debug("Luna Doll DNA injectée dans le prompt")
        return enforced

    def validate_prompt(self, prompt: str, character: str) -> bool:
        """Vérifie qu'un prompt ne contredit pas le DNA officiel."""
        violations = NEGATIVE_PROMPTS.get(character, [])
        found = [v for v in violations if v.lower() in prompt.lower()]
        if found:
            logger.warning(
                "Prompt viole le DNA de %s — mots interdits: %s", character, found
            )
            return False
        return True

    def build_scene_context(self, scene_type: str, characters: List[str]) -> str:
        """Compose le contexte visuel d'une scène complète."""
        parts = []
        scene_dna = self.get_scene_dna(scene_type)
        parts.append(scene_dna.get("eclairage", ""))
        parts.append(scene_dna.get("ambiance", ""))
        parts.append(scene_dna.get("palette", ""))

        if "Luna_Doll" in characters:
            d = LUNA_DOLL_DNA
            parts.append(
                f"small handmade doll, {d['cheveux']} hair, {d['robe']} dress"
            )
        if "Luna_adulte" in characters:
            a = LUNA_ADULTE_DNA
            parts.append(
                f"woman {a['age_apparent']}, {a['cheveux']} hair, {a['tenue']}"
            )
        if "YAWatch_AI" in characters:
            parts.append(YAWATCH_ENV_DNA["elements"])

        return ", ".join(p for p in parts if p)
