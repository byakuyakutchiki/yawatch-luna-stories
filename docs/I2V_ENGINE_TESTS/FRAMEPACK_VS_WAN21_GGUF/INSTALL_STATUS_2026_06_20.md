# Install Status — 2026-06-20

## Objectif

Mettre a jour l'etat reel Windows apres installation du kit FramePack vs Wan2.1 GGUF.

## Etat machine

- ComfyUI root: `C:\Users\saint\Documents\Codex\ComfyUI`
- GPU: NVIDIA GeForce RTX 4060 Laptop GPU
- VRAM: 8 Go
- CUDA PyTorch: disponible
- Torch: `2.5.1+cu121`
- Espace libre avant installation FramePack: environ 160 Go

## Custom nodes installes

Installes dans `ComfyUI/custom_nodes/`:

- `ComfyUI-FramePackWrapper`
- `ComfyUI-GGUF`

Dependances Python installees dans le venv ComfyUI:

- requirements FramePackWrapper
- requirements ComfyUI-GGUF

## Modeles FramePack telecharges

Presents:

- `models/diffusion_models/FramePackI2V_HY_fp8_e4m3fn.safetensors`
- `models/vae/hunyuan_video_vae_bf16.safetensors`
- `models/clip_vision/sigclip_vision_patch14_384.safetensors`
- cache support: `models/_hf_cache/HunyuanVideo_repackaged`

Text encoders copies dans `models/text_encoders/`:

- `clip_l.safetensors`
- `llava_llama3_fp16.safetensors`

## Modeles Wan2.1 GGUF

Non encore telecharges au moment de ce rapport:

- `wan2.1-i2v-14b-480p-Q5_K_S.gguf`: absent
- `wan2.1-i2v-14b-480p-Q4_K_S.gguf`: absent
- support cache Wan: absent

## Verification ComfyUI

ComfyUI a ete lance sur:

```text
http://127.0.0.1:8188
```

`/object_info` repond.

Nombre de noeuds detectes: `1027`.

Noeuds pertinents detectes:

- `LoadFramePackModel`
- `DownloadAndLoadFramePackModel`
- `FramePackSampler`
- `FramePackSingleFrameSampler`
- `FramePackFindNearestBucket`
- `CLIPLoaderGGUF`
- `DualCLIPLoaderGGUF`
- `TripleCLIPLoaderGGUF`
- `QuadrupleCLIPLoaderGGUF`
- `UnetLoaderGGUF`
- `UnetLoaderGGUFAdvanced`
- `WanImageToVideo`

## Point de blocage actuel

Le workflow officiel FramePack fourni dans `ComfyUI-FramePackWrapper/example_workflows/framepack_hv_example.json` depend de noeuds annexes qui ne sont pas tous presents dans l'installation actuelle:

- `ImageResize+`: absent
- `GetImageSizeAndCount`: absent
- `SetNode`: absent
- `GetNode`: absent

Ces noeuds viennent probablement de packs utilitaires additionnels. Il ne faut donc pas declarer le workflow officiel executable tel quel avant installation ou remplacement de ces noeuds.

## Etat decisionnel

FramePack est installe cote modeles et noeuds principaux, mais pas encore valide en production.

Statut FramePack:

```text
INSTALLED_NOT_GENERATED
```

Wan2.1 GGUF:

```text
NOT_DOWNLOADED
```

## Prochaine action concrete

Choisir une des deux options:

1. Installer les noeuds utilitaires manquants pour faire tourner le workflow officiel FramePack.
2. Construire un workflow API minimal uniquement avec les noeuds deja presents:
   - `LoadImage`
   - `ImageScale`
   - `DualCLIPLoader`
   - `CLIPTextEncode`
   - `ConditioningZeroOut`
   - `CLIPVisionLoader`
   - `CLIPVisionEncode`
   - `VAELoader`
   - `VAEEncode`
   - `LoadFramePackModel`
   - `FramePackSampler`
   - `VAEDecodeTiled`
   - `VHS_VideoCombine`

Regle: aucune generation FramePack ne doit etre declaree valide tant qu'un MP4 n'a pas ete produit, visionne et note dans `EVALUATION_SHEET.md`.

