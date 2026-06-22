from __future__ import annotations

from typing import Any


CAMERA_MOTIONS = {
    "static_hold": {"intensity": "low", "use": "emotional hold, minimal motion"},
    "slow_push_in": {"intensity": "low", "use": "growing suspicion or inner pressure"},
    "slow_pull_back": {"intensity": "low", "use": "loneliness, reveal of environment"},
    "pan_left": {"intensity": "medium", "use": "discovering off-screen context"},
    "pan_right": {"intensity": "medium", "use": "following attention shift"},
    "handheld_subtle": {"intensity": "medium", "use": "controlled instability, never shaky"},
    "dolly_lateral": {"intensity": "medium", "use": "premium movement in office or hallway"},
}


def plan_camera(request: dict[str, Any], shot_plan: dict[str, Any]) -> dict[str, Any]:
    requested = request.get("camera_motion") or "slow_push_in"
    if requested not in CAMERA_MOTIONS:
        requested = "slow_push_in"

    motion = CAMERA_MOTIONS[requested]
    max_camera_drift = 0.08 if shot_plan["shot_type"] in {"gros_plan", "interaction_objet"} else 0.14

    return {
        "camera_motion": requested,
        "intensity": motion["intensity"],
        "dramatic_use": motion["use"],
        "max_camera_drift_ratio": max_camera_drift,
        "rules": [
            "camera motion must support intention, not decorate the shot",
            "no abrupt zoom unless explicitly approved by human director",
            "close shots require identity-preserving low drift",
            "movement must be readable over 4-6 seconds",
        ],
    }
