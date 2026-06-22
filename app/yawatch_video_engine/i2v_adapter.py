from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Protocol

from .montage_exporter import export_montage

# Racine du repo : .../app/yawatch_video_engine/i2v_adapter.py -> remonte de 3
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Négatif anti-déformation prouvé (identité/anatomie). Aligné sur le pipeline gouverné.
_NEGATIVE = (
    "different person, identity change, face swap, deformed face, distorted eyes, "
    "asymmetric eyes, melting face, bad anatomy, extra fingers, fused fingers, "
    "child, teen, glamour, sexualized, cartoon, anime, cyberpunk, neon, "
    "purple dominant lighting, changing skin tone, inconsistent lighting, "
    "exposure flicker, text, watermark, logo, low quality, heavy flicker, jitter, "
    "violent motion, foot sliding, body scale changing"
)


def _resolve_image(path: str | None) -> str:
    """Résout un chemin d'image (relatif au repo si nécessaire) en absolu."""
    if not path:
        raise ValueError("character_reference_image manquant : pas de source I2V.")
    p = Path(path)
    if not p.is_absolute():
        p = _REPO_ROOT / path
    return str(p)


def _build_prompt(request: dict[str, Any], shot_plan: dict[str, Any],
                  motion_plan: dict[str, Any]) -> str:
    """Assemble un prompt ORIENTÉ ACTION (pas « respire et regarde »).

    Priorité à l'intention dramatique + mouvement du corps. La vision Ludovic :
    Luna existe, bouge, marche, se retourne — pas un portrait animé.
    """
    parts: list[str] = []
    intention = (request.get("dramatic_intention") or "").strip()
    if intention:
        parts.append(intention)
    emotion = (shot_plan.get("emotion") or request.get("emotion") or "").strip()
    if emotion:
        parts.append(f"{emotion} expression")
    # Corps entier : indices VISUELS selon le type de plan (priorité Ludovic =
    # Luna bouge intégralement, pas juste le buste). On n'injecte PAS le texte de
    # stratégie pipeline (ça, c'est pour le backend, pas pour le prompt).
    shot_type = shot_plan.get("shot_type", "")
    if shot_type in {"deplacement", "plan_large"}:
        parts.append("full body visible in frame, whole-body movement, legible gait, "
                     "feet planted on the ground, natural weight shift")
    subj = motion_plan.get("subject_motion")
    if subj:
        parts.append(subj)
    cam = motion_plan.get("camera_motion")
    if cam:
        parts.append(cam.replace("_", " ") + " camera")
    # Ancrage identité + facture cinéma premium.
    parts.append(
        "same identity as the reference image, consistent face and hair, "
        "cinematic premium psychological thriller, natural human presence, "
        "realistic skin, soft cinematic lighting, shallow depth of field, "
        "film grain, high quality, no text"
    )
    return ", ".join(p for p in parts if p)


def _comfy_env():
    """ComfyEnv depuis variables d'env (défauts = pod RunPod)."""
    from app.i2v_engine.comfyui_backend import ComfyEnv
    return ComfyEnv(
        comfy_root=os.environ.get("YAWATCH_COMFY_ROOT", "/workspace/ComfyUI"),
        python_exe=os.environ.get("YAWATCH_PYTHON_EXE", "/usr/local/bin/python"),
        ffmpeg_exe=os.environ.get("YAWATCH_FFMPEG", "ffmpeg"),
        port=int(os.environ.get("YAWATCH_COMFY_PORT", "8188")),
    )


class I2VAdapter(Protocol):
    name: str

    def generate(self, run_dir: Path, request: dict[str, Any],
                 shot_plan: dict[str, Any], motion_plan: dict[str, Any]) -> dict[str, Any]:
        ...


class MockCinematicAdapter:
    name = "mock_cinematic_ffmpeg"

    def generate(self, run_dir, request, shot_plan, motion_plan):
        export = export_montage(run_dir, request, shot_plan, motion_plan)
        return {
            "adapter": self.name,
            "status": "mock_generated",
            "engine_role": "local proof of API architecture, not artistic validation",
            **export,
        }


class _GovernedI2VAdapter:
    """Base réelle : construit un VideoJob SCELLÉ et le génère via le backend gouverné.

    Chaîne respectée : request -> prompt action -> VideoJob (job_hash +
    locked_parameters) -> validate_job_governance -> backend ComfyUI -> MP4 ->
    Quality Gate I2V. Aucun workflow édité à la main.
    """
    name = "governed"
    engine = ""

    def generate(self, run_dir: Path, request: dict[str, Any],
                 shot_plan: dict[str, Any], motion_plan: dict[str, Any]) -> dict[str, Any]:
        # Imports lazy : le mode mock et les tests ne dépendent pas de cv2/backend.
        from app.i2v_engine.comfyui_backend import (
            VideoJob, run_job, compute_job_hash, validate_job_governance,
            GOVERNED_SOURCE, DEFAULT_LOCKED_PARAMETERS,
            WAN21_DEFAULTS, FRAMEPACK_DEFAULTS,
            ENGINE_WAN21, ENGINE_FRAMEPACK,
        )

        defaults = WAN21_DEFAULTS if self.engine == ENGINE_WAN21 else FRAMEPACK_DEFAULTS
        engine_params = dict(defaults)
        prompt = _build_prompt(request, shot_plan, motion_plan)
        image_path = _resolve_image(request.get("character_reference_image"))
        artifacts = run_dir / "artifacts"
        artifacts.mkdir(parents=True, exist_ok=True)
        out_name = f"{request.get('shot_id', 'shot')}_{self.engine}.mp4"

        job = VideoJob(
            output_name=out_name,
            deposit_dir=str(artifacts),
            image_path=image_path,
            prompt_positive=prompt,
            prompt_negative=_NEGATIVE,
            engine=self.engine,
            engine_params=engine_params,
            seed=int(request.get("seed", 2406202601)),
            fps=float(request.get("fps", 24)),
            plan_id=request.get("shot_id", ""),
            plan_type=shot_plan.get("shot_type", ""),
            character="luna_adulte",
        )
        # Sceau de gouvernance (verrouillage identité/params + hash anti-altération).
        job.source_generatrice = GOVERNED_SOURCE
        job.locked_parameters = tuple(DEFAULT_LOCKED_PARAMETERS)
        job.job_hash = compute_job_hash(job)
        validate_job_governance(job)

        result: dict[str, Any] = {
            "adapter": self.name,
            "engine": self.engine,
            "job_hash": job.job_hash,
            "prompt_positive": prompt,
            "preview_png": None,
            "is_mock_video": False,
        }
        try:
            mp4 = run_job(_comfy_env(), job)
        except Exception as exc:  # le backend a échoué (modèle, VRAM, node…)
            result.update({"status": "error", "mp4_path": None,
                           "export_status": "render_failed", "error": str(exc)})
            return result

        result.update({"status": "generated", "mp4_path": str(mp4), "export_status": "ok"})

        # Quality Gate I2V — seuils intacts (SSIM>=0.85 / lumière<=15% / flicker<=0.5).
        try:
            from app.i2v_quality_gate import run_i2v_quality_gate
            gate = run_i2v_quality_gate(mp4, output_json=run_dir / "i2v_quality_gate.json")
            result["i2v_quality_gate"] = gate.to_dict()
            result["gate_passed"] = gate.passed
        except Exception as exc:
            result["i2v_quality_gate_error"] = str(exc)
        return result


class WanAdapter(_GovernedI2VAdapter):
    name = "wan21"
    engine = "wan21"


class FramePackAdapter(_GovernedI2VAdapter):
    name = "framepack"
    engine = "framepack"


class PoseToVideoAdapter:
    """Mouvement corps entier piloté par squelette (OpenPose/ControlNet).

    HONNÊTE : le ControlNet pose pour Wan n'est PAS encore installé dans notre
    ComfyUI. Le mouvement corps entier passe pour l'instant par le PROMPT
    (via WanAdapter), pas par un squelette imposé. Ce vrai contrôle de pose est
    le prochain chantier (pipeline 2 étages : pose -> I2V -> restauration visage).
    """
    name = "pose_to_video_future"

    def generate(self, run_dir, request, shot_plan, motion_plan):
        return {
            "adapter": self.name,
            "status": "planned_not_executed",
            "mp4_path": None,
            "preview_png": None,
            "required_next_step": "installer ControlNet/OpenPose pour Wan, puis restauration visage (2 étages)",
            "locked_inputs": {
                "pose_reference": request.get("pose_reference"),
                "shot_type": shot_plan["shot_type"],
            },
        }


def select_adapter(engine_preference: str | None) -> I2VAdapter:
    key = (engine_preference or "mock").lower()
    if key in {"wan", "wan21", "wan2.1"}:
        return WanAdapter()
    if key in {"framepack", "frame_pack"}:
        return FramePackAdapter()
    if key in {"pose", "pose_to_video"}:
        return PoseToVideoAdapter()
    return MockCinematicAdapter()
