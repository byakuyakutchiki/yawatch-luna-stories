#!/usr/bin/env python3
"""Runner gouverné YAWatch-LUNA (pod RunPod).

Chaîne RESPECTÉE de bout en bout — aucun workflow édité à la main :

    MotionDirector (prépare + scelle le job)
        → validate_job_governance (refuse tout job altéré)
            → backend ComfyUI (exécute la branche moteur)
                → I2V Quality Gate (seuils INTACTS : SSIM≥0.85 / lumière≤15% / flicker≤0.5)
                    → décision humaine (Ludovic)

Usage (sur le pod, après provision.sh) :
    /usr/local/bin/python tools/runpod/runner.py --engine framepack
    /usr/local/bin/python tools/runpod/runner.py --engine wan21
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# Le repo doit être importable (lancé depuis n'importe où sur le pod).
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from app.motion_director import MotionDirector, TargetPaths  # noqa: E402
from app.i2v_engine.comfyui_backend import (  # noqa: E402
    ComfyEnv, run_job, validate_job_governance,
)

DEFAULT_IMAGE = REPO / "assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png"


def main() -> int:
    ap = argparse.ArgumentParser(description="Runner gouverné I2V YAWatch-LUNA")
    ap.add_argument("--plan", default="plan02")
    ap.add_argument("--engine", required=True, choices=["animatediff", "framepack", "wan21"])
    ap.add_argument("--image", default=str(DEFAULT_IMAGE), help="image source canonique")
    ap.add_argument("--comfy-root", default="/workspace/ComfyUI")
    ap.add_argument("--python-exe", default="/usr/local/bin/python")
    ap.add_argument("--sources-dir", default="/workspace/inputs")
    ap.add_argument("--out", default="/workspace/outputs")
    ap.add_argument("--port", type=int, default=8188)
    ap.add_argument("--no-gate", action="store_true", help="ne pas lancer le Quality Gate I2V")
    args = ap.parse_args()

    # 1. Préparation gouvernée (le rôle métier choisit prompts + paramètres).
    director = MotionDirector(strict=True)
    target = TargetPaths(sources_dir=args.sources_dir, deposit_dir=args.out, posix=True)
    job = director.prepare_job(args.plan, target, engine=args.engine)

    # 2. Gouvernance AVANT toute action (sceau intact ?).
    validate_job_governance(job)
    print(f"[gouvernance] OK  engine={job.engine}  source={job.source_generatrice}")
    print(f"[gouvernance] job_hash={job.job_hash}")
    print(f"[gouvernance] {len(job.locked_parameters)} paramètres verrouillés")

    # 3. Mettre l'image canonique à l'emplacement attendu par le job.
    #    (image_path n'est PAS verrouillé : on peut l'ancrer sur le host.)
    src = Path(args.image)
    if not src.exists():
        sys.exit(f"[ÉCHEC] image source introuvable : {src}")
    staged = Path(job.image_path)
    staged.parent.mkdir(parents=True, exist_ok=True)
    if src.resolve() != staged.resolve():
        shutil.copy2(src, staged)
    print(f"[job] {job.output_name}\n[job] image={job.image_path}")

    # 4. Exécution via le backend (lance ComfyUI, génère, finalise, arrête).
    env = ComfyEnv(comfy_root=args.comfy_root, python_exe=args.python_exe,
                   ffmpeg_exe="ffmpeg", port=args.port)
    mp4 = run_job(env, job)
    print(f"\n✅ Clip généré : {mp4}")

    # 5. Quality Gate I2V — seuils intacts, jamais abaissés.
    if args.no_gate:
        return 0
    from app.i2v_quality_gate import run_i2v_quality_gate
    report_json = Path(args.out) / f"{Path(job.output_name).stem}.i2v_quality_gate.json"
    result = run_i2v_quality_gate(mp4, output_json=report_json)
    print("\n" + str(result))
    print(f"\n[rapport] {report_json}")
    print("→ PASS automatique ≠ validation finale. Visionnage humain de Ludovic obligatoire.")
    return 0 if result.passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
