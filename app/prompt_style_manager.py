"""Gestion des styles de prompts pour la génération d'images.

Construit des prompts Stable Diffusion/DALL-E cohérents avec l'univers.
Délègue la validation DNA à VisualConsistencyManager.
"""

import logging
from typing import Dict, List, Optional

from app.visual_consistency_manager import VisualConsistencyManager

logger = logging.getLogger(__name__)


STYLE_PRESETS: Dict[str, Dict[str, str]] = {
    "cinematic": {
        "quality": "cinematic, 4k, photorealistic, award-winning photography",
        "lighting": "dramatic cinematic lighting, volumetric light",
        "mood": "epic, emotional, tense",
        "camera": "35mm lens, shallow depth of field",
    },
    "intimate": {
        "quality": "intimate portrait, soft bokeh, film grain",
        "lighting": "soft natural window light, golden hour",
        "mood": "warm, nostalgic, emotional",
        "camera": "50mm portrait lens, close-up",
    },
    "surveillance": {
        "quality": "premium corporate thriller footage, realistic cinematic photography",
        "lighting": "natural Paris daylight with subtle cold reflections",
        "mood": "controlled, ambiguous, quietly unsettling",
        "camera": "35mm lens, slow observational framing",
    },
    "dreamlike": {
        "quality": "ethereal, soft glow, painterly",
        "lighting": "diffused ambient, pastel tones",
        "mood": "mysterious, otherworldly, gentle",
        "camera": "macro lens, extreme close-up",
    },
}

ASPECT_RATIO_SHORTS = "9:16 vertical, mobile screen format"


class PromptStyleManager:
    """Construit des prompts d'images complets et cohérents."""

    def __init__(self):
        self.vcm = VisualConsistencyManager()

    def build_prompt(
        self,
        scene_description: str,
        scene_type: str,
        characters: List[str],
        style_preset: str = "cinematic",
        extra_details: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Retourne un dict avec 'positive' et 'negative' prompt.
        Garantit la cohérence DNA de tous les personnages présents.
        """
        parts: List[str] = []

        # 1. Contexte visuel de la scène (DNA officiel)
        scene_context = self.vcm.build_scene_context(scene_type, characters)
        parts.append(scene_context)

        # 2. Description narrative
        parts.append(scene_description)

        # 3. Style preset
        preset = STYLE_PRESETS.get(style_preset, STYLE_PRESETS["cinematic"])
        parts.extend(preset.values())

        # 4. Format Shorts
        parts.append(ASPECT_RATIO_SHORTS)

        # 5. Détails supplémentaires
        if extra_details:
            parts.append(extra_details)

        positive = ", ".join(p for p in parts if p)

        # 6. Prompts négatifs fusionnés pour tous les personnages
        negative_parts: List[str] = [
            "blurry, low quality, deformed, ugly, nsfw",
            "text, watermark, signature",
        ]
        for char in characters:
            neg = self.vcm.get_negative_prompt(char)
            if neg:
                negative_parts.append(neg)

        negative = ", ".join(negative_parts)

        # 7. Validation
        for char in characters:
            if not self.vcm.validate_prompt(positive, char):
                logger.warning("Prompt potentiellement incohérent pour %s", char)

        return {"positive": positive, "negative": negative}

    def build_luna_doll_close_up(self, scene_type: str = "emotionnelle") -> Dict[str, str]:
        """Prompt spécialisé : gros plan sur Luna Doll (usage fréquent)."""
        scene_desc = (
            "close-up of a small handmade fabric doll with brown hair and violet velvet dress, "
            "resting on a dark wooden desk, soft focus background with blue monitor glow"
        )
        return self.build_prompt(
            scene_description=scene_desc,
            scene_type=scene_type,
            characters=["Luna_Doll"],
            style_preset="intimate",
        )

    def build_luna_with_doll(self, emotion: str = "contemplative") -> Dict[str, str]:
        """Luna adulte tenant la poupée — scène signature."""
        scene_desc = (
            f"woman in her 30s with long brown hair and dark professional attire, "
            f"{emotion} expression, gently holding a small violet-dressed doll, "
            f"standing in a bright La Defense office with Paris visible through glass"
        )
        return self.build_prompt(
            scene_description=scene_desc,
            scene_type="present_paris",
            characters=["Luna_adulte", "Luna_Doll", "Paris_reel"],
            style_preset="cinematic",
        )

    def build_yawatch_room(self, incident: str = "") -> Dict[str, str]:
        """Salle de contrôle YAWatch — ambiance froide."""
        scene_desc = (
            "premium YAWatch office at La Defense, glass walls, restrained monitoring screens, "
            "Paris daylight, corporate thriller mood"
        )
        if incident:
            scene_desc += f", {incident}"
        return self.build_prompt(
            scene_description=scene_desc,
            scene_type="la_defense",
            characters=["YAWatch", "Paris_reel"],
            style_preset="surveillance",
        )

    def list_presets(self) -> List[str]:
        return list(STYLE_PRESETS.keys())
