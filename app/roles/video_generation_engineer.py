"""Rôle : Video Generation Engineer.

Responsabilité : s'assurer que les clips proviennent d'un vrai outil image-to-video
(Kling, SVD, CogVideoX, AnimateDiff) et non d'un assemblage FFmpeg d'images fixes.
"""

from pathlib import Path

from app.roles.base_role import BaseRole, VerdictResult

PLACEHOLDER_PATTERNS = frozenset({
    "scene_hook", "scene_story", "scene_climax", "scene_resolution",
    "episode_test", "placeholder", "test_image", "demo_", "sample_",
    "untitled", "image_test",
})

I2V_TOOL_MARKERS = frozenset({
    "kling", "runway", "luma", "svd", "cogvideox", "animatediff",
    "wan2", "pika", "stable_video",
})

CANON_TEASER_ASSETS = frozenset({
    "luna_adulte_neutral_9x16_01",
    "luna_adulte_office_desk_01",
    "luna_adulte_looking_at_turned_photo_01",
    "luna_enfant_worried_night_01",
    "luna_enfant_comforted_with_doll_01",
    "poupee_luna_gros_plan_yeux_mystere_01",
    "aby_adulte_observing_luna_01",
    "aby_enfant_main_jeton_noir_maquette_01",
    "yawatch_tour_la_defense_exterieur_jour",
})


class VideoGenerationEngineer(BaseRole):
    role_name = "VideoGenerationEngineer"
    knowledge_doc = "IMAGE_TO_VIDEO_ENGINE_RULES.md"
    verdict_name = "verdict_generation_clips"

    def validate(self, context: dict) -> VerdictResult:
        """
        context attendu :
          - "clips" : list[str|Path] — chemins des clips MP4
          - "source_images" : list[str|Path] — images source utilisées
          - "i2v_tool" : str — outil utilisé ("kling", "svd", "ffmpeg_zoompan", ...)
          - "manifest" : dict — manifest JSON du pipeline (optionnel)
        """
        errors: list[str] = []
        warnings: list[str] = []

        source_images: list[str] = [str(p) for p in context.get("source_images", [])]
        clips: list[str] = [str(p) for p in context.get("clips", [])]
        i2v_tool: str = context.get("i2v_tool", "unknown").lower()
        manifest: dict = context.get("manifest", {})

        # Règle 0 : FFmpeg zoompan n'est pas un outil de génération de clips
        if i2v_tool in ("ffmpeg", "ffmpeg_zoompan", "moviepy", "unknown"):
            if clips:
                errors.append(
                    f"Outil '{i2v_tool}' ne génère pas de mouvement réel. "
                    "Utiliser Kling, SVD, CogVideoX ou AnimateDiff. "
                    "Voir IMAGE_TO_VIDEO_ENGINE_RULES.md — Règle 0."
                )

        # Règle 1 : Images source ne doivent pas être des placeholders
        for img in source_images:
            img_lower = img.lower()
            for pattern in PLACEHOLDER_PATTERNS:
                if pattern in img_lower:
                    errors.append(f"Image placeholder interdite en production : {Path(img).name}")
                    break

        # Règle 2 : Pour le teaser, les images doivent être les assets canon
        episode_id: str = context.get("episode_id", "")
        if "teaser" in episode_id.lower() or "s01e00" in episode_id.lower():
            for img in source_images:
                stem = Path(img).stem.lower()
                if not any(canon in stem for canon in CANON_TEASER_ASSETS):
                    warnings.append(
                        f"Image teaser non reconnue comme asset canon : {Path(img).name}. "
                        "Vérifier TEASER_S01E00_PRODUCTION_PACK.md."
                    )

        # Règle 3 : Manifest status ne doit pas être "prototype" avec des clips déclarés
        manifest_status = manifest.get("status", "")
        if manifest_status == "prototype" and clips:
            warnings.append(
                "Le manifest indique STATUS=prototype mais des clips sont listés. "
                "Un prototype ne contient pas de vrais clips IA."
            )

        # Règle 4 : Vérifier que les clips existent sur disque
        missing_clips = [c for c in clips if not Path(c).exists()]
        if missing_clips:
            for c in missing_clips:
                errors.append(f"Clip introuvable sur disque : {Path(c).name}")

        if errors:
            return VerdictResult(self.verdict_name, "FAIL", errors, warnings)
        if not clips and not source_images:
            return VerdictResult(
                self.verdict_name, "FAIL",
                ["Aucun clip ni image source fourni — pipeline vide."], warnings
            )
        return VerdictResult(self.verdict_name, "PASS", [], warnings)
