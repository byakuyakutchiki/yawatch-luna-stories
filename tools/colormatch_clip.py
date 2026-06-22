#!/usr/bin/env python3
"""Color-match d'un clip face-swappé vers l'éclairage d'un clip de référence.

Problème résolu : après un face-swap, le visage inséré n'a pas la couleur /
l'exposition de la scène (effet « visage collé »). On transfère les statistiques
couleur (L*a*b* moyenne/écart-type) de la zone visage du clip de RÉFÉRENCE (le
Wan original, bien éclairé) sur la zone visage du clip CONTENU (le face-swap).

→ On garde l'IDENTITÉ du swap + on récupère la LUMIÈRE de la scène.

CPU pur (cv2 + Haar). Les 2 clips doivent être alignés frame-à-frame (le
face-swap est dérivé du clip Wan, donc c'est le cas).

Usage :
    python tools/colormatch_clip.py --content faceswap.mp4 --reference wan.mp4 \
        --output faceswap_colormatch.mp4
"""
from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np

_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def _detect(gray, last):
    dets = _CASCADE.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
    if len(dets) > 0:
        return max(dets, key=lambda b: b[2] * b[3])
    return last


def _feather_mask(h, w):
    """Masque elliptique adouci (évite les bords nets du rectangle)."""
    m = np.zeros((h, w), np.float32)
    cv2.ellipse(m, (w // 2, h // 2), (int(w * 0.42), int(h * 0.48)), 0, 0, 360, 1, -1)
    k = max(3, (min(h, w) // 6) | 1)
    return cv2.GaussianBlur(m, (k, k), 0)[..., None]


def _lab_transfer(content_bgr, ref_bgr):
    """Transfère moyenne/écart-type L*a*b* de ref vers content."""
    c = cv2.cvtColor(content_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    r = cv2.cvtColor(ref_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    out = c.copy()
    for i in range(3):
        cm, cs = c[..., i].mean(), c[..., i].std() + 1e-6
        rm, rs = r[..., i].mean(), r[..., i].std() + 1e-6
        out[..., i] = (c[..., i] - cm) / cs * rs + rm
    out = np.clip(out, 0, 255).astype(np.uint8)
    return cv2.cvtColor(out, cv2.COLOR_LAB2BGR)


def colormatch(content_mp4, reference_mp4, output_mp4):
    cc = cv2.VideoCapture(str(content_mp4))
    rc = cv2.VideoCapture(str(reference_mp4))
    if not cc.isOpened() or not rc.isOpened():
        raise RuntimeError("clip illisible")
    fps = cc.get(cv2.CAP_PROP_FPS) or 25.0
    w = int(cc.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cc.get(cv2.CAP_PROP_FRAME_HEIGHT))
    Path(output_mp4).parent.mkdir(parents=True, exist_ok=True)
    out = cv2.VideoWriter(str(output_mp4), cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    last = None
    n = 0
    while True:
        okc, cf = cc.read()
        okr, rf = rc.read()
        if not okc:
            break
        if okr:
            box = _detect(cv2.cvtColor(rf, cv2.COLOR_BGR2GRAY), last)
            last = box
        else:
            box = last
        if box is not None:
            x, y, bw, bh = box
            # marge autour du visage pour englober le cou (raccord de teint)
            x0, y0 = max(0, x - bw // 6), max(0, y - bh // 6)
            x1, y1 = min(w, x + bw + bw // 6), min(h, y + bh + bh // 2)
            c_roi, r_roi = cf[y0:y1, x0:x1], (rf[y0:y1, x0:x1] if okr else cf[y0:y1, x0:x1])
            if c_roi.size and r_roi.size and c_roi.shape == r_roi.shape:
                matched = _lab_transfer(c_roi, r_roi)
                mask = _feather_mask(c_roi.shape[0], c_roi.shape[1])
                cf[y0:y1, x0:x1] = (matched * mask + c_roi * (1 - mask)).astype(np.uint8)
        out.write(cf)
        n += 1
    cc.release(); rc.release(); out.release()
    print(f"[colormatch] {n} frames → {output_mp4}")
    return output_mp4


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content", required=True, help="clip face-swappé (identité)")
    ap.add_argument("--reference", required=True, help="clip d'origine (lumière correcte)")
    ap.add_argument("--output", required=True)
    a = ap.parse_args()
    colormatch(a.content, a.reference, a.output)


if __name__ == "__main__":
    raise SystemExit(main())
