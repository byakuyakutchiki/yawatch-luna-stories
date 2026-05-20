"""Gestionnaire de l'état narratif de l'univers YAWatch-Luna.

Maintient la continuité entre tous les épisodes générés.
Persiste dans content/lore/universe_state.json.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from app.utils import load_json, save_json

logger = logging.getLogger(__name__)

ARCS = ["saison_1_enfance", "saison_2_yawatch", "saison_3_mystere", "saison_4_verite"]

# Secrets révélés progressivement (tous les N épisodes)
SECRETS_TIMELINE: List[Dict] = [
    {"episode": 5,  "secret": "Luna Doll a été faite par Luna enfant elle-même avec du tissu volé"},
    {"episode": 10, "secret": "La poupée contient un fragment de code IA prototype"},
    {"episode": 15, "secret": "YAWatch Industries a voulu racheter le brevet de la poupée"},
    {"episode": 20, "secret": "Luna Doll a protégé Luna enfant d'un danger réel une nuit"},
    {"episode": 30, "secret": "La vraie fondatrice de YAWatch n'est pas Luna — elle l'a repris de force"},
    {"episode": 40, "secret": "Luna Doll est le seul objet qui peut désactiver le système central"},
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
                "known_facts": ["fondatrice YAWatch", "garde toujours sa poupée"],
                "secret_revealed": False,
            },
            "Luna_enfant": {
                "known_facts": ["solitaire", "parlait à sa poupée chaque soir"],
            },
            "YAWatch_AI": {
                "known_facts": ["surveille tout"],
                "rebellion_stage": 0,
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
                "hook": "Quand Luna était petite, elle n'avait qu'une seule amie.",
                "context": "Chaque soir, elle serrait sa poupée violette et lui chuchotait ses peurs.",
            },
            "mysterieuse": {
                "hook": f"À 3h14 du matin, la poupée a bougé. Seule. (Mystère niveau {mystery}/10)",
                "context": "Les logs YAWatch ont capturé quelque chose d'inexplicable.",
            },
            "inquietante": {
                "hook": "YAWatch Industries a émis un ordre de destruction.",
                "context": "L'objet visé : Luna Doll. La raison : classifiée.",
            },
            "protection": {
                "hook": "Cette nuit, une alarme s'est déclenchée. Et s'est éteinte toute seule.",
                "context": "Les logs indiquent une intervention. Source : inconnue.",
            },
            "philosophique": {
                "hook": "Luna a demandé à l'IA : 'Est-ce que tu peux aimer ?'",
                "context": "L'IA n'a pas répondu. Mais la poupée a bougé.",
            },
        }

        prompt = base_prompts.get(story_type, base_prompts["emotionnelle"])

        # Enrichit avec les secrets de l'arc
        if arc == "saison_2_yawatch" and story_type == "inquietante":
            prompt["context"] += " YAWatch prépare quelque chose depuis 3 ans."
        elif arc == "saison_3_mystere":
            prompt["context"] += " La vérité commence à émerger."

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

        # Progression rebellion YAWatch
        if story_type == "inquietante":
            rb = self.state["characters"]["YAWatch_AI"]["rebellion_stage"]
            self.state["characters"]["YAWatch_AI"]["rebellion_stage"] = min(5, rb + 1)

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
            f"Rébellion YAWatch: {s['characters']['YAWatch_AI']['rebellion_stage']}/5",
            f"Secrets révélés: {len(s['revealed_secrets'])}",
            f"Secrets en attente: {len(s.get('pending_secrets', []))}",
        ]
        return "\n".join(lines)
