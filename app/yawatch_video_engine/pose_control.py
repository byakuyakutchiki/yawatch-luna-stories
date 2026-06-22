from __future__ import annotations

from typing import Any


def plan_pose(request: dict[str, Any], shot_plan: dict[str, Any]) -> dict[str, Any]:
    shot_type = shot_plan["shot_type"]
    needs_pose = shot_type in {"deplacement", "plan_large"} or bool(request.get("pose_reference"))

    if shot_type == "interaction_objet":
        body_strategy = "lock torso, preserve hands and object relation"
    elif shot_type == "deplacement":
        body_strategy = "use pose-to-video or control sequence before I2V"
    elif shot_type == "plan_large":
        body_strategy = "preserve silhouette and scale inside decor"
    else:
        body_strategy = "subtle breathing and shoulder micro-motion only"

    return {
        "needs_pose_control": needs_pose,
        "pose_reference": request.get("pose_reference"),
        "body_strategy": body_strategy,
        "failure_modes": [
            "foot sliding",
            "arms changing length",
            "hands merging with object",
            "body scale changing across frames",
            "head drifting away from canonical identity",
        ],
        "future_hooks": [
            "ControlNet/OpenPose",
            "Depth control",
            "pose-to-video model",
            "face restoration after motion pass",
        ],
    }
