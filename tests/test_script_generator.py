import pytest
from app.lore_manager import LoreManager
from app.story_generator import StoryGenerator
from app.script_generator import ScriptGenerator


def _make_story(tmp_path, story_type=None):
    lore = LoreManager(tmp_path)
    gen = StoryGenerator(lore)
    return gen.generate(story_type)


def test_script_has_all_sections(tmp_path):
    story = _make_story(tmp_path)
    script_gen = ScriptGenerator()
    script = script_gen.generate(story)
    for section in ["HOOK:", "STORY:", "TWIST:", "CTA:"]:
        assert section in script


def test_all_story_types_generate(tmp_path):
    from app.story_generator import STORY_TYPES
    script_gen = ScriptGenerator()
    for stype in STORY_TYPES:
        story = _make_story(tmp_path, stype)
        script = script_gen.generate(story)
        assert "HOOK:" in script
        assert len(script) > 100


def test_script_save(tmp_path):
    story = _make_story(tmp_path)
    script_gen = ScriptGenerator()
    script = script_gen.generate(story)
    path = script_gen.save(script, story["id"], tmp_path)
    assert path.exists()
    assert path.read_text(encoding="utf-8") == script
