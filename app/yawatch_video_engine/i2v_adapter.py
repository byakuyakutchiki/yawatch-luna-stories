from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

from .montage_exporter import export_montage


class I2VAdapter(Protocol):
    name: str

    def generate(
        self,
        run_dir: Path,
        request: dict[str, Any],
        shot_plan: dict[str, Any],
        motion_plan: dict[str, Any],
    ) -> dict[str, Any]:
        ...


class MockCinematicAdapter:
    name = "mock_cinematic_ffmpeg"

    def generate(
        self,
        run_dir: Path,
        request: dict[str, Any],
        shot_plan: dict[str, Any],
        motion_plan: dict[str, Any],
    ) -> dict[str, Any]:
        export = export_montage(run_dir, request, shot_plan, motion_plan)
        return {
            "adapter": self.name,
            "status": "mock_generated",
            "engine_role": "local proof of API architecture, not artistic validation",
            **export,
        }


class WanAdapter:
    name = "wan21"

    def generate(self, run_dir: Path, request: dict[str, Any], shot_plan: dict[str, Any], motion_plan: dict[str, Any]) -> dict[str, Any]:
        return {
            "adapter": self.name,
            "status": "planned_not_executed",
            "mp4_path": None,
            "preview_png": None,
            "required_next_step": "connect this adapter to the existing Wan GGUF/ComfyUI workflow runner",
            "locked_inputs": {
                "character_reference_image": request.get("character_reference_image"),
                "decor_image": request.get("decor_image"),
                "prompt": motion_plan["target_artistic_axes"],
            },
        }


class FramePackAdapter:
    name = "framepack"

    def generate(self, run_dir: Path, request: dict[str, Any], shot_plan: dict[str, Any], motion_plan: dict[str, Any]) -> dict[str, Any]:
        return {
            "adapter": self.name,
            "status": "planned_not_executed",
            "mp4_path": None,
            "preview_png": None,
            "required_next_step": "connect this adapter to FramePack runner on RunPod or local ComfyUI",
            "locked_inputs": {
                "character_reference_image": request.get("character_reference_image"),
                "duration_sec": motion_plan["duration_sec"],
                "camera_motion": motion_plan["camera_motion"],
            },
        }


class PoseToVideoAdapter:
    name = "pose_to_video_future"

    def generate(self, run_dir: Path, request: dict[str, Any], shot_plan: dict[str, Any], motion_plan: dict[str, Any]) -> dict[str, Any]:
        return {
            "adapter": self.name,
            "status": "planned_not_executed",
            "mp4_path": None,
            "preview_png": None,
            "required_next_step": "add pose/depth/control workflow before I2V for full-body motion",
            "locked_inputs": {
                "pose_reference": request.get("pose_reference"),
                "shot_type": shot_plan["shot_type"],
            },
        }


def select_adapter(engine_preference: str | None) -> I2VAdapter:
    key = (engine_preference or "mock").lower()
    if key in {"wan", "wan21", "wan2.1"}:
        return WanAdapter()
    if key in {"framepack", "frame_pack"}:
        return FramePackAdapter()
    if key in {"pose", "pose_to_video"}:
        return PoseToVideoAdapter()
    return MockCinematicAdapter()
