#!/usr/bin/env bash
# ============================================================================
# Entraînement LoRA Luna sur Wan2.1 14B — via musubi-tuner (action B).
# ----------------------------------------------------------------------------
# ⚠️ BLEEDING-EDGE : LoRA vidéo Wan = outillage récent. Ce script suit le flux
# documenté de musubi-tuner (kohya). À VALIDER/ajuster sur le pod (versions,
# noms de flags). VRAM 14B tendu → fp8_base + block swap pour tenir en 32 Go.
# Coût réaliste : download base Wan (~28 Go si absent) + entraînement plusieurs
# heures → compter quelques € de pod, PAS « 1,50 € ».
#
# Pré-requis : modèles Wan de base présents (cf. provision.sh / volume persistant) :
#   diffusion_models/wan2.1_t2v_14B_fp16 (ou i2v), vae/wan_2.1_vae,
#   text_encoders/umt5_xxl, clip_vision/clip_vision_h.
#
# Usage (pod) :  bash tools/runpod/train_lora_luna.sh
# ============================================================================
set -euo pipefail
PY=python
REPO=/workspace/yawatch-luna-stories
M=/workspace/ComfyUI/models
MT=/workspace/musubi-tuner
OUT=/workspace/lora
mkdir -p "$OUT"

echo "== 1. dataset =="
cd "$REPO" && $PY tools/prepare_lora_dataset.py --size 768 --trigger lunaw

echo "== 2. musubi-tuner =="
if [ ! -d "$MT/.git" ]; then git clone https://github.com/kohya-ss/musubi-tuner "$MT"; fi
cd "$MT" && $PY -m pip install -q --break-system-packages -e . 2>&1 | tail -3 || true

# Modèles de base (chemins à adapter à ce qui est sur le volume)
DIT="$M/diffusion_models/wan2.1_t2v_14B_fp8_e4m3fn.safetensors"   # ou i2v selon la cible
VAE="$M/vae/wan_2.1_vae.safetensors"
T5="$M/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors"
DS="$REPO/tools/runpod/luna_dataset.toml"

echo "== 3. cache latents + text encoder =="
$PY src/musubi_tuner/wan_cache_latents.py --dataset_config "$DS" --vae "$VAE"
$PY src/musubi_tuner/wan_cache_text_encoder_outputs.py --dataset_config "$DS" --t5 "$T5" --batch_size 1

echo "== 4. entraînement LoRA =="
accelerate launch --num_processes 1 src/musubi_tuner/wan_train_network.py \
  --task t2v-14B \
  --dit "$DIT" --vae "$VAE" --t5 "$T5" \
  --dataset_config "$DS" \
  --network_module networks.lora_wan --network_dim 32 --network_alpha 16 \
  --learning_rate 1e-4 --max_train_epochs 16 \
  --mixed_precision bf16 --fp8_base --blocks_to_swap 20 \
  --gradient_checkpointing --sdpa \
  --optimizer_type adamw8bit \
  --output_dir "$OUT" --output_name luna_lunaw \
  --save_every_n_epochs 4 --seed 42

echo "== TERMINÉ → $OUT/luna_lunaw.safetensors =="
