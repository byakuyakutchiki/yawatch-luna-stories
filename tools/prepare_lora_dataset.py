#!/usr/bin/env python3
"""Prépare + densifie le dataset LoRA Luna (action B).

Sources : UNIQUEMENT Luna adulte SOLO, visage visible (on EXCLUT Aby/Malik/enfant
/multi-perso/non-canon — sinon le LoRA apprend les mauvais visages).

Densification (dataset réel mince) : pour chaque image, on ajoute un RECADRAGE
VISAGE (Haar) et des MIROIRS → renforce l'apprentissage de l'identité.
⚠️ Honnête : ce sont des augmentations des MÊMES visages (focalise l'identité),
pas de nouvelles prises de vue. Pour de vrais angles en plus → générer/photographier.

Sortie : dataset/luna_lora/ (png + .txt trigger). Régénérable.
Usage : python tools/prepare_lora_dataset.py [--size 768] [--trigger lunaw] [--no-augment]
"""
from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

_REPO = Path(__file__).resolve().parents[1]
_SRC = _REPO / "assets" / "luna_stories_assets"

# Liste CURÉE de Luna adulte solo (canon). On nomme explicitement pour éviter
# d'aspirer Aby/Malik/scènes multi-perso.
_LUNA_SOLO = [
    _SRC / "01_luna_adulte" / "luna_adulte_ceo_01.png",
    _SRC / "01_luna_adulte" / "luna_adulte_ceo_02_landscape.png",
    _SRC / "01_luna_adulte" / "luna_adulte_ceo_03_portrait.png",
    _SRC / "01_luna_adulte" / "luna_adulte_determination_9x16_01.png",
    _SRC / "01_luna_adulte" / "luna_adulte_looking_at_turned_photo_01.png",
    _SRC / "01_luna_adulte" / "luna_adulte_looking_out_window_01.png",
    _SRC / "01_luna_adulte" / "luna_adulte_neutral_9x16_01.png",
    _SRC / "01_luna_adulte" / "luna_adulte_office_desk_01.png",
    _SRC / "01_luna_adulte" / "luna_adulte_protective_luna_doll_01.png",
    _SRC / "01_luna_adulte" / "luna_adulte_reference_realiste_01.jpg",
    _SRC / "01_luna_adulte" / "luna_adulte_worried_9x16_01.png",
    _SRC / "00_assets_deja_dans_app" / "app_luna_adulte_avatar_current.jpg",
    # Luna-solo de visuels clés (scènes — visage extrait si détecté) :
    _SRC / "08_visuels_cles" / "ep01_luna_seule_bureau_nuit_cadre_en_main_01.png",
    _SRC / "08_visuels_cles" / "ep01_luna_consulte_historique_yawatch_01.png",
]

_CTX = {"neutral": "neutral expression", "worried": "worried expression",
        "determination": "determined expression", "ceo": "business attire",
        "office": "in an office", "window": "looking outside", "photo": "holding a photo",
        "doll": "holding a doll", "reference": "studio portrait", "avatar": "portrait",
        "bureau": "in an office at night", "historique": "at a screen"}

_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def _caption(name: str, trigger: str) -> str:
    low = name.lower()
    ctx = next((v for k, v in _CTX.items() if k in low), "")
    return f"{trigger}, a young adult woman" + (f", {ctx}" if ctx else "")


def _resize(im: Image.Image, size: int) -> Image.Image:
    w, h = im.size
    s = size / max(w, h)
    return im.resize((round(w * s), round(h * s)), Image.LANCZOS) if s < 1 else im


def _face_crop(im: Image.Image):
    """Recadrage visage padé (40%) si un visage est détecté, sinon None."""
    bgr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    dets = _CASCADE.detectMultiScale(g, 1.1, 5, minSize=(60, 60))
    if len(dets) == 0:
        return None
    x, y, w, h = max(dets, key=lambda b: b[2] * b[3])
    px, py = int(w * 0.4), int(h * 0.4)
    W, H = im.size
    box = (max(0, x - px), max(0, y - py), min(W, x + w + px), min(H, y + h + py))
    return im.crop(box)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=768)
    ap.add_argument("--trigger", default="lunaw")
    ap.add_argument("--no-augment", action="store_true")
    ap.add_argument("--out", default=str(_REPO / "dataset" / "luna_lora"))
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    augment = not a.no_augment
    n = 0

    def emit(img: Image.Image, name: str):
        nonlocal n
        img = _resize(img, a.size)
        img.save(out / f"{n:03d}_{name}.png")
        (out / f"{n:03d}_{name}.txt").write_text(_caption(name, a.trigger), encoding="utf-8")
        n += 1

    for p in _LUNA_SOLO:
        if not p.exists():
            print(f"  (absent) {p.name}"); continue
        try:
            im = Image.open(p).convert("RGB")
        except Exception as e:  # noqa: BLE001
            print(f"  skip {p.name}: {e}"); continue
        emit(im, p.stem)                                   # image complète
        fc = _face_crop(im)
        if fc is not None:
            emit(fc, p.stem + "_face")                     # recadrage visage
        if augment:
            emit(im.transpose(Image.FLIP_LEFT_RIGHT), p.stem + "_flip")
            if fc is not None:
                emit(fc.transpose(Image.FLIP_LEFT_RIGHT), p.stem + "_face_flip")
        print(f"  ok {p.name}  (face={'oui' if fc is not None else 'non'})")

    print(f"\n✅ {n} échantillons dans {out}  (originaux + visages + miroirs)")
    print("⚠️ Augmentation = mêmes visages re-cadrés/mirroir (focalise l'identité), "
          "pas de nouveaux angles. Pour un LoRA vraiment fort → plus de vraies prises.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
