import json
from pathlib import Path

from app.yawatch_video_engine.engine import generate_shot


def _request():
    return {
        "project": "YAWatch-LUNA",
        "episode_id": "S01E00",
        "shot_id": "unit_luna_kling_like",
        "character_reference_image": "assets/luna.png",
        "decor_description": "bureau YAWatch de nuit a La Defense",
        "dramatic_intention": "Luna garde le controle alors qu'une verite familiale revient.",
        "shot_type": "plan_poitrine",
        "duration_sec": 5,
        "camera_motion": "slow_push_in",
        "emotion": "contained tension",
        "sound_need": {"mode": "ambiance"},
        "engine_preference": "mock",
    }


def test_generate_shot_creates_reusable_run_folder(tmp_path):
    result = generate_shot(_request(), run_root=tmp_path)

    run_dir = Path(result["run_dir"])
    assert run_dir.exists()
    assert result["production_folder_reusable"] is True
    assert (run_dir / "input.json").exists()
    assert (run_dir / "shot_plan.json").exists()
    assert (run_dir / "motion_plan.json").exists()
    assert (run_dir / "quality_review.json").exists()
    assert (run_dir / "metadata.json").exists()
    assert (run_dir / "logs" / "technical.log").exists()


def test_generate_shot_preserves_narrative_intent(tmp_path):
    result = generate_shot(_request(), run_root=tmp_path)
    run_dir = Path(result["run_dir"])
    motion = json.loads((run_dir / "motion_plan.json").read_text(encoding="utf-8"))
    quality = json.loads((run_dir / "quality_review.json").read_text(encoding="utf-8"))

    assert motion["camera_motion"] == "slow_push_in"
    assert "presence_humaine" in motion["target_artistic_axes"]
    assert "tension_cinematique" in motion["target_artistic_axes"]
    assert quality["human_review_required"] is True
    assert "kling_target_lessons_applied" in quality
