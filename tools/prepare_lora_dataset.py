#!/usr/bin/env python3
"""Prépare le dataset LoRA Luna (action B) — images + captions trigger.

Collecte les images Luna adulte canoniques, les redimensionne (côté long ≤ taille
cible, aspect conservé) et écrit une caption par image avec un MOT-DÉCLENCHEUR.
Pour un LoRA de personnage, on garde la caption courte et centrée sur Luna (pas
le décor) pour que le modèle lie l'identité au trigger.

Sortie : dataset/luna_lora/ (images .png + .txt), prêt pour musubi-tuner.
Regénérable (sur VM ou pod) — pas besoin de versionner le dataset lui-même.

Usage : python tools/prepare_lora_dataset.py [--size 768] [--trigger lunaw]
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

_REPO = Path(__file__).resolve().parents[1]
_SRC = _REPO / "assets" / "luna_stories_assets"
# Sources Luna adulte (canon). On exclut enfant / secondaires / décors.
_DIRS = [_SRC / "01_luna_adulte"]
_EXTRA = [_SRC / "00_assets_deja_dans_app" / "app_luna_adulte_avatar_current.jpg"]

# Contexte léger par mot-clé du nom de fichier (aide la flexibilité sans bake le fond)
_CTX = {
    "neutral": "neutral expression", "worried": "worried expression",
    "determination": "determined expression", "ceo": "business attire",
    "office": "in an office", "window": "looking outside",
    "photo": "holding a photo", "doll": "holding a doll", "reference": "studio portrait",
    "avatar": "portrait",
}


def _caption(name: str, trigger: str) -> str:
    low = name.lower()
    ctx = next((v for k, v in _CTX.items() if k in low), "")
    return f"{trigger}, a young adult woman" + (f", {ctx}" if ctx else "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=768, help="côté long max")
    ap.add_argument("--trigger", default="lunaw", help="mot déclencheur (rare)")
    ap.add_argument("--out", default=str(_REPO / "dataset" / "luna_lora"))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    srcs = []
    for d in _DIRS:
        srcs += sorted([p for p in d.glob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg")])
    srcs += [p for p in _EXTRA if p.exists()]
    # exclure les sous-dossiers candidates/non_canon déjà évités par glob non récursif

    n = 0
    for p in srcs:
        try:
            im = Image.open(p).convert("RGB")
        except Exception as e:  # noqa: BLE001
            print(f"  skip {p.name}: {e}"); continue
        w, h = im.size
        scale = a.size / max(w, h)
        if scale < 1:
            im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        stem = f"{n:03d}_{p.stem}"
        im.save(out / f"{stem}.png")
        (out / f"{stem}.txt").write_text(_caption(p.name, a.trigger), encoding="utf-8")
        n += 1
        print(f"  [{n}] {p.name} -> {im.size}  | {_caption(p.name, a.trigger)}")

    print(f"\n✅ {n} images préparées dans {out}")
    if n < 20:
        print(f"⚠️  {n} images = un peu juste pour un LoRA robuste (idéal 20-40). "
              "Premier LoRA de test OK ; en générer plus améliorera l'identité.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
