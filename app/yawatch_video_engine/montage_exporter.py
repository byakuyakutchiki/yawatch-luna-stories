from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover - optional runtime dependency
    Image = None
    ImageDraw = None


def create_preview(run_dir: Path, request: dict[str, Any], shot_plan: dict[str, Any]) -> Path:
    preview_path = run_dir / "preview.png"
    if Image is None:
        preview_path.write_text("Pillow unavailable: preview not rendered.\n", encoding="utf-8")
        return preview_path

    image = Image.new("RGB", (1080, 1920), (12, 14, 18))
    draw = ImageDraw.Draw(image)
    lines = [
        "YAWatch Video Engine",
        f"shot: {request.get('shot_id', 'unnamed')}",
        f"type: {shot_plan.get('shot_type')}",
        f"emotion: {request.get('emotion', 'contained')}",
        f"duration: {shot_plan.get('duration_sec')}s",
        "MVP preview - replace with I2V output",
    ]
    y = 760
    for line in lines:
        draw.text((80, y), line, fill=(220, 225, 230))
        y += 58
    image.save(preview_path)
    return preview_path


def create_mock_mp4(run_dir: Path, preview_path: Path, duration_sec: float, fps: int) -> tuple[Path | None, str]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return None, "ffmpeg_not_found"

    output_path = run_dir / "final.mp4"
    cmd = [
        ffmpeg,
        "-y",
        "-loop",
        "1",
        "-i",
        str(preview_path),
        "-t",
        str(duration_sec),
        "-r",
        str(fps),
        "-vf",
        "scale=1080:1920,format=yuv420p",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return None, completed.stderr[-1200:] or "ffmpeg_failed"
    return output_path, "ok"


def export_montage(
    run_dir: Path,
    request: dict[str, Any],
    shot_plan: dict[str, Any],
    motion_plan: dict[str, Any],
) -> dict[str, Any]:
    preview_path = create_preview(run_dir, request, shot_plan)
    mp4_path, status = create_mock_mp4(
        run_dir=run_dir,
        preview_path=preview_path,
        duration_sec=float(motion_plan["duration_sec"]),
        fps=int(motion_plan["fps"]),
    )
    return {
        "preview_png": str(preview_path.resolve()),
        "mp4_path": str(mp4_path.resolve()) if mp4_path else None,
        "export_status": status,
        "is_mock_video": True,
        "notes": [
            "This MVP export proves API/run-folder plumbing.",
            "Replace mock export with WAN/FramePack/pose-to-video adapter output.",
        ],
    }
