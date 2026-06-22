from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

from . import database as db
from .engine import generate_shot
from .queue import submit
from .schemas import GenerateShotRequest, GenerateShotResponse

_ROOT = Path(__file__).resolve().parents[2]
_UPLOADS = _ROOT / "content" / "uploads"
_STATIC = Path(__file__).resolve().parent / "static"

app = FastAPI(
    title="yawatch-video-engine",
    version="0.2.0",
    description="API asynchrone de production vidéo narrative YAWatch-LUNA (remplace Kling).",
)


@app.on_event("startup")
def _startup() -> None:
    db.init_db()


def _dump(model: GenerateShotRequest) -> dict:
    return model.model_dump() if hasattr(model, "model_dump") else model.dict()


# ── Frontend ──────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def home() -> str:
    idx = _STATIC / "index.html"
    return idx.read_text(encoding="utf-8") if idx.exists() else "<h1>yawatch-video-engine</h1>"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "yawatch-video-engine"}


# ── Génération asynchrone (comme Kling) ───────────────────────────────────────

@app.post("/generate")
def generate(request: GenerateShotRequest) -> dict:
    """Crée un job, le met en file, retourne un job_id immédiatement."""
    job_id = db.create_job(_dump(request))
    mode = submit(job_id)
    job = db.get_job(job_id)
    return {"job_id": job_id, "queue": mode, "status": job["status"] if job else "queued"}


@app.get("/status/{job_id}")
def status(job_id: str) -> dict:
    job = db.get_job(job_id)
    if not job:
        raise HTTPException(404, "job introuvable")
    return {
        "job_id": job_id, "status": job["status"],
        "mp4_ready": bool(job.get("mp4_path")),
        "artistic_score": job.get("artistic_score"),
        "gate_passed": bool(job.get("gate_passed")),
        "error": job.get("error"),
    }


@app.get("/download/{job_id}")
def download(job_id: str):
    job = db.get_job(job_id)
    if not job:
        raise HTTPException(404, "job introuvable")
    if job["status"] != "done" or not job.get("mp4_path"):
        raise HTTPException(409, f"pas pret (statut={job['status']})")
    mp4 = Path(job["mp4_path"])
    if not mp4.exists():
        raise HTTPException(410, "MP4 absent sur le disque")
    return FileResponse(str(mp4), media_type="video/mp4", filename=mp4.name)


# ── Assets ────────────────────────────────────────────────────────────────────

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)) -> dict:
    _UPLOADS.mkdir(parents=True, exist_ok=True)
    suffix = Path(file.filename or "img.png").suffix or ".png"
    dest = _UPLOADS / f"{uuid.uuid4().hex}{suffix}"
    with dest.open("wb") as out:
        shutil.copyfileobj(file.file, out)
    return {"path": str(dest), "filename": file.filename}


@app.get("/characters")
def characters() -> list[dict]:
    return db.list_characters()


@app.post("/characters")
def add_character(name: str, reference_image: str | None = None,
                  lora_path: str | None = None, notes: str | None = None) -> dict:
    return {"id": db.add_character(name, reference_image, lora_path, notes)}


@app.get("/scenes")
def scenes() -> list[dict]:
    return db.list_scenes()


@app.post("/scenes")
def add_scene(name: str, decor_image: str | None = None,
              decor_description: str | None = None, notes: str | None = None) -> dict:
    return {"id": db.add_scene(name, decor_image, decor_description, notes)}


@app.get("/jobs")
def jobs() -> list[dict]:
    return db.list_jobs()


# ── Compat : génération synchrone (MVP d'origine) ─────────────────────────────

@app.post("/generate-shot", response_model=GenerateShotResponse)
def generate_shot_endpoint(request: GenerateShotRequest) -> dict:
    return generate_shot(_dump(request))
