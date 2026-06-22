# API de production vidéo YAWatch-LUNA — image Cloud Run (HTTPS auto).
# Mode mock par défaut (sans GPU) : sert le frontend + l'API sur une seule URL.
# La génération réelle (Wan/FramePack) reste sur un worker GPU (pod), pas ici.
FROM python:3.11-slim

# ffmpeg = assemblage des MP4 (mode mock + finalisation). Pas de torch/cv2 ici.
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV YAWATCH_QUEUE=inline \
    YAWATCH_DB=/tmp/yawatch.db \
    PYTHONUNBUFFERED=1

# Cloud Run fournit $PORT (8080). uvicorn écoute dessus ; frontend servi sur /.
CMD ["sh", "-c", "uvicorn app.yawatch_video_engine.api:app --host 0.0.0.0 --port ${PORT:-8080}"]
