from __future__ import annotations

from typing import Any


def _score_bool(condition: bool, points: int) -> int:
    return points if condition else 0


def review_quality(
    request: dict[str, Any],
    scene: dict[str, Any],
    shot_plan: dict[str, Any],
    motion_plan: dict[str, Any],
    render_result: dict[str, Any],
) -> dict[str, Any]:
    """Score planning quality first; rendered video metrics can be added later."""

    axes = {
        "presence_humaine": 0,
        "intention_dramatique": 0,
        "mouvement_corps": 0,
        "profondeur_decor": 0,
        "tension_cinematique": 0,
        "stabilite_technique": 0,
    }
    axes["presence_humaine"] += _score_bool(bool(request.get("character_reference_image")), 12)
    axes["presence_humaine"] += _score_bool("subject_motion" in motion_plan, 6)
    axes["intention_dramatique"] += _score_bool(bool(scene.get("dramatic_intention")), 16)
    axes["intention_dramatique"] += _score_bool(bool(scene.get("emotion")), 4)
    axes["mouvement_corps"] += _score_bool(bool(motion_plan.get("subject_motion")), 10)
    axes["mouvement_corps"] += _score_bool(bool(motion_plan.get("pose_control")), 6)
    axes["profondeur_decor"] += _score_bool(bool(scene.get("decor_image") or scene.get("decor_description")), 12)
    axes["tension_cinematique"] += _score_bool("psychological_thriller" in scene.get("tone_tags", []) or bool(scene.get("tone_tags")), 12)
    axes["tension_cinematique"] += _score_bool(shot_plan.get("duration_sec", 0) >= 4, 4)
    axes["stabilite_technique"] += _score_bool(render_result.get("export_status") == "ok", 10)
    axes["stabilite_technique"] += _score_bool(motion_plan["technical_targets"]["face_identity_ssim_min"] >= 0.85, 8)

    if render_result.get("is_mock_video"):
        total = min(72, sum(axes.values()))
        verdict = "MVP_STRUCTURE_ONLY"
    else:
        total = min(100, sum(axes.values()))
        if total >= 85:
            verdict = "READY_FOR_HUMAN_REVIEW"
        elif total >= 70:
            verdict = "NEEDS_ARTISTIC_REVIEW"
        else:
            verdict = "NOT_READY"

    return {
        "artistic_score": total,
        "axis_scores": axes,
        "verdict": verdict,
        "human_review_required": True,
        "kling_target_lessons_applied": [
            "evaluate human presence, not only SSIM",
            "track body/hair/shoulder motion, not only face",
            "preserve low flicker while increasing scene life",
            "prefer two-stage motion plus identity restoration when needed",
        ],
        "automatic_limits": [
            "mock mode cannot prove face identity",
            "mock mode cannot prove real body motion",
            "final validation belongs to Ludovic",
        ],
    }
