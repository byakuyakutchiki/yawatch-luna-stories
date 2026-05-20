"""Génération de prompts d'images pour chaque scène du script.

Délègue la cohérence visuelle à PromptStyleManager.
"""

import logging
from pathlib import Path
from typing import Dict, List

from app.prompt_style_manager import PromptStyleManager
from app.utils import save_json

logger = logging.getLogger(__name__)


class ImagePromptGenerator:
    def __init__(self):
        self.psm = PromptStyleManager()

    def generate_for_story(self, story: Dict) -> List[Dict[str, str]]:
        """Génère 3-4 prompts d'images pour couvrir le script complet."""
        story_type = story["type"]
        characters = story["characters"]
        prompts = []

        # Scène 1 : ouverture / hook
        prompts.append({
            "scene": "hook",
            **self.psm.build_luna_doll_close_up(scene_type=story_type),
        })

        # Scène 2 : story body
        if "Luna_adulte" in characters:
            emotion_map = {
                "emotionnelle": "nostalgic",
                "mysterieuse": "concerned",
                "inquietante": "defiant",
                "protection": "grateful",
                "philosophique": "contemplative",
            }
            emotion = emotion_map.get(story_type, "contemplative")
            prompts.append({
                "scene": "story",
                **self.psm.build_luna_with_doll(emotion=emotion),
            })
        else:
            prompts.append({
                "scene": "story",
                **self.psm.build_yawatch_room(),
            })

        # Scène 3 : twist — ambiance froide YAWatch
        prompts.append({
            "scene": "twist",
            **self.psm.build_yawatch_room(
                incident="warning alert on screen, red notification light"
            ),
        })

        # Scène 4 : cta — poupée seule en premier plan
        prompts.append({
            "scene": "cta",
            **self.psm.build_prompt(
                scene_description=(
                    "small violet-dressed doll alone on an empty dark desk, "
                    "single spotlight from above, dramatic shadow, subscribe button overlay area"
                ),
                scene_type="mysterieuse",
                characters=["Luna_Doll"],
                style_preset="dreamlike",
            ),
        })

        logger.info("%d prompts générés pour histoire type: %s", len(prompts), story_type)
        return prompts

    def save(self, prompts: List[Dict], story_id: str, output_dir: Path) -> Path:
        filepath = output_dir / f"prompts_{story_id}.json"
        save_json({"story_id": story_id, "scenes": prompts}, filepath)
        logger.debug("Prompts sauvegardés: %s", filepath.name)
        return filepath
