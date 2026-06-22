from __future__ import annotations

from pathlib import Path
from typing import Any

from .camera_director import plan_camera
from .i2v_adapter import select_adapter
from .motion_engine import build_motion_plan
from .pose_control import plan_pose
from .quality_review import review_quality
from .run_manager import append_log, as_posix, create_run_dir, utc_now_iso, write_json
from .scene_parser import parse_scene
from .shot_planner import plan_shot
from .sound_layer import plan_sound


def generate_shot(request: dict[str, Any], run_root: str | Path | None = None) -> dict[str, Any]:
    run_id, run_dir = create_run_dir(request.get("shot_id"), run_root=run_root)
    append_log(run_dir, f"created run {run_id}")
    write_json(run_dir / "input.json", request)

    scene = parse_scene(request)
    shot_plan = plan_shot(request, scene)
    camera_plan = plan_camera(request, shot_plan)
    pose_plan = plan_pose(request, shot_plan)
    motion_plan = build_motion_plan(request, shot_plan, camera_plan, pose_plan)
    sound_plan = plan_sound(request, scene)

    write_json(run_dir / "scene_parse.json", scene)
    write_json(run_dir / "shot_plan.json", shot_plan)
    write_json(run_dir / "camera_plan.json", camera_plan)
    write_json(run_dir / "pose_plan.json", pose_plan)
    write_json(run_dir / "motion_plan.json", motion_plan)
    write_json(run_dir / "sound_plan.json", sound_plan)

    adapter = select_adapter(request.get("engine_preference"))
    append_log(run_dir, f"selected adapter {adapter.name}")
    render_result = adapter.generate(run_dir, request, shot_plan, motion_plan)
    write_json(run_dir / "render_result.json", render_result)

    quality = review_quality(request, scene, shot_plan, motion_plan, render_result)
    quality_path = write_json(run_dir / "quality_review.json", quality)

    metadata = {
        "run_id": run_id,
        "created_at": utc_now_iso(),
        "project": scene["project"],
        "episode_id": request.get("episode_id"),
        "shot_id": request.get("shot_id"),
        "status": render_result.get("status"),
        "adapter": render_result.get("adapter"),
        "mp4_final": render_result.get("mp4_path"),
        "preview_png": render_result.get("preview_png"),
        "metadata_json": as_posix(run_dir / "metadata.json"),
        "quality_review_json": as_posix(quality_path),
        "run_dir": as_posix(run_dir),
        "artistic_score": quality["artistic_score"],
        "quality_verdict": quality["verdict"],
        "human_review_required": True,
    }
    metadata_path = write_json(run_dir / "metadata.json", metadata)
    append_log(run_dir, f"finished run {run_id} with verdict {quality['verdict']}")

    return {
        "run_id": run_id,
        "status": metadata["status"],
        "run_dir": metadata["run_dir"],
        "mp4_final": metadata["mp4_final"],
        "preview_png": metadata["preview_png"],
        "metadata_json": as_posix(metadata_path),
        "quality_review_json": metadata["quality_review_json"],
        "artistic_score": quality,
        "logs_techniques": [as_posix(run_dir / "logs" / "technical.log")],
        "production_folder_reusable": True,
    }
