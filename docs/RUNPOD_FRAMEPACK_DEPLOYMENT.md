# RunPod FramePack Deployment — YAWatch-LUNA

Date: 2026-06-20

## Objectif

Déployer un atelier cloud temporaire pour générer les clips FramePack plus vite que la RTX 4060 locale, tout en gardant la même gouvernance:

```text
FramePack generation -> I2V Quality Gate -> human validation Ludovic
```

## Choix RunPod

Dans le dashboard RunPod:

```text
Recommended path: Pods
```

Ne pas choisir pour l'instant:

- `Serverless`: trop tôt tant que le workflow n'est pas industrialisé.
- `Clusters`: inutile et coûteux.
- `Public endpoints`: pas adapté à notre pipeline YAWatch.

## Sécurité obligatoire

Avant de déposer de l'argent:

1. Activer Multi-Factor Authentication.
2. Ajouter seulement un petit montant de test.
3. Éteindre le pod après usage.

## Configuration recommandée

| Paramètre | Valeur |
|---|---|
| GPU | RTX 4090 Community Cloud |
| Template | PyTorch CUDA récent ou ComfyUI récent |
| Container Disk | `30 GB` minimum |
| Network Volume | `50 GB` recommandé |
| Ports | HTTP `8188` |
| Budget test | `10 USD` maximum |

Pourquoi `50 GB` de volume:

- FramePack principal: ~16 GB;
- LLaVA text encoder: ~16 GB;
- VAE / CLIP / repo / outputs: plusieurs GB;
- marge pour outputs et cache.

## Script d'installation corrigé

À exécuter dans le terminal du pod:

```bash
set -e

cd /workspace

if [ ! -d yawatch-luna-stories ]; then
  git clone https://github.com/byakuyakutchiki/yawatch-luna-stories.git
fi

if [ ! -d ComfyUI ]; then
  git clone https://github.com/comfyanonymous/ComfyUI.git
fi

cd /workspace/ComfyUI
python -m pip install --upgrade pip
pip install -r requirements.txt

cd /workspace/ComfyUI/custom_nodes
if [ ! -d ComfyUI-FramePackWrapper ]; then
  git clone https://github.com/kijai/ComfyUI-FramePackWrapper.git
fi
if [ ! -d ComfyUI-VideoHelperSuite ]; then
  git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git
fi

cd /workspace/ComfyUI
pip install -r custom_nodes/ComfyUI-FramePackWrapper/requirements.txt || true
pip install -r custom_nodes/ComfyUI-VideoHelperSuite/requirements.txt || true

mkdir -p models/diffusion_models models/vae models/clip_vision models/text_encoders input user/default/workflows

cd /workspace/ComfyUI/models

test -f diffusion_models/FramePackI2V_HY_fp8_e4m3fn.safetensors || \
  wget -O diffusion_models/FramePackI2V_HY_fp8_e4m3fn.safetensors \
  https://huggingface.co/Kijai/HunyuanVideo_comfy/resolve/main/FramePackI2V_HY_fp8_e4m3fn.safetensors

test -f vae/hunyuan_video_vae_bf16.safetensors || \
  wget -O vae/hunyuan_video_vae_bf16.safetensors \
  https://huggingface.co/Kijai/HunyuanVideo_comfy/resolve/main/hunyuan_video_vae_bf16.safetensors

test -f clip_vision/sigclip_vision_patch14_384.safetensors || \
  wget -O clip_vision/sigclip_vision_patch14_384.safetensors \
  https://huggingface.co/Kijai/HunyuanVideo_comfy/resolve/main/sigclip_vision_patch14_384.safetensors

test -f text_encoders/clip_l.safetensors || \
  wget -O text_encoders/clip_l.safetensors \
  https://huggingface.co/Kijai/HunyuanVideo_comfy/resolve/main/clip_l.safetensors

test -f text_encoders/llava_llama3_fp16.safetensors || \
  wget -O text_encoders/llava_llama3_fp16.safetensors \
  https://huggingface.co/Kijai/HunyuanVideo_comfy/resolve/main/llava_llama3_fp16.safetensors

cd /workspace/ComfyUI

cp /workspace/yawatch-luna-stories/docs/I2V_ENGINE_TESTS/FRAMEPACK_VS_WAN21_GGUF/workflows/framepack_plan02_luna_api_test_001.json \
  user/default/workflows/

echo "INSTALL_OK"
echo "Launch with:"
echo "cd /workspace/ComfyUI && python main.py --listen 0.0.0.0 --port 8188"
```

## Lancement ComfyUI

```bash
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8188
```

Ensuite ouvrir le lien proxy RunPod du port `8188`.

## Workflow validé à utiliser

```text
docs/I2V_ENGINE_TESTS/FRAMEPACK_VS_WAN21_GGUF/workflows/framepack_plan02_luna_api_test_001.json
```

## Quality Gate cloud

Après génération, cloner le repo donne accès à:

```text
app/i2v_quality_gate.py
app/video_metrics_evaluator.py
```

Commande type:

```bash
cd /workspace/yawatch-luna-stories
python -m app.i2v_quality_gate /workspace/ComfyUI/output/YOUR_CLIP.mp4 \
  --output-json /workspace/ComfyUI/output/YOUR_CLIP.i2v_quality_gate.json
```

## Règles d'arrêt

Arrêter le pod si:

- ComfyUI ne démarre pas;
- les modèles ne se téléchargent pas;
- le premier MP4 ne passe pas le Quality Gate;
- le coût dépasse le budget test.

Toujours arrêter le pod après la session.
