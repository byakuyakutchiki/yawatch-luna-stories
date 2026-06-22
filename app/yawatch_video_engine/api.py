from __future__ import annotations

from fastapi import FastAPI

from .engine import generate_shot
from .schemas import GenerateShotRequest, GenerateShotResponse


app = FastAPI(
    title="yawatch-video-engine",
    version="0.1.0",
    description="Local API MVP for narrative cinematic YAWatch-LUNA shot production.",
)


def _dump_model(model: GenerateShotRequest) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


@app.post("/generate-shot", response_model=GenerateShotResponse)
def generate_shot_endpoint(request: GenerateShotRequest) -> dict:
    return generate_shot(_dump_model(request))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "yawatch-video-engine"}
