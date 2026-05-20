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


def test_luna_doll_in_most_stories(tmp_path):
    lore = LoreManager(tmp_path)
    gen = StoryGenerator(lore)
    for _ in range(10):
        story = gen.generate()
        assert "Luna_Doll" in story["characters"]


def test_save_creates_file(tmp_path):
    lore = LoreManager(tmp_path)
    gen = StoryGenerator(lore)
    story = gen.generate()
    path = gen.save(story, tmp_path)
    assert path.exists()
    assert path.suffix == ".json"
