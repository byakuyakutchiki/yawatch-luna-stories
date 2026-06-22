"""Persistance SQLite pour l'API de production vidéo (jobs / personnages / scènes).

Stdlib uniquement (sqlite3) — zéro dépendance. La base est l'état partagé entre
l'API (qui crée les jobs) et le worker (qui les exécute).
"""
from __future__ import annotations

import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def _db_path() -> Path:
    # Lu à chaque appel (et pas à l'import) → permet d'isoler la base en test.
    return Path(os.environ.get(
        "YAWATCH_DB", str(Path(__file__).resolve().parents[2] / "content" / "yawatch.db")))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _conn() -> sqlite3.Connection:
    p = _db_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(str(p))
    c.row_factory = sqlite3.Row
    return c


def init_db() -> None:
    """Crée les 3 tables si absentes (idempotent)."""
    with _conn() as c:
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL,          -- queued|running|done|error
                request_json TEXT NOT NULL,
                run_id TEXT, mp4_path TEXT, error TEXT,
                artistic_score INTEGER, gate_passed INTEGER,
                created_at TEXT NOT NULL, updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS characters (
                id TEXT PRIMARY KEY, name TEXT NOT NULL,
                reference_image TEXT, lora_path TEXT, notes TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS scenes (
                id TEXT PRIMARY KEY, name TEXT NOT NULL,
                decor_image TEXT, decor_description TEXT, notes TEXT,
                created_at TEXT NOT NULL
            );
            """
        )


# ── Jobs ────────────────────────────────────────────────────────────────────

def create_job(request: dict[str, Any]) -> str:
    job_id = uuid.uuid4().hex
    now = _now()
    with _conn() as c:
        c.execute(
            "INSERT INTO jobs (id,status,request_json,created_at,updated_at) "
            "VALUES (?,?,?,?,?)",
            (job_id, "queued", json.dumps(request, ensure_ascii=False), now, now),
        )
    return job_id


def update_job(job_id: str, **fields: Any) -> None:
    if not fields:
        return
    fields["updated_at"] = _now()
    cols = ", ".join(f"{k}=?" for k in fields)
    with _conn() as c:
        c.execute(f"UPDATE jobs SET {cols} WHERE id=?", (*fields.values(), job_id))


def get_job(job_id: str) -> dict[str, Any] | None:
    with _conn() as c:
        row = c.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    return dict(row) if row else None


def list_jobs(limit: int = 50) -> list[dict[str, Any]]:
    with _conn() as c:
        rows = c.execute(
            "SELECT id,status,mp4_path,artistic_score,gate_passed,created_at "
            "FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    return [dict(r) for r in rows]


# ── Personnages / Scènes ──────────────────────────────────────────────────────

def add_character(name: str, reference_image: str | None = None,
                  lora_path: str | None = None, notes: str | None = None) -> str:
    cid = uuid.uuid4().hex
    with _conn() as c:
        c.execute("INSERT INTO characters (id,name,reference_image,lora_path,notes,created_at)"
                  " VALUES (?,?,?,?,?,?)", (cid, name, reference_image, lora_path, notes, _now()))
    return cid


def list_characters() -> list[dict[str, Any]]:
    with _conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM characters ORDER BY name").fetchall()]


def add_scene(name: str, decor_image: str | None = None,
              decor_description: str | None = None, notes: str | None = None) -> str:
    sid = uuid.uuid4().hex
    with _conn() as c:
        c.execute("INSERT INTO scenes (id,name,decor_image,decor_description,notes,created_at)"
                  " VALUES (?,?,?,?,?,?)", (sid, name, decor_image, decor_description, notes, _now()))
    return sid


def list_scenes() -> list[dict[str, Any]]:
    with _conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM scenes ORDER BY name").fetchall()]
