from __future__ import annotations

from typing import Any


def build_motion_plan(
    request: dict[str, Any],
    shot_plan: dict[str, Any],
    camera_plan: dict[str, Any],
    pose_plan: dict[str, Any],
) -> dict[str, Any]:
    duration = shot_plan["duration_sec"]
    camera_motion = camera_plan["camera_motion"]
    emotion = shot_plan["emotion"]

    if "fear" in emotion.lower() or "tension" in emotion.lower():
        subject_motion = "controlled breathing, small eye movement, restrained shoulders"
    elif "surprise" in emotion.lower():
        subject_motion = "small head hesitation, eyes searching off-screen"
    else:
        subject_motion = "natural micro-movement without performance exaggeration"

    return {
        "duration_sec": duration,
        "fps": int(request.get("fps") or 24),
        "camera_motion": camera_motion,
        "subject_motion": subject_motion,
        "pose_control": pose_plan,
        "identity_strategy": {
            "primary": "preserve reference face and hair shape",
            "secondary": "restore or re-anchor face after motion pass when available",
            "no_silent_fallback": True,
        },
        "target_artistic_axes": {
            "presence_humaine": "visible breath, shoulders, eyes, hands when relevant",
            "intention": shot_plan["dramatic_intention"],
            "mouvement_corps": pose_plan["body_strategy"],
            "profondeur_decor": "background parallax or readable spatial layers",
            "tension_cinematique": "motion supports mystery, not spectacle",
        },
        "technical_targets": {
            "face_flicker_mean_abs_delta_max": 0.15,
            "face_identity_ssim_min": 0.85,
            "full_frame_flow_target_min": 0.20,
            "hair_or_shoulder_flow_target_min": 0.14,
        },
    }
