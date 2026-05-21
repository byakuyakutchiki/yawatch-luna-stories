"""Production automatisée d'épisodes en volume."""

import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from app.config_loader import ConfigLoader, PROJECT_ROOT
from app.lore_manager import LoreManager
from app.story_generator import StoryGenerator
from app.script_generator import ScriptGenerator
from app.image_prompt_generator import ImagePromptGenerator
from app.voice_generator import VoiceGenerator
from app.subtitle_generator import SubtitleGenerator
from app.audio_mixer import AudioMixer
from app.scene_composer import SceneComposer
from app.export_manager import ExportManager
from app.utils import ensure_dir, get_logger, save_json, load_json

logger = get_logger(__name__)

HISTORY_FILE = PROJECT_ROOT / "outputs" / "batch_history.json"


class BatchProcessor:
    """Produit N épisodes en séquence avec gestion d'erreurs et historique."""

    def __init__(self, config: ConfigLoader):
        self.config = config
        lore_dir = config.get_path("paths.lore_dir")
        self.lore = LoreManager(lore_dir)
        self.story_gen = StoryGenerator(self.lore)
        self.script_gen = ScriptGenerator()
        self.img_gen = ImagePromptGenerator()
        self.voice_gen = VoiceGenerator(openai_key=config.openai_key)
        self.sub_gen = SubtitleGenerator()
        self.mixer = AudioMixer()
        self.composer = SceneComposer()
        self.exporter = ExportManager()
        self.history = load_json(HISTORY_FILE) or {"batches": [], "total_episodes": 0}

    def produce(
        self,
        count: int,
        story_type: Optional[str] = None,
        delay_seconds: float = 1.0,
    ) -> List[Dict]:
        logger.info("Batch démarré: %d épisodes", count)
        batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = []

        for i in range(count):
            logger.info("Épisode %d/%d", i + 1, count)
            result = self._produce_one(story_type)
            result["batch_index"] = i + 1
            results.append(result)

            if result["status"] == "success":
                self.lore.record_episode(result["type"])

            if i < count - 1 and delay_seconds > 0:
                time.sleep(delay_seconds)

        successful = [r for r in results if r["status"] == "success"]
        self.history["batches"].append({
            "batch_id": batch_id,
            "date": datetime.now().isoformat(),
            "count": count,
            "successful": len(successful),
        })
        self.history["total_episodes"] += len(successful)
        ensure_dir(HISTORY_FILE.parent)
        save_json(self.history, HISTORY_FILE)

        logger.info("Batch terminé: %d/%d réussis", len(successful), count)
        return results

    def _produce_one(self, story_type: Optional[str]) -> Dict:
        try:
            story = self.story_gen.generate(story_type)
            script = self.script_gen.generate(story)

            story_id = story["id"]
            scripts_dir = self.config.get_path("paths.scripts_dir")
            audio_dir = self.config.get_path("paths.audio_dir")
            subs_dir = self.config.get_path("paths.subtitles_dir")
            images_dir = self.config.get_path("paths.images_dir")

            script_path = self.script_gen.save(script, story_id, scripts_dir)

            # Audio
            raw_audio = audio_dir / f"luna_{story_id}.mp3"
            self.voice_gen.text_to_speech(script, raw_audio)
            mixed_audio = self.mixer.mix(raw_audio, audio_dir / f"luna_{story_id}_mixed.mp3")

            # Sous-titres
            subs_path = self.sub_gen.generate(script, story_id, subs_dir)

            # Prompts images
            prompts = self.img_gen.generate_for_story(story)
            self.img_gen.save(prompts, story_id, images_dir)

            # Composition scènes
            self.composer.compose(script)

            # Export package
            self.exporter.create_package(
                episode_id=story_id,
                story=story,
                script_path=script_path,
                subtitles_path=subs_path,
            )

            return {
                "status": "success",
                "episode_id": story_id,
                "title": story["title"],
                "type": story["type"],
                "arc": story["arc"],
                "script_path": str(script_path),
                "audio_path": str(mixed_audio),
                "subtitles_path": str(subs_path),
            }

        except Exception as e:
            logger.error("Épisode échoué: %s", e)
            return {"status": "failed", "error": str(e), "type": story_type or "unknown"}
