from __future__ import annotations

from typing import Any


def plan_sound(request: dict[str, Any], scene: dict[str, Any]) -> dict[str, Any]:
    sound_need = request.get("sound_need") or {}
    if isinstance(sound_need, str):
        sound_need = {"mode": sound_need}

    mode = sound_need.get("mode", "silence")
    return {
        "mode": mode,
        "ambience_description": sound_need.get("ambience_description"),
        "foley": sound_need.get("foley", []),
        "voice_off_text": sound_need.get("voice_off_text"),
        "dialogue_text": sound_need.get("dialogue_text"),
        "rules": [
            "silence is allowed when it increases tension",
            "sound must not explain what the image already says",
            "voice off should be rare, short, and emotionally loaded",
            "foley must support object interactions when visible",
        ],
        "scene_tone_tags": scene.get("tone_tags", []),
    }
