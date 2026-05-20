"""Pipeline YAWatch Luna Stories — point d'entrée principal."""

import argparse
import logging
import sys
from pathlib import Path

from app.config_loader import ConfigLoader, PROJECT_ROOT
from app.lore_manager import LoreManager
from app.character_manager import CharacterManager
from app.story_generator import StoryGenerator
from app.script_generator import ScriptGenerator
from app.image_prompt_generator import ImagePromptGenerator
from app.voice_generator import VoiceGenerator
from app.subtitle_generator import SubtitleGenerator
from app.video_builder import VideoBuilder
from app.utils import timestamp


def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(PROJECT_ROOT / "content" / "luna_factory.log"),
        ],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YAWatch Luna Stories — générateur de Shorts")
    parser.add_argument(
        "--type",
        choices=["emotionnelle", "mysterieuse", "inquietante", "protection", "philosophique"],
        default=None,
        help="Type d'histoire à générer (défaut: aléatoire)",
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=1,
        metavar="N",
        help="Nombre d'histoires à générer",
    )
    parser.add_argument("--verbose", action="store_true", help="Logs détaillés")
    parser.add_argument("--status", action="store_true", help="Afficher l'état de l'univers et quitter")
    return parser.parse_args()


def run_pipeline(config: ConfigLoader, lore: LoreManager, story_type: str = None) -> dict:
    logger = logging.getLogger(__name__)

    # Chemins
    stories_dir = config.get_path("paths.stories_dir")
    scripts_dir = config.get_path("paths.scripts_dir")
    audio_dir = config.get_path("paths.audio_dir")
    subtitles_dir = config.get_path("paths.subtitles_dir")
    images_dir = config.get_path("paths.images_dir")
    videos_dir = config.get_path("paths.videos_dir")

    # Génération histoire
    story_gen = StoryGenerator(lore)
    story = story_gen.generate(story_type)
    story_gen.save(story, stories_dir)

    # Script
    script_gen = ScriptGenerator(duration=config.get("content.script_duration", 35))
    script = script_gen.generate(story)
    script_path = script_gen.save(script, story["id"], scripts_dir)

    # Prompts images
    img_gen = ImagePromptGenerator()
    prompts = img_gen.generate_for_story(story)
    img_gen.save(prompts, story["id"], images_dir)

    # Voix
    voice_gen = VoiceGenerator(openai_key=config.openai_key)
    audio_path = audio_dir / f"luna_{story['id']}.mp3"
    voice_gen.text_to_speech(script, audio_path)

    # Sous-titres
    sub_gen = SubtitleGenerator()
    sub_path = sub_gen.generate(script, story["id"], subtitles_dir)

    # Vidéo (manifest si pas d'images réelles)
    video_builder = VideoBuilder()
    video_path = video_builder.build(
        story_id=story["id"],
        image_paths=[],  # sera rempli quand les images seront générées
        audio_path=audio_path,
        subtitles_path=sub_path,
        output_dir=videos_dir,
    )

    # Enregistrement dans le lore APRÈS la génération
    lore.record_episode(story["type"])

    logger.info("Pipeline terminé — ep.%d [%s]", story["episode_number"], story["title"])

    return {
        "story": story,
        "script": script_path,
        "audio": audio_path,
        "subtitles": sub_path,
        "video": video_path,
        "image_prompts": images_dir / f"prompts_{story['id']}.json",
    }


def main():
    args = parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    print("\n🧸  YAWatch Luna Stories — Usine narrative IA")
    print("=" * 55)

    config = ConfigLoader()
    lore_dir = config.get_path("paths.lore_dir")
    lore = LoreManager(lore_dir)
    char_mgr = CharacterManager(lore_dir)
    char_mgr.save()  # persiste les descriptions canoniques

    if args.status:
        print("\n📊 État de l'univers YAWatch-Luna:")
        print(lore.summary())
        sys.exit(0)

    results = []
    for i in range(args.batch):
        if args.batch > 1:
            print(f"\n--- Génération {i + 1}/{args.batch} ---")
        result = run_pipeline(config, lore, story_type=args.type)
        results.append(result)

        story = result["story"]
        print(f"\n✅ Épisode {story['episode_number']} prêt")
        print(f"   Titre    : {story['title']}")
        print(f"   Type     : {story['type']}")
        print(f"   Arc      : {story['arc']}")
        print(f"   Mystère  : {story['mystery_level']}/10")
        print(f"   Script   : {result['script'].name}")
        print(f"   Prompts  : {result['image_prompts'].name}")

    print(f"\n📊 Univers mis à jour:")
    print(lore.summary())

    print("\n💡 Prochaines étapes:")
    print("   1. Générer les images avec les prompts via Stable Diffusion/DALL-E")
    print("   2. Relancer avec --batch 5 pour produire une semaine de contenu")
    print("   3. Assembler les vidéos (FFmpeg hint dans les manifests)")


if __name__ == "__main__":
    main()
