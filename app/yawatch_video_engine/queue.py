"""File d'attente des jobs vidéo.

Prod : Celery + Redis (worker sur la machine GPU) — `YAWATCH_QUEUE=celery`.
Dev/test : exécution INLINE (aucun broker requis) → l'API reste testable partout.

Le worker appelle `engine.generate_shot` (→ i2v_adapter → backend gouverné). En
mode `mock`, ça produit un vrai MP4 sans GPU ; en `wan21/framepack`, ça tourne
sur la machine GPU où le worker est lancé.

Lancer le worker (prod) :
    YAWATCH_QUEUE=celery celery -A app.yawatch_video_engine.queue worker --loglevel=info
"""
from __future__ import annotations

import json
import os
import traceback

from . import database as db
from .engine import generate_shot

_BROKER = os.environ.get("YAWATCH_REDIS_URL", "redis://localhost:6379/0")
_USE_CELERY = os.environ.get("YAWATCH_QUEUE", "inline").lower() == "celery"

# Import Celery seulement si demandé (et disponible) — sinon mode inline pur.
celery_app = None
if _USE_CELERY:
    try:
        from celery import Celery
        celery_app = Celery("yawatch_video", broker=_BROKER, backend=_BROKER)
        celery_app.conf.task_track_started = True
    except Exception as exc:  # noqa: BLE001
        print(f"[queue] Celery indisponible ({exc}) → repli mode inline")
        celery_app = None


def _run_job(job_id: str) -> None:
    """Exécute un job : charge la requête, génère, met à jour la DB. Jamais d'exception
    propagée silencieusement — l'erreur est persistée dans le job."""
    job = db.get_job(job_id)
    if not job:
        return
    db.update_job(job_id, status="running")
    try:
        request = json.loads(job["request_json"])
        result = generate_shot(request)
        gate = result.get("artistic_score", {})
        db.update_job(
            job_id, status="done",
            run_id=result.get("run_id"),
            mp4_path=result.get("mp4_final"),
            artistic_score=(gate.get("artistic_score") if isinstance(gate, dict) else None),
            gate_passed=1 if (isinstance(gate, dict) and gate.get("verdict", "").startswith("READY")) else 0,
        )
    except Exception as exc:  # noqa: BLE001
        db.update_job(job_id, status="error", error=f"{exc}\n{traceback.format_exc()[-1500:]}")


# Tâche Celery (n'existe que si Celery est actif).
if celery_app is not None:
    process_job_task = celery_app.task(name="yawatch.process_job")(_run_job)
else:
    process_job_task = None


def submit(job_id: str) -> str:
    """Met le job en file. Retourne le mode ('celery' ou 'inline')."""
    if celery_app is not None and process_job_task is not None:
        process_job_task.delay(job_id)
        return "celery"
    # Dev/test : exécution immédiate, synchrone, en process.
    _run_job(job_id)
    return "inline"
