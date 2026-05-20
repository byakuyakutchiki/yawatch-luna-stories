import pytest
from app.visual_consistency_manager import VisualConsistencyManager


def test_luna_doll_dna_present():
    vcm = VisualConsistencyManager()
    dna = vcm.get_character_dna("Luna_Doll")
    assert "robe" in dna
    assert "violette" in dna["robe"]
    assert "interdit" in dna
    assert "robot" in dna["interdit"]


def test_validate_prompt_rejects_robot():
    vcm = VisualConsistencyManager()
    assert not vcm.validate_prompt("a cute robot doll with violet dress", "Luna_Doll")


def test_validate_prompt_accepts_valid():
    vcm = VisualConsistencyManager()
    assert vcm.validate_prompt("small handmade fabric doll, brown hair, violet dress", "Luna_Doll")


def test_negative_prompt_contains_robot():
    vcm = VisualConsistencyManager()
    neg = vcm.get_negative_prompt("Luna_Doll")
    assert "robot" in neg


def test_enforce_luna_doll_injects_dna():
    vcm = VisualConsistencyManager()
    result = vcm.enforce_luna_doll("a cute doll")
    assert "violette" in result
    assert "bruns" in result


def test_scene_context_includes_doll():
    vcm = VisualConsistencyManager()
    ctx = vcm.build_scene_context("emotionnelle", ["Luna_Doll"])
    assert "violet" in ctx.lower() or "violette" in ctx.lower()


def test_unknown_character_returns_empty():
    vcm = VisualConsistencyManager()
    dna = vcm.get_character_dna("Personnage_Inconnu")
    assert dna == {}
