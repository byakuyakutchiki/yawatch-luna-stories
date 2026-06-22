from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_RUN_ROOT = Path("content") / "video_engine_runs"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_slug(value: str | None, fallback: str = "shot") -> str:
    raw = value or fallback
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "_", raw.strip()).strip("_").lower()
    return slug or fallback


def create_run_dir(shot_id: str | None, run_root: str | Path | None = None) -> tuple[str, Path]:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"{timestamp}_{safe_slug(shot_id)}"
    base = Path(run_root) if run_root else DEFAULT_RUN_ROOT
    run_dir = base / run_id
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    return run_id, run_dir


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def append_log(run_dir: Path, message: str) -> None:
    log_path = run_dir / "logs" / "technical.log"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"[{utc_now_iso()}] {message}\n")


def as_posix(path: Path) -> str:
    return path.resolve().as_posix()
