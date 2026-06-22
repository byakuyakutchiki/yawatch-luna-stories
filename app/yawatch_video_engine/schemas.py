from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class SoundNeed(BaseModel):
    mode: Literal["silence", "ambiance", "bruitage", "voix_off", "dialogue"] = "silence"
    ambience_description: str | None = None
    foley: list[str] = Field(default_factory=list)
    voice_off_text: str | None = None
    dialogue_text: str | None = None


class GenerateShotRequest(BaseModel):
    project: str = "YAWatch-LUNA"
    episode_id: str | None = None
    shot_id: str = Field(..., min_length=1)
    character_reference_image: str = Field(..., description="Canonical character image path or URL")
    decor_image: str | None = None
    decor_description: str | None = None
    dramatic_intention: str = Field(..., min_length=5)
    shot_type: Literal["gros_plan", "plan_poitrine", "plan_large", "deplacement", "interaction_objet"]
    duration_sec: float = Field(5.0, ge=2.0, le=12.0)
    camera_motion: Literal[
        "static_hold",
        "slow_push_in",
        "slow_pull_back",
        "pan_left",
        "pan_right",
        "handheld_subtle",
        "dolly_lateral",
    ] = "slow_push_in"
    emotion: str = "contained tension"
    sound_need: SoundNeed = Field(default_factory=SoundNeed)
    engine_preference: Literal["mock", "wan21", "framepack", "pose_to_video", "auto"] = "mock"
    pose_reference: str | None = None
    object_interaction: dict[str, Any] | None = None
    continuity_notes: list[str] = Field(default_factory=list)
    fps: int = Field(24, ge=12, le=30)


class GenerateShotResponse(BaseModel):
    run_id: str
    status: str
    run_dir: str
    mp4_final: str | None
    preview_png: str | None
    metadata_json: str
    quality_review_json: str
    artistic_score: dict[str, Any]
    logs_techniques: list[str]
    production_folder_reusable: bool
