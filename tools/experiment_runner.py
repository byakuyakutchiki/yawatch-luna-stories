#!/usr/bin/env python3
"""Boucle de mesure YAWatch-LUNA — « ne plus travailler à l'aveugle ».

Principe : on ne lance JAMAIS un test sans (1) une question et (2) la métrique
qui y répond. Chaque run produit une ligne dans un tableau versionné (CSV + MD).

Deux modes :
  • gate       — mesure des clips MP4 déjà produits (offline, sans GPU/pod).
  • experiment — fait varier UN paramètre, génère via le backend gouverné
                 (pod/ComfyUI), puis mesure. `--dry-run` = construit/scelle les
                 jobs sans générer (vérif logique sans GPU).

Mesures par clip (un seul décodage vidéo) :
  identité SSIM visage, lumière visage (peak-to-peak %), flicker visage,
  + MOUVEMENT (optical flow) visage / épaules / cheveux / image entière,
  + verdict gate (seuils INTACTS : SSIM≥0.85 / lumière≤15% / flicker≤0.5).

Exemples :
  # mesurer des clips existants
  python tools/experiment_runner.py gate \
      --question "FramePack vs Wan: lequel bouge le plus sans casser l'identité ?" \
      --metric "flow_full vs ssim_face_min" \
      --exp-id compare_fp_wan \
      --clips ~/Téléchargements/plan02_luna_FRAMEPACK.mp4 ~/Téléchargements/plan02_luna_WAN.mp4

  # expérience: effet du seed sur l'identité (sur le pod)
  python tools/experiment_runner.py experiment \
      --question "Le seed change-t-il l'identité ?" --metric ssim_face_min \
      --exp-id wan_seed --engine wan21 --vary seed --values 42 123 777 \
      --image assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png \
      --prompt "Luna walks slowly, looks over her shoulder" --duration 3
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

EXPERIMENTS_ROOT = _REPO / "content" / "experiments"

# Colonnes du tableau de résultats (ordre stable).
FIELDS = [
    "timestamp", "exp_id", "question", "metric", "label",
    "engine", "varied_param", "value", "seed", "duration_sec",
    # Capacité 2 — identité (rectangle fixe + visage SUIVI = mesure juste mobile)
    "ssim_face_min", "face_tracked_ssim_min", "face_tracked_ssim_mean",
    "face_detect_rate", "lighting_face_pct", "flicker_face",
    # Métriques artistiques (action E) : matière + stabilité lumineuse (visage suivi)
    "face_sharpness", "face_luma_variation_pct", "face_luma_flicker",
    # Capacité 1 — mouvement (brut + organique vs glissement)
    "flow_face", "flow_shoulders", "flow_hair", "flow_full",
    "translation_risk", "organic_score", "face_residual",
    # Capacité 3 — décor
    "background_lighting_pct", "background_flicker",
    "gate_passed", "mp4",
]


def measure_clip(mp4: str | Path, max_frames: int | None = 80) -> dict:
    """Décode UNE fois et renvoie identité + lumière + flicker + mouvement + verdict."""
    from app.video_metrics_evaluator import evaluate_video
    from app.i2v_quality_gate import metrics_from_video_metric_report, evaluate_i2v_metrics

    from app.motion_metrics import compute_organic_motion
    from app.video_metrics_evaluator import tracked_face_identity_ssim

    report = evaluate_video(Path(mp4), max_frames=max_frames)
    tracked = tracked_face_identity_ssim(Path(mp4), max_frames=max_frames)
    gate_metrics = metrics_from_video_metric_report(report)
    gate = evaluate_i2v_metrics(mp4, gate_metrics)
    flow = {r.name: r.optical_flow_mean for r in report.regions}
    face = next(r for r in report.regions if r.name == "face")
    bg = next((r for r in report.regions if r.name == "background"), None)
    # Mouvement organique vs glissement (cadre photo qui glisse) — Capacité 1.
    om = compute_organic_motion(mp4)
    return {
        "ssim_face_min": round(report.identity_ssim_face_min, 4),
        "lighting_face_pct": round(face.luminance_peak_to_peak_pct, 4),
        "flicker_face": round(face.flicker_mean_abs_delta, 4),
        "flow_face": round(flow.get("face", 0.0), 4),
        "flow_shoulders": round(flow.get("shoulders", 0.0), 4),
        "flow_hair": round(flow.get("hair", 0.0), 4),
        "flow_full": round(flow.get("full_frame", 0.0), 4),
        "translation_risk": om.translation_risk,
        "organic_score": om.organic_score,
        "face_residual": om.face_residual,
        "background_lighting_pct": round(bg.luminance_peak_to_peak_pct, 4) if bg else "",
        "background_flicker": round(bg.flicker_mean_abs_delta, 4) if bg else "",
        # Identité + qualité sur visage SUIVI (boîte détectée) — juste pour sujet mobile.
        "face_tracked_ssim_min": tracked["face_tracked_ssim_min"],
        "face_tracked_ssim_mean": tracked["face_tracked_ssim_mean"],
        "face_detect_rate": tracked["face_detect_rate"],
        # Métriques artistiques (action E) : netteté/matière + stabilité lumineuse
        "face_sharpness": tracked.get("face_tracked_sharpness", ""),
        "face_luma_variation_pct": tracked.get("face_tracked_luma_variation_pct", ""),
        "face_luma_flicker": tracked.get("face_tracked_luma_flicker", ""),
        "gate_passed": gate.passed,
        "duration_sec": round(report.duration_sec, 2),
    }


def _exp_dir(exp_id: str) -> Path:
    d = EXPERIMENTS_ROOT / exp_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def _write_manifest(exp_dir: Path, question: str, metric: str) -> None:
    # Garde-fou anti-aveugle : la question et la métrique sont enregistrées.
    (exp_dir / "manifest.json").write_text(
        json.dumps({"question": question, "metric": metric}, ensure_ascii=False, indent=2),
        encoding="utf-8")


def _append_rows(exp_dir: Path, rows: list[dict]) -> None:
    csv_path = exp_dir / "results.csv"
    existing = []
    if csv_path.exists():
        existing = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    all_rows = existing + rows
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in all_rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    _write_markdown(exp_dir, all_rows)


def _write_markdown(exp_dir: Path, rows: list[dict]) -> None:
    q = ""
    man = exp_dir / "manifest.json"
    if man.exists():
        q = json.loads(man.read_text(encoding="utf-8")).get("question", "")
    cols = ["label", "face_tracked_ssim_min", "face_sharpness",
            "face_luma_variation_pct", "face_luma_flicker", "flow_full",
            "organic_score", "gate_passed"]
    lines = [f"# Expérience : {exp_dir.name}", "", f"**Question :** {q}", "",
             "| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for r in rows:
        lines.append("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |")
    (exp_dir / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _now(ts: str | None) -> str:
    return ts or "unstamped"  # Date.now indispo ici ; passer --timestamp si besoin


def cmd_gate(args) -> int:
    exp_dir = _exp_dir(args.exp_id)
    _write_manifest(exp_dir, args.question, args.metric)
    rows = []
    for clip in args.clips:
        m = measure_clip(clip, max_frames=args.max_frames)
        label = Path(clip).stem
        rows.append({"timestamp": _now(args.timestamp), "exp_id": args.exp_id,
                     "question": args.question, "metric": args.metric, "label": label,
                     "engine": "", "varied_param": "", "value": "", "seed": "",
                     "mp4": str(clip), **m})
        print(f"[mesuré] {label}: SSIM={m['ssim_face_min']} lumière={m['lighting_face_pct']}% "
              f"flicker={m['flicker_face']} flow_full={m['flow_full']} gate={'PASS' if m['gate_passed'] else 'FAIL'}")
    _append_rows(exp_dir, rows)
    print(f"\n→ tableau : {exp_dir/'results.md'}")
    return 0


def cmd_experiment(args) -> int:
    exp_dir = _exp_dir(args.exp_id)
    _write_manifest(exp_dir, args.question, args.metric)
    from app.i2v_engine.comfyui_backend import (
        VideoJob, run_job, compute_job_hash, validate_job_governance, ComfyEnv,
        GOVERNED_SOURCE, DEFAULT_LOCKED_PARAMETERS, WAN21_DEFAULTS, FRAMEPACK_DEFAULTS,
        ENGINE_WAN21,
    )
    defaults = WAN21_DEFAULTS if args.engine == ENGINE_WAN21 else FRAMEPACK_DEFAULTS
    image = str((_REPO / args.image) if not Path(args.image).is_absolute() else Path(args.image))
    env = ComfyEnv(comfy_root=args.comfy_root, python_exe=args.python_exe, ffmpeg_exe="ffmpeg")
    rows = []
    for val in args.values:
        engine_params = dict(defaults)
        seed = int(args.seed)
        if args.vary == "seed":
            seed = int(val)
        elif args.vary in engine_params:
            engine_params[args.vary] = type(engine_params[args.vary])(val)
        label = f"{args.vary}={val}"
        job = VideoJob(
            output_name=f"{args.exp_id}_{args.vary}_{val}.mp4",
            deposit_dir=str(exp_dir / "clips"), image_path=image,
            prompt_positive=args.prompt, prompt_negative=args.negative,
            engine=args.engine, engine_params=engine_params, seed=seed,
            plan_id=args.exp_id, plan_type="experiment", character="luna_adulte",
        )
        job.source_generatrice = GOVERNED_SOURCE
        job.locked_parameters = tuple(DEFAULT_LOCKED_PARAMETERS)
        job.job_hash = compute_job_hash(job)
        validate_job_governance(job)
        print(f"[job scellé] {label} hash={job.job_hash[:12]}")
        if args.dry_run:
            rows.append({"timestamp": _now(args.timestamp), "exp_id": args.exp_id,
                         "question": args.question, "metric": args.metric, "label": label,
                         "engine": args.engine, "varied_param": args.vary, "value": val,
                         "seed": seed, "mp4": "(dry-run)"})
            continue
        try:
            mp4 = run_job(env, job)
        except Exception as exc:
            print(f"[ÉCHEC génération] {label}: {exc}")
            rows.append({"timestamp": _now(args.timestamp), "exp_id": args.exp_id,
                         "question": args.question, "metric": args.metric, "label": label,
                         "engine": args.engine, "varied_param": args.vary, "value": val,
                         "seed": seed, "mp4": f"ERROR: {exc}"})
            continue
        m = measure_clip(mp4, max_frames=args.max_frames)
        rows.append({"timestamp": _now(args.timestamp), "exp_id": args.exp_id,
                     "question": args.question, "metric": args.metric, "label": label,
                     "engine": args.engine, "varied_param": args.vary, "value": val,
                     "seed": seed, "mp4": str(mp4), **m})
        print(f"[mesuré] {label}: SSIM={m['ssim_face_min']} flow_full={m['flow_full']} "
              f"gate={'PASS' if m['gate_passed'] else 'FAIL'}")
    _append_rows(exp_dir, rows)
    print(f"\n→ tableau : {exp_dir/'results.md'}")
    return 0


def cmd_restore(args) -> int:
    """Mesure un clip, restaure le visage (étage 2), re-mesure, logue avant/après."""
    from app.yawatch_video_engine.face_restore import restore_video_faces
    exp_dir = _exp_dir(args.exp_id)
    _write_manifest(exp_dir, args.question, args.metric)
    src = Path(args.clip)
    out = exp_dir / "clips" / f"{src.stem}_restored_{args.backend}.mp4"
    rows = []

    before = measure_clip(src, max_frames=args.max_frames)
    print(f"[avant] SSIM={before['ssim_face_min']} flicker={before['flicker_face']} "
          f"flow_full={before['flow_full']} gate={'PASS' if before['gate_passed'] else 'FAIL'}")
    rows.append({"timestamp": _now(args.timestamp), "exp_id": args.exp_id,
                 "question": args.question, "metric": args.metric, "label": f"{src.stem}__avant",
                 "engine": "", "varied_param": "restore", "value": "none", "seed": "",
                 "mp4": str(src), **before})

    restore_video_faces(src, out, backend=args.backend, fidelity=args.fidelity,
                        reference_image=getattr(args, "reference", None))

    after = measure_clip(out, max_frames=args.max_frames)
    print(f"[après] SSIM={after['ssim_face_min']} flicker={after['flicker_face']} "
          f"flow_full={after['flow_full']} gate={'PASS' if after['gate_passed'] else 'FAIL'}")
    rows.append({"timestamp": _now(args.timestamp), "exp_id": args.exp_id,
                 "question": args.question, "metric": args.metric,
                 "label": f"{src.stem}__apres_{args.backend}",
                 "engine": "", "varied_param": "restore", "value": args.backend, "seed": "",
                 "mp4": str(out), **after})

    d_ssim = round(after["ssim_face_min"] - before["ssim_face_min"], 4)
    d_flick = round(after["flicker_face"] - before["flicker_face"], 4)
    d_flow = round(after["flow_full"] - before["flow_full"], 4)
    print(f"\nΔ SSIM={d_ssim:+}  Δ flicker={d_flick:+}  Δ mouvement={d_flow:+}")
    print("→ restauration UTILE si Δ SSIM > 0 sans casser flicker ni mouvement")
    _append_rows(exp_dir, rows)
    print(f"→ tableau : {exp_dir/'results.md'}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Boucle de mesure I2V YAWatch-LUNA")
    p.add_argument("--timestamp", default=None, help="horodatage (sinon 'unstamped')")
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("gate", help="mesurer des clips existants (offline)")
    g.add_argument("--question", required=True)
    g.add_argument("--metric", required=True)
    g.add_argument("--exp-id", required=True)
    g.add_argument("--clips", nargs="+", required=True)
    g.add_argument("--max-frames", type=int, default=80)
    g.set_defaults(func=cmd_gate)

    e = sub.add_parser("experiment", help="varier 1 paramètre + générer (pod)")
    e.add_argument("--question", required=True)
    e.add_argument("--metric", required=True)
    e.add_argument("--exp-id", required=True)
    e.add_argument("--engine", default="wan21")
    e.add_argument("--vary", required=True, help="seed | steps | cfg | shift | ...")
    e.add_argument("--values", nargs="+", required=True)
    e.add_argument("--image", required=True)
    e.add_argument("--prompt", required=True)
    e.add_argument("--negative", default="deformed face, identity change, low quality")
    e.add_argument("--seed", default="2406202601")
    e.add_argument("--duration", type=float, default=3.0)
    e.add_argument("--max-frames", type=int, default=80)
    e.add_argument("--dry-run", action="store_true")
    e.add_argument("--comfy-root", default="/workspace/ComfyUI")
    e.add_argument("--python-exe", default="/usr/local/bin/python")
    e.set_defaults(func=cmd_experiment)

    r = sub.add_parser("restore", help="restaurer le visage d'un clip (étage 2) + mesurer avant/après")
    r.add_argument("--question", required=True)
    r.add_argument("--metric", required=True)
    r.add_argument("--exp-id", required=True)
    r.add_argument("--clip", required=True)
    r.add_argument("--backend", default="gfpgan", choices=["gfpgan", "codeformer", "faceswap"])
    r.add_argument("--reference", default=None, help="image canonique (backend faceswap)")
    r.add_argument("--fidelity", type=float, default=0.7)
    r.add_argument("--max-frames", type=int, default=80)
    r.set_defaults(func=cmd_restore)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
