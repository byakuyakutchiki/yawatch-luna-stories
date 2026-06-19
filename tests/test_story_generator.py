import pytest
from app.lore_manager import LoreManager
from app.story_generator import StoryGenerator, STORY_TYPES


def test_generate_returns_all_fields(tmp_path):
    lore = LoreManager(tmp_path)
    gen = StoryGenerator(lore)
    story = gen.generate()
    for field in ["id", "type", "title", "hook", "context", "characters", "arc", "episode_number"]:
        assert field in story


def test_generate_valid_type(tmp_path):
    lore = LoreManager(tmp_path)
    gen = StoryGenerator(lore)
    story = gen.generate()
    assert story["type"] in STORY_TYPES


def test_generate_specific_type(tmp_path):
    lore = LoreManager(tmp_path)
    gen = StoryGenerator(lore)
    story = gen.generate("mysterieuse")
    assert story["type"] == "mysterieuse"


def test_generate_invalid_type_uses_random(tmp_path):
    lore = LoreManager(tmp_path)
    gen = StoryGenerator(lore)
    story = gen.generate("type_inexistant")
    assert story["type"] in STORY_TYPES


def test_luna_doll_in_emotionnelle_stories(tmp_path):
    # Luna_Doll n'apparaît que dans le type "emotionnelle" — pas dans tous les types.
    lore = LoreManager(tmp_path)
    gen = StoryGenerator(lore)
    for _ in range(5):
        story = gen.generate("emotionnelle")
        assert "Luna_Doll" in story["characters"], (
            "Le type 'emotionnelle' doit toujours inclure Luna_Doll."
        )

def test_luna_doll_not_in_all_types(tmp_path):
    # Les types non émotionnels n'incluent pas nécessairement Luna_Doll.
    lore = LoreManager(tmp_path)
    gen = StoryGenerator(lore)
    non_emotional_types = ["mysterieuse", "inquietante", "protection", "philosophique"]
    for story_type in non_emotional_types:
        story = gen.generate(story_type)
        assert "Luna_Doll" not in story["characters"], (
            f"Le type '{story_type}' ne doit pas inclure Luna_Doll "
            "(personnage réservé aux épisodes émotionnels)."
        )


def test_save_creates_file(tmp_path):
    lore = LoreManager(tmp_path)
    gen = StoryGenerator(lore)
    story = gen.generate()
    path = gen.save(story, tmp_path)
    assert path.exists()
    assert path.suffix == ".json"
