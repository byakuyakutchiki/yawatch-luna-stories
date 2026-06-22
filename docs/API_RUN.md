# Lancer l'API de production vidéo (yawatch-video-engine)

API asynchrone style Kling : on poste un job, on récupère un `job_id`, on
poll le statut, on télécharge le MP4. Frontend web inclus sur `/`.

## Dev / local (mode inline, sans Redis ni GPU)
```bash
pip install -r requirements.txt
uvicorn app.yawatch_video_engine.api:app --reload --port 8000
# → http://localhost:8000  (frontend)  | engine_preference="mock" = MP4 sans GPU
```
En mode inline, le job s'exécute **dans le process API** (pratique pour tester).

## Prod (Celery + Redis, worker sur la machine GPU)
```bash
# 1) broker
redis-server &
# 2) worker (sur la machine GPU — c'est lui qui appelle Wan/FramePack)
export YAWATCH_QUEUE=celery YAWATCH_REDIS_URL=redis://localhost:6379/0
celery -A app.yawatch_video_engine.queue worker --loglevel=info &
# 3) API (peut être sur une autre machine partageant la même DB/Redis)
export YAWATCH_QUEUE=celery
uvicorn app.yawatch_video_engine.api:app --host 0.0.0.0 --port 8000
```

## Endpoints
| Méthode | Route | Rôle |
|---|---|---|
| POST | `/generate` | crée un job en file → `{job_id, queue, status}` |
| GET | `/status/{job_id}` | statut (queued/running/done/error) + score |
| GET | `/download/{job_id}` | le MP4 (quand done) |
| POST | `/upload-image` | uploade une image → chemin serveur |
| GET/POST | `/characters` `/scenes` | bibliothèque personnages / décors |
| GET | `/jobs` | derniers jobs |
| GET | `/` | frontend web |

## Variables d'environnement
- `YAWATCH_QUEUE` : `inline` (défaut) ou `celery`
- `YAWATCH_REDIS_URL` : broker (défaut `redis://localhost:6379/0`)
- `YAWATCH_DB` : chemin SQLite (défaut `content/yawatch.db`)
- `YAWATCH_COMFY_ROOT` / `YAWATCH_PYTHON_EXE` : pour le worker GPU (cf. i2v_adapter)

## Note
Le **worker doit tourner sur la machine GPU** (il appelle ComfyUI via le backend
gouverné). En `mock`, tout marche sans GPU (preuve d'architecture). En
`wan21`/`framepack`, le worker génère réellement là où sont les modèles.
