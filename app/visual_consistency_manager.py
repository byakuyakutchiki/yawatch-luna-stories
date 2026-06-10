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
    "ambiance": "protectrice, crédible, cinématique, fausse suspecte de la saison 1",
    "interdit": "pas de super-héroïne, pas d'uniforme, pas d'armure",
}

ABY_ADULTE_DNA: Dict[str, str] = {
    "type": "femme humaine réelle",
    "age_apparent": "28-32 ans",
    "cheveux": "blonds, coiffés avec précision",
    "tenue": "tailleur noir ou anthracite, bijoux discrets",
    "regard": "froid, stratégique, calme, contrôlé",
    "motifs": "reflets, dossiers, jeton noir, présence hors champ",
    "ambiance": "manipulatrice cachée, jamais méchante évidente avant le final",
    "interdit": "pas de sourire maléfique, pas de posture cartoon villain",
}

ABY_ENFANT_DNA: Dict[str, str] = {
    "type": "petite fille humaine canon APK",
    "age_apparent": "8 ans",
    "cheveux": "blonds",
    "regard": "dur, lucide, stratégique",
    "motifs": "maquette de ville, jeton noir, chambre, lumières miniatures",
    "ambiance": "enfance froide, contrôle, observation",
    "interdit": "ne pas la confondre avec Luna enfant, pas de cartoon, pas d'expression hystérique",
}

PERE_LUNA_ABY_DNA: Dict[str, str] = {
    "type": "homme humain élégant, figure mafieuse",
    "age_apparent": "45-60 ans",
    "cheveux": "gris ou noirs, barbe courte possible",
    "tenue": "costume sombre, chemise noire ou blanche, montre discrète",
    "regard": "calme, dominant, menaçant sans geste spectaculaire",
    "ambiance": "blessure d'enfance, pouvoir, peur contenue",
    "interdit": "pas de gangster cartoon, pas de violence graphique, pas d'arme mise en avant",
}

MALIK_ADULTE_DNA: Dict[str, str] = {
    "type": "homme noir adulte réel",
    "age_apparent": "30-45 ans",
    "tenue": "sobre, vêtements sombres quotidiens",
    "regard": "fatigué, retenu, silencieux",
    "ambiance": "appartement parisien, solitude, blessure non dite",
    "interdit": "pas d'action héroïque, pas de colère spectaculaire",
}

YAWATCH_ENV_DNA: Dict[str, str] = {
    "type": "bureaux premium à La Défense, Paris",
    "eclairage": "lumière parisienne claire, reflets de verre; bascule bleu/violet seulement en tension",
    "elements": "tour de bureaux, vitres, skyline La Défense, écrans discrets, salles de réunion",
    "atmosphere": "réussite publique, protection ambiguë, contrôle sous-jacent",
    "palette": "lumière claire, verre, anthracite, acier, violet Luna discret",
    "interdit": "pas de New York, pas de cyberpunk permanent, pas de bleu sombre dominant sans raison",
}

PARIS_REAL_DNA: Dict[str, str] = {
    "type": "Paris réel contemporain",
    "lieux": "La Défense, Quatre Temps, métro/RER, quais de Seine, Marais, cafés, appartements",
    "eclairage": "lumière naturelle, couleurs de vie quotidienne",
    "ambiance": "thriller émotionnel ancré dans le réel, pas carte postale permanente",
    "interdit": "pas de ville américaine, pas de skyline New York, pas de décor générique",
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

SCENE_PARIS_PRESENT_DNA: Dict[str, str] = {
    "eclairage": "lumière naturelle parisienne, reflets réalistes",
    "composition": "décor vécu, personnages intégrés au lieu, pas de pose publicitaire",
    "palette": "tons clairs, pierre, verre, acier, touches humaines",
    "ambiance": "présent crédible, thriller humain, vie quotidienne",
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
    "Aby_adulte": [
        "cartoon villain", "evil grin", "witch", "monster", "red eyes",
        "armor", "weapon focus", "brunette",
    ],
    "Aby_enfant": [
        "brunette", "Luna child", "cartoon", "anime", "hysterical",
        "evil child", "monster",
    ],
    "Pere_Luna_Aby": [
        "cartoon gangster", "gun focus", "blood", "gore", "screaming",
        "supervillain", "mask",
    ],
    "Malik_adulte": [
        "superhero", "weapon", "rage", "gangster", "cartoon", "anime",
    ],
    "YAWatch_env": [
        "New York", "Manhattan", "cyberpunk city", "spaceship", "rustic", "vintage",
    ],
    "YAWatch": [
        "New York", "Manhattan", "cyberpunk city", "spaceship", "rustic", "vintage",
    ],
    "Paris_reel": [
        "New York", "Manhattan", "Los Angeles", "Tokyo", "generic American city",
        "cyberpunk", "futuristic megacity",
    ],
}

# ── API publique ───────────────────────────────────────────────────────────────


class VisualConsistencyManager:
    """Valide et renforce la cohérence visuelle de tous les prompts générés."""

    def get_character_dna(self, character: str) -> Dict[str, str]:
        mapping = {
            "Luna_Doll": LUNA_DOLL_DNA,
            "Luna_adulte": LUNA_ADULTE_DNA,
            "Aby_adulte": ABY_ADULTE_DNA,
            "Aby_enfant": ABY_ENFANT_DNA,
            "Pere_Luna_Aby": PERE_LUNA_ABY_DNA,
            "Malik_adulte": MALIK_ADULTE_DNA,
            "YAWatch": YAWATCH_ENV_DNA,
            "YAWatch_env": YAWATCH_ENV_DNA,
            "Paris_reel": PARIS_REAL_DNA,
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
            "present_paris": SCENE_PARIS_PRESENT_DNA,
            "la_defense": SCENE_PARIS_PRESENT_DNA,
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
        if "Aby_adulte" in characters:
            a = ABY_ADULTE_DNA
            parts.append(
                f"blonde woman {a['age_apparent']}, {a['tenue']}, {a['regard']}"
            )
        if "Aby_enfant" in characters:
            a = ABY_ENFANT_DNA
            parts.append(
                f"blonde child {a['age_apparent']}, {a['regard']}, miniature city"
            )
        if "Pere_Luna_Aby" in characters:
            p = PERE_LUNA_ABY_DNA
            parts.append(
                f"elegant threatening father figure, {p['tenue']}, {p['regard']}"
            )
        if "Malik_adulte" in characters:
            m = MALIK_ADULTE_DNA
            parts.append(f"Black adult man, {m['regard']}, {m['ambiance']}")
        if "YAWatch_AI" in characters or "YAWatch" in characters or "YAWatch_env" in characters:
            parts.append(YAWATCH_ENV_DNA["elements"])
        if "Paris_reel" in characters:
            parts.append(PARIS_REAL_DNA["lieux"])

        return ", ".join(p for p in parts if p)
