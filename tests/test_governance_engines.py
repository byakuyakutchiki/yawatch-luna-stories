"""Tests de la gouvernance multi-moteurs — sceau de job + dispatcher.

Vérifie que :
  - le backend REFUSE tout job non préparé par le rôle métier (ou altéré) ;
  - le job_hash scelle réellement les paramètres verrouillés ;
  - le MotionDirector scelle les jobs qu'il prépare ;
  - build_workflow route vers la bonne branche moteur (graphes prouvés) ;
  - le re-test Wan utilise le chargeur NATIF (pas GGUF).
"""

import pytest

from app.i2v_engine.comfyui_backend import (
    VideoJob,
    build_workflow,
    compute_job_hash,
    validate_job_governance,
    GovernanceError,
    GOVERNED_SOURCE,
    DEFAULT_LOCKED_PARAMETERS,
    ENGINE_ANIMATEDIFF,
    ENGINE_FRAMEPACK,
    ENGINE_WAN21,
)
from app.motion_director import MotionDirector, TargetPaths


@pytest.fixture
def director():
    return MotionDirector(strict=True)


@pytest.fixture
def target():
    return TargetPaths(
        sources_dir=r"C:\Users\saint\Desktop\PONT_LINUX_WINDOWS\sources",
        deposit_dir=r"C:\Users\saint\Desktop\PONT_LINUX_WINDOWS\resultats\clips_yawatch",
    )


def _sealed(**overrides) -> VideoJob:
    """VideoJob minimal scellé comme le ferait le MotionDirector."""
    job = VideoJob(
        output_name="x.mp4", deposit_dir="d", image_path="i.png",
        prompt_positive="p", prompt_negative="n",
        source_generatrice=GOVERNED_SOURCE,
        locked_parameters=tuple(DEFAULT_LOCKED_PARAMETERS),
        **overrides,
    )
    job.job_hash = compute_job_hash(job)
    return job


# ── Sceau de gouvernance ────────────────────────────────────────────────────

def test_sealed_job_passes_validation():
    validate_job_governance(_sealed())  # ne lève pas


def test_hand_authored_job_is_refused():
    """Un job sans source ni hash (écrit à la main) est refusé."""
    job = VideoJob(output_name="x.mp4", deposit_dir="d", image_path="i.png",
                   prompt_positive="p", prompt_negative="n")
    with pytest.raises(GovernanceError):
        validate_job_governance(job)


def test_wrong_source_is_refused():
    job = _sealed()
    job.source_generatrice = "humain_qui_bidouille"
    with pytest.raises(GovernanceError):
        validate_job_governance(job)


def test_tampered_locked_parameter_breaks_hash():
    """Modifier un paramètre verrouillé après préparation casse le hash."""
    job = _sealed()
    job.cfg = 99.0  # altération manuelle d'un paramètre scellé
    with pytest.raises(GovernanceError):
        validate_job_governance(job)


def test_tampered_prompt_breaks_hash():
    job = _sealed()
    job.prompt_positive = "prompt injecté à la main"
    with pytest.raises(GovernanceError):
        validate_job_governance(job)


def test_unknown_engine_is_refused():
    with pytest.raises(GovernanceError):
        validate_job_governance(_sealed(engine="kling"))


def test_hash_is_deterministic():
    assert compute_job_hash(_sealed()) == compute_job_hash(_sealed())


def test_engine_params_are_sealed():
    """engine_params fait partie du hash : l'altérer casse la validation."""
    job = _sealed(engine=ENGINE_WAN21, engine_params={"steps": 12})
    validate_job_governance(job)
    job.engine_params["steps"] = 4
    with pytest.raises(GovernanceError):
        validate_job_governance(job)


# ── MotionDirector scelle ses jobs ──────────────────────────────────────────

def test_director_seals_prepared_job(director, target):
    job = director.prepare_job("plan02", target)
    assert job.source_generatrice == GOVERNED_SOURCE
    assert job.job_hash
    validate_job_governance(job)  # le job du rôle métier passe la gouvernance


def test_director_default_engine_is_animatediff(director, target):
    job = director.prepare_job("plan02", target)
    assert job.engine == ENGINE_ANIMATEDIFF
    assert job.engine_params == {}


def test_director_rejects_unknown_engine(director, target):
    with pytest.raises(ValueError):
        director.prepare_job("plan02", target, engine="kling")


def test_director_framepack_loads_engine_params(director, target):
    job = director.prepare_job("plan02", target, engine=ENGINE_FRAMEPACK)
    assert job.engine == ENGINE_FRAMEPACK
    assert job.engine_params["framepack_model"].startswith("FramePackI2V")
    validate_job_governance(job)


def test_director_wan_loads_engine_params(director, target):
    job = director.prepare_job("plan02", target, engine=ENGINE_WAN21)
    assert job.engine == ENGINE_WAN21
    assert job.engine_params["unet_name"].endswith(".safetensors")
    validate_job_governance(job)


# ── Dispatcher build_workflow ───────────────────────────────────────────────

def test_dispatch_framepack_graph():
    job = _sealed(engine=ENGINE_FRAMEPACK, engine_params={
        "framepack_model": "FramePackI2V_HY_fp8_e4m3fn.safetensors"})
    graph = build_workflow(job, "luna.png")
    class_types = {n["class_type"] for n in graph.values()}
    assert "LoadFramePackModel" in class_types
    assert "FramePackSampler" in class_types
    # prompts du job réellement injectés
    assert graph["9"]["inputs"]["text"] == "p"


def test_dispatch_wan_graph_is_native_not_gguf():
    """Le re-test Wan doit charger le modèle NATIF, jamais le GGUF quantifié."""
    job = _sealed(engine=ENGINE_WAN21, engine_params={
        "unet_name": "wan2.1_i2v_480p_14B_fp16.safetensors"})
    graph = build_workflow(job, "luna.png")
    class_types = {n["class_type"] for n in graph.values()}
    assert "UNETLoader" in class_types
    assert "UnetLoaderGGUF" not in class_types  # surtout pas le GGUF
    assert "WanImageToVideo" in class_types


def test_dispatch_animatediff_unchanged():
    """Le moteur par défaut reste le graphe AnimateDiff prouvé."""
    job = _sealed(engine=ENGINE_ANIMATEDIFF)
    graph = build_workflow(job, "luna.png")
    class_types = {n["class_type"] for n in graph.values()}
    assert "ADE_AnimateDiffLoaderGen1" in class_types
