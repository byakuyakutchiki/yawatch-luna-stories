"""Restauration de visage post-I2V (étage 2 du pipeline « Kling maison »).

But : récupérer l'identité/la netteté du visage après une génération vivante
(Wan) qui dérive. C'est l'étage 2 ; l'étage 1 (mouvement) reste FramePack/Wan.

Backends :
  • gfpgan    — robuste, pip-installable, auto-télécharge ses poids. DÉFAUT.
  • codeformer— meilleur sur l'identité d'après la litté, mais install fragile
                (repo + basicsr/torch). Branché si présent, sinon message clair.

⚠️ Limites honnêtes :
  - Restauration FRAME PAR FRAME → risque de scintillement temporel. On le
    MESURE (flicker) au lieu de le supposer.
  - GFPGAN/CodeFormer restaurent un *beau* visage générique : ils corrigent la
    QUALITÉ, pas forcément l'IDENTITÉ-Luna. Pour ré-ancrer vers le Luna canonique,
    c'est un face-swap référencé (ReActor/InstantID) — backend 'reactor' à venir.

Usage (sur le pod, GPU) :
    from app.yawatch_video_engine.face_restore import restore_video_faces
    restore_video_faces("in.mp4", "out.mp4", backend="gfpgan", fidelity=0.7)
"""
from __future__ import annotations

import os
from pathlib import Path

# Poids GFPGAN officiels (auto-téléchargés si absents).
_GFPGAN_URL = ("https://github.com/TencentARC/GFPGAN/releases/download/"
               "v1.3.0/GFPGANv1.4.pth")


def _load_gfpgan(fidelity: float):
    """Charge GFPGANer (lazy : n'importe rien tant qu'on n'appelle pas)."""
    import torch
    from gfpgan import GFPGANer
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return GFPGANer(
        model_path=_GFPGAN_URL,
        upscale=1,                 # on garde la résolution source
        arch="clean",
        channel_multiplier=2,
        bg_upsampler=None,         # pas d'upscale du fond (on veut juste le visage)
        device=device,
    )


def restore_video_faces(input_mp4: str | Path, output_mp4: str | Path,
                        backend: str = "gfpgan", fidelity: float = 0.7) -> Path:
    """Restaure les visages frame par frame et réassemble la vidéo.

    fidelity : 0 = restauration agressive, 1 = fidèle à la source (CodeFormer).
    Retourne le chemin du MP4 restauré (mêmes dimensions/fps que la source).
    """
    import cv2  # lazy
    input_mp4, output_mp4 = Path(input_mp4), Path(output_mp4)
    output_mp4.parent.mkdir(parents=True, exist_ok=True)

    if backend == "gfpgan":
        restorer = _load_gfpgan(fidelity)
        def restore(frame_bgr):
            _, _, out = restorer.enhance(frame_bgr, has_aligned=False,
                                         only_center_face=False, paste_back=True)
            return out if out is not None else frame_bgr
    elif backend == "codeformer":
        restore = _load_codeformer(fidelity)
    else:
        raise ValueError(f"Backend de restauration inconnu : {backend!r} "
                         "(attendu 'gfpgan' ou 'codeformer').")

    cap = cv2.VideoCapture(str(input_mp4))
    if not cap.isOpened():
        raise RuntimeError(f"Impossible d'ouvrir : {input_mp4}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter(str(output_mp4), cv2.VideoWriter_fourcc(*"mp4v"),
                             fps, (w, h))
    n = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            writer.write(restore(frame))
            n += 1
    finally:
        cap.release()
        writer.release()
    if n == 0:
        raise RuntimeError(f"Aucune frame décodée : {input_mp4}")
    print(f"[face_restore] {backend} : {n} frames restaurées → {output_mp4}")
    return output_mp4


def _load_codeformer(fidelity: float):
    """Backend CodeFormer (réel) — nécessite facexlib + l'arch CodeFormer.

    On ne l'active que si les dépendances sont là, sinon message explicite
    (pas de fallback silencieux).
    """
    try:
        import torch
        from torchvision.transforms.functional import normalize
        from facexlib.utils.face_restoration_helper import FaceRestoreHelper
        from basicsr.utils import img2tensor, tensor2img
        from basicsr.archs.codeformer_arch import CodeFormer  # repo CodeFormer requis
        from basicsr.utils.download_util import load_file_from_url
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            "Backend CodeFormer indisponible : "
            f"dépendances manquantes ({exc}). Installer le repo CodeFormer + "
            "facexlib, ou utiliser backend='gfpgan'."
        ) from exc

    import numpy as np  # noqa: F401
    device = "cuda" if torch.cuda.is_available() else "cpu"
    ckpt = load_file_from_url(
        "https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth",
        model_dir=os.path.expanduser("~/.cache/codeformer"))
    net = CodeFormer(dim_embd=512, codebook_size=1024, n_head=8, n_layers=9,
                     connect_list=["32", "64", "128", "256"]).to(device)
    net.load_state_dict(torch.load(ckpt, map_location=device)["params_ema"])
    net.eval()
    helper = FaceRestoreHelper(1, face_size=512, crop_ratio=(1, 1),
                               det_model="retinaface_resnet50", device=device)

    def restore(frame_bgr):
        import cv2
        helper.clean_all()
        helper.read_image(frame_bgr)
        helper.get_face_landmarks_5(only_center_face=False, resize=640)
        helper.align_warp_face()
        for cropped in helper.cropped_faces:
            t = img2tensor(cropped / 255.0, bgr2rgb=True, float32=True)
            normalize(t, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5), inplace=True)
            t = t.unsqueeze(0).to(device)
            with torch.no_grad():
                out = net(t, w=fidelity, adain=True)[0]
                restored = tensor2img(out, rgb2bgr=True, min_max=(-1, 1))
            helper.add_restored_face(restored.astype("uint8"))
        helper.get_inverse_affine(None)
        return helper.paste_faces_to_input_image()

    return restore
