from __future__ import annotations

from typing import Any


def parse_scene(request: dict[str, Any]) -> dict[str, Any]:
    """Normalize human intent into a scene description.

    This module does not generate pixels. It protects the director's intent so
    downstream engines receive narrative context instead of a vague prompt.
    """

    decor_image = request.get("decor_image")
    decor_description = request.get("decor_description") or ""
    dramatic_intention = request.get("dramatic_intention") or ""
    emotion = request.get("emotion") or "contained"

    if decor_image:
        decor_source_type = "image_reference"
    elif decor_description:
        decor_source_type = "text_description"
    else:
        decor_source_type = "missing"

    tone_tags = []
    lowered = f"{dramatic_intention} {emotion} {decor_description}".lower()
    for tag in ["tension", "mystery", "fear", "guilt", "control", "silence", "revelation"]:
        if tag in lowered:
            tone_tags.append(tag)
    if not tone_tags:
        tone_tags.append("psychological_thriller")

    return {
        "project": request.get("project", "YAWatch-LUNA"),
        "episode_id": request.get("episode_id"),
        "shot_id": request.get("shot_id"),
        "character_reference_image": request.get("character_reference_image"),
        "decor_image": decor_image,
        "decor_description": decor_description,
        "decor_source_type": decor_source_type,
        "dramatic_intention": dramatic_intention,
        "emotion": emotion,
        "tone_tags": tone_tags,
        "continuity_notes": request.get("continuity_notes", []),
        "object_interaction": request.get("object_interaction"),
    }
