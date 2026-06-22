from __future__ import annotations

from typing import Any


SHOT_GRAMMAR = {
    "gros_plan": {
        "composition": "face and eyes dominate the frame",
        "risk": "identity drift is highly visible",
        "priority": "face stability and emotional micro-expression",
    },
    "plan_poitrine": {
        "composition": "head, shoulders, hands, and object context",
        "risk": "hand deformation and frozen shoulders",
        "priority": "presence humaine, breath, hands, shoulders",
    },
    "plan_large": {
        "composition": "character placed inside readable decor depth",
        "risk": "character becomes too small for identity control",
        "priority": "decor depth, silhouette, camera geography",
    },
    "deplacement": {
        "composition": "body motion must remain legible across frames",
        "risk": "pose collapse, foot sliding, inconsistent body scale",
        "priority": "pose control before I2V",
    },
    "interaction_objet": {
        "composition": "hands, object, and face share narrative attention",
        "risk": "object morphing and finger fusion",
        "priority": "object continuity, hand anatomy, restrained motion",
    },
}


def plan_shot(request: dict[str, Any], scene: dict[str, Any]) -> dict[str, Any]:
    shot_type = request.get("shot_type") or "plan_poitrine"
    grammar = SHOT_GRAMMAR.get(shot_type, SHOT_GRAMMAR["plan_poitrine"])
    duration = float(request.get("duration_sec") or 5.0)
    duration = max(2.0, min(duration, 12.0))

    return {
        "shot_type": shot_type,
        "duration_sec": duration,
        "composition": grammar["composition"],
        "primary_risk": grammar["risk"],
        "director_priority": grammar["priority"],
        "dramatic_intention": scene["dramatic_intention"],
        "emotion": scene["emotion"],
        "must_feel": [
            "human presence",
            "clear intention",
            "cinematic tension",
            "decor depth",
            "YAWatch-LUNA continuity",
        ],
        "must_avoid": [
            "photo slideshow feeling",
            "random shaking",
            "face melting",
            "object morphing",
            "over-animated movement",
            "generic AI demo look",
        ],
    }
