import pytest
from app.lore_manager import LoreManager


def test_initial_state(tmp_path):
    lore = LoreManager(tmp_path)
    assert lore.episode_count == 0
    assert lore.current_arc == "saison_1_la_question"
    assert lore.doll_mystery_level == 1


def test_record_episode_increments(tmp_path):
    lore = LoreManager(tmp_path)
    lore.record_episode("emotionnelle")
    assert lore.episode_count == 1


def test_mystery_level_increases_on_mystery_type(tmp_path):
    lore = LoreManager(tmp_path)
    initial = lore.doll_mystery_level
    lore.record_episode("mysterieuse")
    assert lore.doll_mystery_level == initial + 1


def test_mystery_level_capped_at_10(tmp_path):
    lore = LoreManager(tmp_path)
    lore.state["characters"]["Luna_Doll"]["mystery_level"] = 10
    lore.record_episode("mysterieuse")
    assert lore.doll_mystery_level == 10


def test_arc_progression(tmp_path):
    lore = LoreManager(tmp_path)
    # Avance jusqu'au seuil du 2e arc (épisode 10)
    for _ in range(10):
        lore.record_episode("emotionnelle")
    assert lore.current_arc == "saison_2_ombre_du_pere"


def test_secrets_revealed_by_episode_5(tmp_path):
    # Le lore a des secrets aux épisodes 3 et 5 → 2 secrets révélés après 5 épisodes.
    lore = LoreManager(tmp_path)
    for _ in range(5):
        lore.record_episode("emotionnelle")
    revealed = lore.state["revealed_secrets"]
    assert len(revealed) == 2
    episodes = {s["episode"] for s in revealed}
    assert 3 in episodes
    assert 5 in episodes


def test_get_next_story_prompt(tmp_path):
    lore = LoreManager(tmp_path)
    prompt = lore.get_next_story_prompt("emotionnelle")
    assert "hook" in prompt
    assert "context" in prompt


def test_persistence(tmp_path):
    lore1 = LoreManager(tmp_path)
    lore1.record_episode("mysterieuse")
    lore1.save()

    lore2 = LoreManager(tmp_path)
    assert lore2.episode_count == 1
    assert lore2.doll_mystery_level == 2


def test_get_next_secret(tmp_path):
    lore = LoreManager(tmp_path)
    secret = lore.get_next_secret()
    assert isinstance(secret, str)
    assert len(secret) > 10
