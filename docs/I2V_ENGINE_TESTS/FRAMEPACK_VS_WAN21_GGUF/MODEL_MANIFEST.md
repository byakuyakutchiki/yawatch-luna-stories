# Model Manifest — FramePack vs Wan2.1 GGUF

## Sources officielles ou prioritaires

FramePack:

- Official FramePack repository: https://github.com/lllyasviel/FramePack
- ComfyUI wrapper: https://github.com/kijai/ComfyUI-FramePackWrapper
- Kijai HunyuanVideo Comfy models: https://huggingface.co/Kijai/HunyuanVideo_comfy
- Comfy-Org HunyuanVideo repackaged: https://huggingface.co/Comfy-Org/HunyuanVideo_repackaged
- Comfy-Org SigCLIP 384: https://huggingface.co/Comfy-Org/sigclip_vision_384

Wan2.1 GGUF:

- ComfyUI-GGUF: https://github.com/city96/ComfyUI-GGUF
- city96 Wan2.1 I2V 14B 480P GGUF: https://huggingface.co/city96/Wan2.1-I2V-14B-480P-gguf
- Comfy-Org Wan 2.1 repackaged support files: https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged

## FramePack — fichiers cibles

| Priorite | Repo HF | Fichier ou dossier | Destination ComfyUI | Statut |
|---|---|---|---|---|
| P0 | `Kijai/HunyuanVideo_comfy` | `FramePackI2V_HY_fp8_e4m3fn.safetensors` | `models/diffusion_models/` | requis |
| P0 | `Kijai/HunyuanVideo_comfy` | `hunyuan_video_vae_bf16.safetensors` | `models/vae/` | requis |
| P0 | `Comfy-Org/sigclip_vision_384` | `sigclip_vision_patch14_384.safetensors` | `models/clip_vision/` | requis |
| P1 | `Comfy-Org/HunyuanVideo_repackaged` | `split_files/text_encoders/` | `models/text_encoders/` | requis selon workflow |
| P1 | `Comfy-Org/HunyuanVideo_repackaged` | `split_files/clip_vision/` | `models/clip_vision/` | requis selon workflow |

Note: le wrapper Kijai peut aussi autodownloader depuis `lllyasviel/FramePackI2V_HY`, mais YAWatch prefere les fichiers locaux explicites pour audit et reproductibilite.

## Wan2.1 GGUF — fichiers cibles

| Priorite | Repo HF | Fichier ou dossier | Destination ComfyUI | Statut |
|---|---|---|---|---|
| P0 | `city96/Wan2.1-I2V-14B-480P-gguf` | `wan2.1-i2v-14b-480p-Q5_K_S.gguf` | `models/unet/` | candidat qualite |
| P0 fallback | `city96/Wan2.1-I2V-14B-480P-gguf` | `wan2.1-i2v-14b-480p-Q4_K_S.gguf` | `models/unet/` | si Q5 manque de VRAM |
| P0 | `Comfy-Org/Wan_2.1_ComfyUI_repackaged` | `split_files/text_encoders/` | `models/text_encoders/` | requis |
| P0 | `Comfy-Org/Wan_2.1_ComfyUI_repackaged` | `split_files/clip_vision/` | `models/clip_vision/` | requis |
| P0 | `Comfy-Org/Wan_2.1_ComfyUI_repackaged` | `split_files/vae/` | `models/vae/` | requis |

## Contraintes disque

Prevoir au minimum:

- FramePack: environ 25 a 35 Go selon dependances exactes.
- Wan2.1 GGUF Q5 + support files: environ 25 a 35 Go.
- Les deux ensemble: viser 70 Go libres pour garder logs, outputs, caches et essais rejetes.

## Regle de telechargement

Ne jamais telecharger depuis des sites clones ou commerciaux non officiels. FramePack signale explicitement que les sites de type `framepack.*` non officiels sont a eviter.

