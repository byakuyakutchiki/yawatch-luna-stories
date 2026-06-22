"""Tests du MotionDirector — préparation de VideoJob pilotée par les bibliothèques.

Vérifie la gouvernance : bibliothèques → profil → VideoJob, sans génération ni validation.
"""

import json
import re
from pathlib import Path

import pytest

from app.motion_director import MotionDirector, TargetPaths, LibrariesNotAvailable, REQUIRED_LIBRARIES
from app.motion_director.director import _PROFILES_PATH, _PLANS_PATH


@pytest.fixture
def director():
    return MotionDirector(strict=True)


@pytest.fixture
def target():
    return TargetPaths(
        sources_dir=r"C:\Users\saint\Desktop\PONT_LINUX_WINDOWS\sources",
        deposit_dir=r"C:\Users\saint\Desktop\PONT_LINUX_WINDOWS\resultats\clips_yawatch",
    )


# ── Gouvernance : la connaissance d'abord ──────────────────────────────────

def test_required_libraries_exist():
    """Toutes les bibliothèques requises par le MotionDirector doivent exister."""
    missing = [p.name for p in REQUIRED_LIBRARIES if not p.exists()]
    assert not missing, f"Bibliothèques manquantes : {missing}"


def test_director_loads_libraries(director):
    assert director.libraries_loaded is True


# ── Cohérence doc ↔ profils machine ────────────────────────────────────────

def test_profiles_match_documented_types():
    """Les profils JSON couvrent exactement les types documentés dans MOTION_CONTROL_RULES.md."""
    data = json.loads(_PROFILES_PATH.read_text(encoding="utf-8"))
    profile_types = set(data["profiles"].keys())
    expected = {"establishing", "portrait_adult", "portrait_child", "hand_object", "macro_object"}
    assert profile_types == expected


def test_profiles_referenced_in_doc():
    """Chaque type de profil doit apparaître dans le document source (anti-dérive)."""
    doc = (Path(__file__).resolve().parent.parent
           / "docs" / "AI_VIDEO_ENGINE_KNOWLEDGE" / "MOTION_CONTROL_RULES.md").read_text(encoding="utf-8")
    data = json.loads(_PROFILES_PATH.read_text(encoding="utf-8"))
    for plan_type in data["profiles"]:
        assert plan_type in doc, f"Type '{plan_type}' absent du document MOTION_CONTROL_RULES.md"


def test_child_profile_more_conservative_than_adult():
    """Règle métier : l'enfant est plus fragile → denoise plus bas, IPAdapter plus fort."""
    data = json.loads(_PROFILES_PATH.read_text(encoding="utf-8"))["profiles"]
    assert data["portrait_child"]["denoise"] <= data["portrait_adult"]["denoise"]
    assert data["portrait_child"]["ipadapter_weight"] >= data["portrait_adult"]["ipadapter_weight"]


def test_establishing_has_no_ipadapter():
    """Un décor sans personnage ne doit pas activer l'IPAdapter."""
    data = json.loads(_PROFILES_PATH.read_text(encoding="utf-8"))["profiles"]
    assert data["establishing"]["ipadapter_weight"] == 0.0


# ── Préparation de VideoJob ────────────────────────────────────────────────

def test_all_nine_teaser_plans_present(director):
    assert director.available_plans() == [f"plan0{i}" for i in range(1, 10)]


def test_prepare_job_uses_profile_values(director, target):
    """Le job hérite des valeurs du profil (pas de réglage à la main)."""
    job = director.prepare_job("plan06", target)
    # Nouveau teaser Luna-only : plan06 = hand_object, car Luna interagit avec le cadre/photo.
    assert job.denoise == 0.45
    assert job.cfg == 5.0
    assert job.steps == 16
    assert job.use_ipadapter is True
    assert job.ipadapter_weight == 0.5


def test_prepare_job_character_plan_enables_ipadapter(director, target):
    job = director.prepare_job("plan02", target)
    assert job.use_ipadapter is True
    assert job.ipadapter_image == job.image_path


def test_prepare_job_luna_only_enables_ipadapter(director, target):
    """Nouveau teaser : les 9 plans sont Luna adulte, donc IPAdapter actif."""
    job = director.prepare_job("plan01", target)
    assert job.character == "luna_adulte"
    assert job.use_ipadapter is True
    assert job.ipadapter_image == job.image_path


def test_prepare_job_output_names_match_quality_gate(director, target):
    """Les noms de sortie doivent correspondre à ce que le Quality Gate attend."""
    for index in range(1, 10):
        plan_id = f"plan{index:02d}"
        assert director.prepare_job(plan_id, target).output_name == f"{plan_id}.mp4"


def test_prepare_job_image_path_is_windows_target(director, target):
    job = director.prepare_job("plan02", target)
    assert job.image_path.startswith(r"C:\Users\saint")
    assert job.image_path.endswith(".png")


def test_prepare_job_carries_governance_traceability(director, target):
    job = director.prepare_job("plan09", target)
    assert job.plan_id == "plan09"
    assert job.plan_type == "portrait_adult"
    assert job.character == "luna_adulte"


def test_prepare_unknown_plan_raises(director, target):
    with pytest.raises(KeyError):
        director.prepare_job("plan99", target)


def test_director_does_not_validate_or_generate(director):
    """Gouvernance : le MotionDirector n'expose ni validate() ni generate()."""
    assert not hasattr(director, "validate")
    assert not hasattr(director, "generate")


# ── Workflow IPAdapter ─────────────────────────────────────────────────────

def test_workflow_without_ipadapter_is_proven_plan02_graph():
    """use_ipadapter=False → graphe strictement identique au chemin prouvé (pas de nœud 12/13)."""
    from app.i2v_engine.comfyui_backend import build_workflow, VideoJob
    job = VideoJob(output_name="x.mp4", deposit_dir="d", image_path="i.png",
                   prompt_positive="p", prompt_negative="n", use_ipadapter=False)
    graph = build_workflow(job, "img.png")
    assert "12" not in graph and "13" not in graph
    assert graph["8"]["inputs"]["model"] == ["1", 0]


def test_workflow_with_ipadapter_inserts_nodes():
    """use_ipadapter=True → nœuds IPAdapter insérés et branchés avant AnimateDiff."""
    from app.i2v_engine.comfyui_backend import build_workflow, VideoJob
    job = VideoJob(output_name="x.mp4", deposit_dir="d", image_path="i.png",
                   prompt_positive="p", prompt_negative="n",
                   use_ipadapter=True, ipadapter_weight=0.75)
    graph = build_workflow(job, "img.png")
    assert graph["12"]["class_type"] == "IPAdapterUnifiedLoader"
    assert graph["13"]["class_type"] == "IPAdapter"
    # AnimateDiff prend le MODEL enrichi par l'IPAdapter
    assert graph["8"]["inputs"]["model"] == ["13", 0]
    assert graph["13"]["inputs"]["weight"] == 0.75
