"""Organic-motion metrics for YAWatch-LUNA I2V clips.

Why this module exists
----------------------
The optical-flow magnitude already computed in ``video_metrics_evaluator`` answers
"how much do pixels move", but NOT "is it a living character or a sliding photo".
A whole frame that translates left-right scores a HIGH flow magnitude while being
exactly the artefact we reject ("cadre photo qui bouge de gauche a droite").

This module separates the flow field into two parts per frame pair:

* GLOBAL TRANSLATION : the median flow vector over the whole frame. A uniform
  camera slide / postcard drift shows up here. We want this LOW.
* RESIDUAL (LOCAL) MOTION : flow minus the global vector. Breathing, head tilt,
  shoulder rise, blinking live here. We want this present in the face/shoulders
  and ABSENT in the background.

It never replaces Ludovic's eye. It turns "alive vs sliding" into numbers so the
Quality Gate can reject a sliding photo even when raw flow looks high.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import cv2
import numpy as np

# Same transparent zones as video_metrics_evaluator (vertical portrait framing).
REGIONS = {
    "face": (0.30, 0.09, 0.40, 0.27),
    "hair": (0.18, 0.05, 0.64, 0.42),
    "shoulders": (0.14, 0.43, 0.72, 0.34),
    "background": (0.08, 0.02, 0.84, 0.20),
}


def _crop_mask(shape, region):
    h, w = shape
    x, y, rw, rh = region
    x0 = max(0, min(w - 1, int(round(x * w))))
    y0 = max(0, min(h - 1, int(round(y * h))))
    x1 = max(x0 + 1, min(w, int(round((x + rw) * w))))
    y1 = max(y0 + 1, min(h, int(round((y + rh) * h))))
    return slice(y0, y1), slice(x0, x1)


@dataclass(frozen=True)
class OrganicMotionReport:
    video_path: str
    frames: int
    # whole-frame decomposition (pixels/frame)
    global_translation_mean: float   # uniform camera/postcard slide — want LOW
    residual_motion_mean: float      # local non-uniform motion — the "life"
    total_motion_mean: float
    translation_risk: float          # 0..1, share of motion that is uniform slide — want LOW
    local_motion_ratio: float        # 0..1, share that is local — want HIGH
    # residual motion per zone — want face/shoulders alive, background still
    face_residual: float
    shoulders_residual: float
    hair_residual: float
    background_residual: float
    # composite 0..1, higher = more credibly alive (and not a sliding frame)
    organic_score: float


def compute_organic_motion(video_path: str | Path) -> OrganicMotionReport:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")
    frames = []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        frames.append(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY))
    cap.release()
    if len(frames) < 2:
        raise RuntimeError(f"Not enough frames: {video_path}")

    glob, resid, total = [], [], []
    zone_resid = {z: [] for z in REGIONS}
    for prev, curr in zip(frames, frames[1:]):
        flow = cv2.calcOpticalFlowFarneback(
            prev, curr, None, 0.5, 3, 15, 3, 5, 1.2, 0
        )
        fx, fy = flow[..., 0], flow[..., 1]
        # global translation = robust median vector over the frame
        gx, gy = float(np.median(fx)), float(np.median(fy))
        glob.append((gx * gx + gy * gy) ** 0.5)
        # residual = flow minus uniform slide
        rmag = np.sqrt((fx - gx) ** 2 + (fy - gy) ** 2)
        resid.append(float(rmag.mean()))
        total.append(float(np.sqrt(fx * fx + fy * fy).mean()))
        for z, reg in REGIONS.items():
            ys, xs = _crop_mask(prev.shape, reg)
            zone_resid[z].append(float(rmag[ys, xs].mean()))

    g = float(np.mean(glob))
    r = float(np.mean(resid))
    t = float(np.mean(total))
    translation_risk = g / (g + r) if (g + r) > 0 else 0.0
    local_ratio = r / (g + r) if (g + r) > 0 else 0.0
    face_r = float(np.mean(zone_resid["face"]))
    sh_r = float(np.mean(zone_resid["shoulders"]))
    hair_r = float(np.mean(zone_resid["hair"]))
    bg_r = float(np.mean(zone_resid["background"]))

    # Composite: reward localized life in face+shoulders, penalize sliding frame
    # and a background that moves as much as the subject.
    life = min(1.0, (face_r + sh_r) / 2.0 / 0.20)        # ~0.20 residual ≈ clearly alive
    slide_penalty = translation_risk                      # 0 good .. 1 bad
    bg_penalty = min(1.0, bg_r / max(1e-6, (face_r + sh_r) / 2.0))  # bg should be < subject
    organic = max(0.0, life * (1.0 - 0.6 * slide_penalty) * (1.0 - 0.4 * bg_penalty))

    rnd = lambda v: round(float(v), 4)
    return OrganicMotionReport(
        video_path=str(video_path), frames=len(frames),
        global_translation_mean=rnd(g), residual_motion_mean=rnd(r),
        total_motion_mean=rnd(t), translation_risk=rnd(translation_risk),
        local_motion_ratio=rnd(local_ratio),
        face_residual=rnd(face_r), shoulders_residual=rnd(sh_r),
        hair_residual=rnd(hair_r), background_residual=rnd(bg_r),
        organic_score=rnd(organic),
    )


# Proposed gate thresholds (calibrated on real clips — see RUNPOD_CLOUD_RESULTS).
ORGANIC_THRESHOLDS = {
    "organic_score_min": 0.35,       # below = lifeless or sliding
    "translation_risk_max": 0.45,    # above = whole frame is sliding (postcard)
    "face_residual_min": 0.06,       # face must show local life
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Organic vs sliding motion metric.")
    ap.add_argument("videos", nargs="+", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    reports = [compute_organic_motion(v) for v in args.videos]
    if args.json:
        print(json.dumps([asdict(r) for r in reports], indent=2, ensure_ascii=False))
    else:
        for r in reports:
            print(f"\n{Path(r.video_path).name}")
            print(f"  organic_score   = {r.organic_score}   (>= {ORGANIC_THRESHOLDS['organic_score_min']})")
            print(f"  translation_risk= {r.translation_risk}   (<= {ORGANIC_THRESHOLDS['translation_risk_max']})  [haut = cadre qui glisse]")
            print(f"  residual face={r.face_residual} shoulders={r.shoulders_residual} bg={r.background_residual}")
            print(f"  global_slide={r.global_translation_mean}  local={r.residual_motion_mean}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
