# Handoff Claude — RunPod FramePack YAWatch-LUNA

Date: 2026-06-20

## Objectif immédiat

Ludovic a créé un pod RunPod pour accélérer les générations FramePack.

But:

```text
Installer ComfyUI + FramePack sur RunPod
→ lancer ComfyUI
→ générer un clip Luna avec le workflow validé
→ appliquer le Quality Gate I2V
→ récupérer le MP4 + rapport
```

## État validé avant passation

### Local Windows

Windows a déjà validé:

- Wan GGUF produit des MP4 mais échoue au gate I2V.
- FramePack produit un MP4 et passe le gate I2V.
- Le Quality Gate I2V automatique est intégré au backend ComfyUI local.

Commits importants:

| Commit | Rôle |
|---|---|
| `a8a18fc` | ajoute les métriques objectives vidéo |
| `8100946` | ajoute le Quality Gate I2V automatique |
| `3e974ae` | branche le Quality Gate après génération ComfyUI |
| `7c84b9f` | ajoute le runbook RunPod corrigé |

### RunPod

Ludovic est dans Jupyter Lab:

```text
https://jotsbly8io8a5r-8888.proxy.runpod.net/lab
```

Pod affiché:

```text
dramatic_silver_orangutan
```

Template:

```text
Runpod PyTorch 2.8.0
runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404
```

Il a choisi le chemin:

```text
Pods
```

Consigne:

```text
Ne pas utiliser Serverless ni Cluster maintenant.
```

GPU recommandé:

```text
RTX 4090
```

Budget:

```text
Balance RunPod: $10.00
Auto-pay: disabled
```

Sécurité:

```text
MFA recommandée avant gros usage.
```

## Où cliquer dans Jupyter

Dans Jupyter Lab:

```text
Launcher → Other → Terminal
```

Puis coller le script d'installation ci-dessous.

## Script d'installation RunPod actuel

À coller dans le terminal Jupyter:

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

test -f diffusion_models/FramePackI2V_HY_fp8_e4m3fn.safetensors || wget -O diffusion_models/FramePackI2V_HY_fp8_e4m3fn.safetensors https://huggingface.co/Kijai/HunyuanVideo_comfy/resolve/main/FramePackI2V_HY_fp8_e4m3fn.safetensors

test -f vae/hunyuan_video_vae_bf16.safetensors || wget -O vae/hunyuan_video_vae_bf16.safetensors https://huggingface.co/Kijai/HunyuanVideo_comfy/resolve/main/hunyuan_video_vae_bf16.safetensors

test -f clip_vision/sigclip_vision_patch14_384.safetensors || wget -O clip_vision/sigclip_vision_patch14_384.safetensors https://huggingface.co/Kijai/HunyuanVideo_comfy/resolve/main/sigclip_vision_patch14_384.safetensors

test -f text_encoders/clip_l.safetensors || wget -O text_encoders/clip_l.safetensors https://huggingface.co/Kijai/HunyuanVideo_comfy/resolve/main/clip_l.safetensors

test -f text_encoders/llava_llama3_fp16.safetensors || wget -O text_encoders/llava_llama3_fp16.safetensors https://huggingface.co/Kijai/HunyuanVideo_comfy/resolve/main/llava_llama3_fp16.safetensors

cd /workspace/ComfyUI

cp /workspace/yawatch-luna-stories/docs/I2V_ENGINE_TESTS/FRAMEPACK_VS_WAN21_GGUF/workflows/framepack_plan02_luna_api_test_001.json user/default/workflows/

echo "INSTALL_OK"
echo "Ensuite lance : cd /workspace/ComfyUI && python main.py --listen 0.0.0.0 --port 8188"
```

## Lancer ComfyUI

Après `INSTALL_OK`:

```bash
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8188
```

Ensuite dans RunPod:

```text
Pods → pod dramatic_silver_orangutan → Connect → HTTP services → port 8188
```

Le lien doit ressembler à:

```text
https://<pod-id>-8188.proxy.runpod.net
```

## Workflow validé à charger

Workflow GitHub:

```text
docs/I2V_ENGINE_TESTS/FRAMEPACK_VS_WAN21_GGUF/workflows/framepack_plan02_luna_api_test_001.json
```

Copie attendue dans le pod:

```text
/workspace/ComfyUI/user/default/workflows/framepack_plan02_luna_api_test_001.json
```

## Image d'entrée

Pour le premier test, utiliser:

```text
luna.png
```

À mettre dans:

```text
/workspace/ComfyUI/input/luna.png
```

Si l'image n'est pas encore sur RunPod, la prendre depuis le repo local ou depuis GitHub, ou uploader via Jupyter Lab.

## Quality Gate I2V

Scripts:

```text
/workspace/yawatch-luna-stories/app/video_metrics_evaluator.py
/workspace/yawatch-luna-stories/app/i2v_quality_gate.py
```

Commande après génération:

```bash
cd /workspace/yawatch-luna-stories
python -m app.i2v_quality_gate /workspace/ComfyUI/output/YOUR_CLIP.mp4 \
  --output-json /workspace/ComfyUI/output/YOUR_CLIP.i2v_quality_gate.json
```

Seuils:

| Métrique | Seuil |
|---|---:|
| `face_identity_ssim_min` | `>= 0.85` |
| `face_lighting_peak_to_peak_pct` | `<= 15.0` |
| `face_flicker_mean_abs_delta` | `<= 0.5` |

Règle:

```text
PASS = clip techniquement montrable à Ludovic.
FAIL = clip rejeté avant validation humaine.
```

## Commandes utiles diagnostic pod

```bash
nvidia-smi
python --version
python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
df -h
du -sh /workspace/ComfyUI/models/* || true
```

## Règles importantes

1. Ne pas laisser le pod tourner après le test.
2. Ne pas activer auto-pay.
3. Ne pas conclure qu'un clip est validé artistiquement sans Ludovic.
4. Ne pas proposer Kling.
5. Ne pas contourner le Quality Gate I2V.

## Prochaine action exacte

Ludovic doit:

1. Cliquer `Terminal` dans Jupyter Lab.
2. Coller le script d'installation.
3. Attendre `INSTALL_OK`.
4. Lancer ComfyUI.
5. Ouvrir le port `8188`.
6. Charger le workflow FramePack.
7. Générer le premier MP4.
8. Lancer le Quality Gate.
9. Télécharger MP4 + `.i2v_quality_gate.json`.

## Si Codex plante

Claude doit reprendre depuis cette page et demander à Ludovic:

```text
Est-ce que tu vois INSTALL_OK dans le terminal RunPod ?
```

Si oui: lancer ComfyUI.

Si non: demander la dernière erreur visible dans le terminal.
