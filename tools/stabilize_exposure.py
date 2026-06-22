#!/usr/bin/env python3
"""Stabilisation d'EXPOSITION temporelle (action A — stabilité lumineuse).

Problème (audit Codex) : la luminosité du visage varie ~42-47% d'une frame à
l'autre sur les sorties WAN, contre ~15% chez Kling → le visage « scintille ».

Solution (≠ colormatch qui a échoué) : on applique un **gain de luminosité
GLOBAL par frame** (toute l'image, donc aucun artefact local « recollé »),
piloté par la luma du **visage suivi** et **lissé temporellement** (moyenne
glissante) pour supprimer le flicker tout en gardant les variations lentes
voulues. Ça ne touche NI la couleur NI la netteté (c'est un gain, pas un filtre).

CPU pur (cv2 + Haar). Affiche les métriques avant/après.

Usage :
    python tools/stabilize_exposure.py --input wan.mp4 --output wan_stable.mp4 [--window 13]
"""
from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np

_HAAR = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def _face_box(gray, last):
    dets = _HAAR.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
    return max(dets, key=lambda b: b[2] * b[3]) if len(dets) else last


def _face_metrics(frames_bgr, boxes):
    """Série luma visage (L*), flicker, variation %, netteté (variance Laplacien)."""
    lumas, sharps = [], []
    for fr, box in zip(frames_bgr, boxes):
        if box is None:
            continue
        x, y, w, h = box
        crop = fr[y:y + h, x:x + w]
        if crop.size == 0:
            continue
        L = cv2.cvtColor(crop, cv2.COLOR_BGR2LAB)[:, :, 0].astype(np.float32)
        lumas.append(float(L.mean()))
        g = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        sharps.append(float(cv2.Laplacian(g, cv2.CV_64F).var()))
    a = np.asarray(lumas, np.float32)
    mean = a.mean() if a.size else 1.0
    var_pct = float((a.max() - a.min()) / mean * 100) if a.size else 0.0
    flicker = float(np.mean(np.abs(np.diff(a)))) if a.size > 1 else 0.0
    return {"luma_variation_pct": round(var_pct, 2),
            "luma_flicker": round(flicker, 3),
            "sharpness": round(float(np.mean(sharps)), 2) if sharps else 0.0}


def stabilize(input_mp4, output_mp4, window=13):
    cap = cv2.VideoCapture(str(input_mp4))
    if not cap.isOpened():
        raise RuntimeError(f"illisible : {input_mp4}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frames, boxes, lumas = [], [], []
    last = None
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        last = _face_box(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), last)
        frames.append(fr)
        boxes.append(last)
        if last is not None:
            x, y, bw, bh = last
            crop = fr[y:y + bh, x:x + bw]
            lumas.append(cv2.cvtColor(crop, cv2.COLOR_BGR2LAB)[:, :, 0].mean()
                         if crop.size else np.nan)
        else:
            lumas.append(np.nan)
    cap.release()
    if not frames:
        raise RuntimeError("aucune frame")

    before = _face_metrics(frames, boxes)

    # Cible = moyenne glissante centrée de la luma visage (garde les arcs lents,
    # tue le flicker). On comble les NaN par interpolation.
    s = np.asarray(lumas, np.float32)
    idx = np.arange(len(s))
    good = ~np.isnan(s)
    if good.sum() >= 2:
        s = np.interp(idx, idx[good], s[good])
    else:
        s = np.nan_to_num(s, nan=float(np.nanmean(s)) if good.any() else 128.0)
    k = max(3, window | 1)
    pad = k // 2
    target = np.convolve(np.pad(s, pad, mode="edge"), np.ones(k) / k, "valid")

    out = cv2.VideoWriter(str(output_mp4), cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    stab = []
    for fr, cur, tgt in zip(frames, s, target):
        gain = float(np.clip(tgt / max(cur, 1e-3), 0.7, 1.4))  # gain borné = pas d'artefact
        sf = np.clip(fr.astype(np.float32) * gain, 0, 255).astype(np.uint8)
        out.write(sf)
        stab.append(sf)
    out.release()

    after = _face_metrics(stab, boxes)
    return before, after


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--window", type=int, default=13, help="fenêtre de lissage (frames)")
    a = ap.parse_args()
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    before, after = stabilize(a.input, a.output, a.window)
    print(f"[stabilize] → {a.output}")
    print(f"  variation luma visage : {before['luma_variation_pct']}% → {after['luma_variation_pct']}%  (cible ≤15%)")
    print(f"  flicker visage        : {before['luma_flicker']} → {after['luma_flicker']}")
    print(f"  netteté (Laplacien)   : {before['sharpness']} → {after['sharpness']}  (doit rester ~stable)")


if __name__ == "__main__":
    raise SystemExit(main())
