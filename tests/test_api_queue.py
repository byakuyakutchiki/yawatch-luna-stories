"""Tests de l'API asynchrone (queue inline + moteur mock → MP4 réel, sans GPU)."""
import os
import importlib

import pytest


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Base isolée + mode inline (pas de Celery/Redis requis).
    monkeypatch.setenv("YAWATCH_DB", str(tmp_path / "test.db"))
    monkeypatch.setenv("YAWATCH_QUEUE", "inline")
    from fastapi.testclient import TestClient
    # Recharge queue/api pour relire YAWATCH_QUEUE.
    import app.yawatch_video_engine.queue as q
    import app.yawatch_video_engine.api as api
    importlib.reload(q)
    importlib.reload(api)
    with TestClient(api.app) as c:
        yield c


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_generate_mock_end_to_end(client):
    body = {
        "shot_id": "plan_test_api",
        "character_reference_image": "assets/x/luna.png",
        "dramatic_intention": "Luna walks slowly and looks over her shoulder",
        "shot_type": "deplacement",
        "engine_preference": "mock",
        "duration_sec": 5,
    }
    r = client.post("/generate", json=body)
    assert r.status_code == 200, r.text
    j = r.json()
    job_id = j["job_id"]
    assert j["queue"] == "inline"
    # Mode inline = synchrone → déjà terminé.
    assert j["status"] == "done"

    st = client.get(f"/status/{job_id}").json()
    assert st["status"] == "done"
    assert st["mp4_ready"] is True

    dl = client.get(f"/download/{job_id}")
    assert dl.status_code == 200
    assert dl.headers["content-type"] == "video/mp4"
    assert len(dl.content) > 0


def test_status_unknown_job_404(client):
    assert client.get("/status/nope").status_code == 404


def test_characters_and_scenes(client):
    assert client.get("/characters").json() == []
    client.post("/characters", params={"name": "Luna",
                "reference_image": "assets/luna.png"})
    chars = client.get("/characters").json()
    assert len(chars) == 1 and chars[0]["name"] == "Luna"

    assert client.get("/scenes").json() == []
    client.post("/scenes", params={"name": "Bureau nuit",
                "decor_description": "La Defense"})
    assert len(client.get("/scenes").json()) == 1


def test_frontend_served(client):
    html = client.get("/").text
    assert "YAWatch Video Engine" in html
