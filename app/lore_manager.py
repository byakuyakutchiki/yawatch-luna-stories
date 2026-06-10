"""Gestionnaire de l'état narratif de l'univers YAWatch-Luna.

Maintient la continuité entre tous les épisodes générés.
Persiste dans content/lore/universe_state.json.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from app.utils import load_json, save_json

logger = logging.getLogger(__name__)

ARCS = [
    "saison_1_la_question",
    "saison_2_ombre_du_pere",
    "saison_3_systeme",
    "saison_4_verite",
]

# Secrets révélés progressivement (tous les N épisodes)
SECRETS_TIMELINE: List[Dict] = [
    {"episode": 3, "secret": "Luna comprend une phrase que Malik n'a jamais dite"},
    {"episode": 5, "secret": "Aby connaît l'origine de cette capacité"},
    {"episode": 8, "secret": "Une phrase de Luna vient en réalité de son père"},
    {"episode": 10, "secret": "Aby a manipulé les événements les plus sombres dans l'ombre"},
    {"episode": 20, "secret": "Le père a construit la peur comme une méthode d'éducation"},
    {"episode": 40, "secret": "YAWatch reproduit ce que Luna voulait empêcher de recommencer"},
]


def _default_state() -> Dict:
    return {
        "timeline": {
            "episodes_produced": 0,
            "current_arc": ARCS[0],
            "arc_index": 0,
        },
        "characters": {
            "Luna_Doll": {
                "known_facts": ["petite poupée brune, robe violette"],
                "mystery_level": 1,
            },
            "Luna_adulte": {
                "known_facts": ["fondatrice YAWatch", "fausse suspecte de la saison 1"],
                "secret_revealed": False,
            },
            "Luna_enfant": {
                "known_facts": ["solitaire", "parlait à sa poupée chaque soir"],
            },
            "YAWatch_AI": {
                "known_facts": ["conséquence du traumatisme familial"],
                "suspicion_level": 0,
            },
            "Aby_adulte": {
                "known_facts": ["semble savoir plus qu'elle ne dit"],
                "shadow_manipulation_level": 0,
            },
            "Pere_Luna_Aby": {
                "known_facts": ["blessure d'enfance, présence par traces"],
            },
        },
        "revealed_secrets": [],
        "pending_secrets": [s["secret"] for s in SECRETS_TIMELINE],
    }


class LoreManager:
    def __init__(self, lore_dir: Path):
        self._state_file = lore_dir / "universe_state.json"
        self.state = self._load()

    def _load(self) -> Dict:
        data = load_json(self._state_file)
        if data is None:
            logger.info("Nouvel univers YAWatch initialisé")
            return _default_state()
        return data

    def save(self):
        save_json(self.state, self._state_file)

    # ── Accesseurs ─────────────────────────────────────────────────────────────

    @property
    def episode_count(self) -> int:
        return self.state["timeline"]["episodes_produced"]

    @property
    def current_arc(self) -> str:
        return self.state["timeline"]["current_arc"]

    @property
    def doll_mystery_level(self) -> int:
        return self.state["characters"]["Luna_Doll"]["mystery_level"]

    def get_character(self, name: str) -> Dict:
        return self.state["characters"].get(name, {})

    def get_next_story_prompt(self, story_type: str) -> Dict[str, str]:
        """Prompt contextuel basé sur l'état actuel de l'arc."""
        arc = self.current_arc
        mystery = self.doll_mystery_level

        base_prompts = {
            "emotionnelle": {
                "hook": "Luna gardait une photo qu'elle refusait de regarder.",
                "context": "Dans Paris, tout semblait normal. Mais certains objets accusaient Luna en silence.",
            },
            "mysterieuse": {
                "hook": f"Luna savait quelque chose que personne n'avait dit. (Mystère niveau {mystery}/10)",
                "context": "Le public doit soupçonner Luna, même si Aby laisse les indices les plus sombres.",
            },
            "inquietante": {
                "hook": "Aby souriait toujours avant de mentir sur leur père.",
                "context": "Le père n'apparaît que par traces : photo, phrase, silence, archive.",
            },
            "protection": {
                "hook": "Malik disait que ça allait. Luna savait que c'était faux.",
                "context": "YAWatch doit sembler protéger, mais cette protection vient d'une blessure familiale.",
            },
            "philosophique": {
                "hook": "Et si protéger quelqu'un, c'était déjà commencer à le contrôler ?",
                "context": "Luna et Aby répondent différemment à la même enfance.",
            },
        }

        prompt = base_prompts.get(story_type, base_prompts["emotionnelle"])

        # Enrichit avec les secrets de l'arc
        if arc == "saison_2_ombre_du_pere" and story_type == "inquietante":
            prompt["context"] += " L'ombre du père devient plus visible."
        elif arc == "saison_3_systeme":
            prompt["context"] += " Le système révèle qu'il reproduit une ancienne méthode de contrôle."

        return prompt

    # ── Mutations ──────────────────────────────────────────────────────────────

    def record_episode(self, story_type: str):
        """Enregistre un épisode produit et fait évoluer l'univers."""
        self.state["timeline"]["episodes_produced"] += 1
        n = self.episode_count

        # Progression de l'arc
        arc_idx = self.state["timeline"]["arc_index"]
        thresholds = [10, 25, 40]
        if arc_idx < len(thresholds) and n >= thresholds[arc_idx]:
            arc_idx += 1
            self.state["timeline"]["arc_index"] = arc_idx
            if arc_idx < len(ARCS):
                self.state["timeline"]["current_arc"] = ARCS[arc_idx]
                logger.info("Nouvel arc démarré: %s", ARCS[arc_idx])

        # Progression mystery_level de Luna Doll
        if story_type in ("mysterieuse", "inquietante"):
            current = self.state["characters"]["Luna_Doll"]["mystery_level"]
            self.state["characters"]["Luna_Doll"]["mystery_level"] = min(10, current + 1)

        # Révélation de secrets
        self._check_secret_reveal(n)

        # Progression du soupçon public contre Luna / YAWatch
        if story_type == "inquietante":
            suspicion = self.state["characters"]["YAWatch_AI"].get("suspicion_level", 0)
            self.state["characters"]["YAWatch_AI"]["suspicion_level"] = min(5, suspicion + 1)
            shadow = self.state["characters"].setdefault("Aby_adulte", {}).get(
                "shadow_manipulation_level", 0
            )
            self.state["characters"]["Aby_adulte"]["shadow_manipulation_level"] = min(
                5, shadow + 1
            )

        self.save()

    def _check_secret_reveal(self, episode: int):
        for item in SECRETS_TIMELINE:
            if episode == item["episode"] and item["secret"] in self.state["pending_secrets"]:
                self.state["pending_secrets"].remove(item["secret"])
                self.state["revealed_secrets"].append(
                    {"episode": episode, "secret": item["secret"]}
                )
                logger.info("SECRET RÉVÉLÉ (ep.%d): %s", episode, item["secret"])

    def get_next_secret(self) -> Optional[str]:
        """Prochain secret à révéler (pour teasing narratif)."""
        remaining = self.state.get("pending_secrets", [])
        return remaining[0] if remaining else None

    def summary(self) -> str:
        s = self.state
        lines = [
            f"Épisodes: {s['timeline']['episodes_produced']}",
            f"Arc: {s['timeline']['current_arc']}",
            f"Mystère Luna Doll: {s['characters']['Luna_Doll']['mystery_level']}/10",
            f"Soupçon Luna/YAWatch: {s['characters']['YAWatch_AI'].get('suspicion_level', 0)}/5",
            f"Manipulation cachée Aby: {s['characters'].get('Aby_adulte', {}).get('shadow_manipulation_level', 0)}/5",
            f"Secrets révélés: {len(s['revealed_secrets'])}",
            f"Secrets en attente: {len(s.get('pending_secrets', []))}",
        ]
        return "\n".join(lines)
