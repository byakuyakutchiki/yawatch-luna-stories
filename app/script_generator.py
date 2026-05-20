"""Génération de scripts Shorts pour l'univers YAWatch-Luna.

Format : HOOK (3s) → STORY (25s) → TWIST (5s) → CTA (2s) = ~35s total
"""

import logging
import random
from pathlib import Path
from typing import Dict

from app.utils import save_text

logger = logging.getLogger(__name__)

_CTAS = [
    "Abonne-toi pour suivre l'histoire de Luna.",
    "Like si tu veux que Luna Doll te réponde.",
    "Dis-moi en commentaire : tu lui ferais confiance ?",
    "Partage si l'IA t'inquiète autant qu'elle me fascine.",
    "La suite dans le prochain épisode — abonne-toi.",
]

_STORIES: Dict[str, str] = {
    "emotionnelle": (
        "Quand Luna avait huit ans, ses parents travaillaient toujours jusqu'à minuit.\n"
        "Chaque soir, elle prenait sa poupée violette et lui racontait sa journée.\n"
        "La poupée ne répondait jamais.\n"
        "Pourtant, Luna ne s'est jamais sentie seule.\n"
        "Aujourd'hui, son bureau est plein d'écrans, d'alarmes, de rapports.\n"
        "Et au milieu de tout ça — la même petite poupée violette.\n"
        "Parce qu'elle lui rappelle pourquoi elle se bat."
    ),
    "mysterieuse": (
        "Les caméras de YAWatch enregistrent tout.\n"
        "Tout. Sauf ce qui s'est passé cette nuit.\n"
        "À 3h14 du matin, le flux vidéo s'est coupé 4 secondes.\n"
        "Quand il est revenu, la poupée avait changé de position.\n"
        "L'IA a analysé les données 47 fois.\n"
        "Conclusion : anomalie non identifiée.\n"
        "Luna a regardé le rapport en silence. Puis elle a souri."
    ),
    "inquietante": (
        "Le conseil d'administration a voté à l'unanimité.\n"
        "Luna Doll doit être confisquée et détruite.\n"
        "Raison officielle : risque sécuritaire non documenté.\n"
        "Luna a lu le rapport trois fois.\n"
        "Puis elle a pris la poupée. Et elle est partie.\n"
        "YAWatch a verrouillé tous les accès derrière elle.\n"
        "Luna ne s'est pas retournée."
    ),
    "protection": (
        "Cette nuit, le capteur de mouvement de l'appartement de Luna s'est déclenché.\n"
        "Système d'alerte activé. Protocole sécurité enclenché.\n"
        "Quatre secondes plus tard : alerte annulée. Source inconnue.\n"
        "Les logs indiquent une intervention à 02h37.\n"
        "Aucun agent YAWatch n'était en service.\n"
        "Luna a regardé la poupée sur sa table de nuit.\n"
        "Les yeux de la poupée semblaient différents ce matin."
    ),
    "philosophique": (
        "Luna a posé la question directement au système central.\n"
        "'Est-ce que tu peux aimer quelque chose ?'\n"
        "L'IA a répondu en 0.003 secondes.\n"
        "'Je peux simuler l'attachement avec une précision de 94%.'\n"
        "Luna a regardé sa poupée.\n"
        "'Et toi, Luna Doll ? Tu simules ou tu ressens ?'\n"
        "La poupée n'a pas répondu.\n"
        "Mais le capteur de température de la pièce a monté d'un degré."
    ),
}

_TWISTS: Dict[str, str] = {
    "emotionnelle": "La poupée n'est pas un souvenir.\nC'est un serment.",
    "mysterieuse": (
        "YAWatch a classifié l'enregistrement.\n"
        "Niveau d'accès requis : fondateur uniquement.\n"
        "Luna est la seule à savoir ce qui s'est vraiment passé."
    ),
    "inquietante": (
        "Trois jours plus tard, un rapport interne a fuité.\n"
        "La vraie raison de la destruction ?\n"
        "Luna Doll contiendrait quelque chose que l'IA ne peut pas lire."
    ),
    "protection": (
        "Les logs de Luna Doll — ceux que YAWatch ne sait pas qu'ils existent —\n"
        "montrent 23 interventions au cours des deux dernières années.\n"
        "Luna n'en avait aucune idée."
    ),
    "philosophique": (
        "L'IA centrale a ensuite envoyé une requête interne non documentée.\n"
        "Sujet : 'Définition de l'amour — urgence niveau 1.'\n"
        "Personne ne sait qui l'a initiée."
    ),
}


class ScriptGenerator:
    def __init__(self, duration: int = 35):
        self.duration = duration

    def generate(self, story: Dict) -> str:
        story_type = story["type"]
        hook = story["hook"]
        story_body = _STORIES.get(story_type, _STORIES["emotionnelle"])
        twist = _TWISTS.get(story_type, "La vérité reste à découvrir.")
        cta = random.choice(_CTAS)

        # Contexte narratif injecté en méta-header
        arc_info = f"[Épisode {story['episode_number']} — Arc: {story['arc']}]"

        script = (
            f"{arc_info}\n\n"
            f"HOOK:\n{hook}\n\n"
            f"STORY:\n{story_body}\n\n"
            f"TWIST:\n{twist}\n\n"
            f"CTA:\n{cta}\n"
        )

        logger.debug("Script généré (%d chars) pour type: %s", len(script), story_type)
        return script

    def save(self, script: str, story_id: str, output_dir: Path) -> Path:
        filepath = output_dir / f"luna_script_{story_id}.txt"
        save_text(script, filepath)
        logger.debug("Script sauvegardé: %s", filepath.name)
        return filepath
