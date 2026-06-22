# YAWatch Video Engine

Local API-first MVP for producing narrative cinematic shots for YAWatch-LUNA.

This is not a Wan vs FramePack comparison layer. It is an orchestration layer:

1. parse the scene and dramatic intention;
2. plan the shot;
3. plan camera, pose, motion, and sound;
4. select an I2V adapter;
5. generate a reusable production run folder;
6. review technical and artistic readiness.

The default adapter is `mock`, so the API can be tested without spending GPU
time. Real engines are intended to plug into `i2v_adapter.py`.

## Run locally

```powershell
uvicorn app.yawatch_video_engine.api:app --reload --port 8010
```

Then call:

```http
POST http://127.0.0.1:8010/generate-shot
```

## Output

Each request creates a folder in:

```text
content/video_engine_runs/<timestamp>_<shot_id>/
```

The folder contains:

- `input.json`
- `scene_parse.json`
- `shot_plan.json`
- `camera_plan.json`
- `pose_plan.json`
- `motion_plan.json`
- `sound_plan.json`
- `render_result.json`
- `quality_review.json`
- `metadata.json`
- `preview.png`
- `final.mp4` when FFmpeg is available in mock mode
- `logs/technical.log`

## Adapter contract

Adapters must never rewrite the director intent silently. They receive the
locked request and motion plan, then return:

- `adapter`
- `status`
- `mp4_path`
- `preview_png`
- technical notes

Future production adapters:

- `wan21`: connect to the existing Wan GGUF/ComfyUI workflow runner.
- `framepack`: connect to the RunPod/local FramePack runner.
- `pose_to_video`: add pose/depth/control before I2V for body movement.

## Quality principle

The first score is not a scientific video score. It is an artistic readiness
score for the production plan. Real MP4 metrics should be added after a real I2V
adapter produces video frames.
