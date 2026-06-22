#!/usr/bin/env bash
# ============================================================================
# Entraînement LoRA Luna sur Wan2.1 via musubi-tuner (action B).
# ----------------------------------------------------------------------------
# CHAÎNE VALIDÉE le 22 juin sur t2v-1.3B (L4) : install -> dataset -> cache
# latents -> cache text-encoder -> train -> .safetensors (84 Mo). 2 corrections
# apprises (intégrées ici) :
#   1) T5 = modèle Wan NATIF `models_t5_umt5-xxl-enc-bf16.pth` (PAS le umt5 Comfy
#      fp8 : format de clés incompatible avec musubi).
#   2) --mixed_precision DOIT matcher le dtype du DiT : DiT fp16 -> fp16.
#
# TASK : t2v-1.3B = run de validation (cheap, rapide). t2v-14B / i2v-14B = run
# de production (lourd : DiT ~14-28 Go, plusieurs heures, GPU costaud conseillé).
# Pour le 14B : VRAM tendue -> tester --fp8_base + --blocks_to_swap (et ajuster
# --mixed_precision en conséquence) ; à valider sur le run 14B.
#
# Usage : TASK=t2v-1.3B bash tools/runpod/train_lora_luna.sh
# ============================================================================
set -euo pipefail
PY=python
REPO=/workspace/yawatch-luna-stories
MT=/workspace/musubi-tuner
BASE=/workspace/wanbase
OUT=/workspace/lora
DS="$REPO/tools/runpod/luna_dataset.toml"
TASK="${TASK:-t2v-1.3B}"
HF=https://huggingface.co
COMFY="$HF/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files"
mkdir -p "$BASE" "$OUT"

dl() { [ -f "$2" ] && [ "$(stat -c%s "$2")" -gt 100000000 ] && { echo "skip $(basename "$2")"; return; }; curl -fL --retry 3 -o "$2" "$1"; }

echo "== 1. dataset =="
cd "$REPO" && $PY tools/prepare_lora_dataset.py --size 768 --trigger lunaw | tail -2

echo "== 2. musubi-tuner =="
[ -d "$MT/.git" ] || git clone --depth 1 https://github.com/kohya-ss/musubi-tuner "$MT"
cd "$MT" && $PY -m pip install -q --break-system-packages -e . 2>&1 | tail -2

echo "== 3. modèles de base ($TASK) =="
# T5 Wan NATIF (commun à toutes les tâches) + VAE
dl "$HF/Wan-AI/Wan2.1-T2V-1.3B/resolve/main/models_t5_umt5-xxl-enc-bf16.pth" "$BASE/t5.pth"
dl "$COMFY/vae/wan_2.1_vae.safetensors" "$BASE/vae.safetensors"
CACHE_EXTRA=""
if [ "$TASK" = "t2v-1.3B" ]; then
  dl "$COMFY/diffusion_models/wan2.1_t2v_1.3B_fp16.safetensors" "$BASE/dit.safetensors"; MP=fp16; EXTRA=""
elif [ "$TASK" = "t2v-14B" ]; then
  dl "$COMFY/diffusion_models/wan2.1_t2v_14B_fp16.safetensors" "$BASE/dit.safetensors"; MP=fp16; EXTRA=""
elif [ "$TASK" = "i2v-14B" ]; then
  dl "$COMFY/diffusion_models/wan2.1_i2v_480p_14B_fp16.safetensors" "$BASE/dit.safetensors"
  # CLIP Wan NATIF (.pth) — le clip_vision_h Comfy a un format incompatible musubi (XLMRobertaCLIP)
  dl "$HF/Wan-AI/Wan2.1-I2V-14B-480P/resolve/main/models_clip_open-clip-xlm-roberta-large-vit-huge-14.pth" "$BASE/clip_native.pth"
  # i2v EXIGE le cache des latents AVEC --i2v --clip (sinon KeyError 'latents_image' au step 0)
  MP=fp16; EXTRA="--clip $BASE/clip_native.pth"; CACHE_EXTRA="--i2v --clip $BASE/clip_native.pth"
else echo "TASK inconnu: $TASK"; exit 1; fi

echo "== 4. cache latents + text encoder =="
cd "$MT"
$PY src/musubi_tuner/wan_cache_latents.py --dataset_config "$DS" --vae "$BASE/vae.safetensors" $CACHE_EXTRA
$PY src/musubi_tuner/wan_cache_text_encoder_outputs.py --dataset_config "$DS" --t5 "$BASE/t5.pth" --batch_size 1

echo "== 5. entraînement LoRA ($TASK, mixed_precision=$MP) =="
accelerate launch --num_processes 1 --mixed_precision "$MP" src/musubi_tuner/wan_train_network.py \
  --task "$TASK" \
  --dit "$BASE/dit.safetensors" --vae "$BASE/vae.safetensors" --t5 "$BASE/t5.pth" $EXTRA \
  --dataset_config "$DS" \
  --network_module networks.lora_wan --network_dim 32 --network_alpha 16 \
  --learning_rate 1e-4 --max_train_epochs 16 \
  --mixed_precision "$MP" --gradient_checkpointing --sdpa \
  --optimizer_type adamw --max_data_loader_n_workers 1 \
  --output_dir "$OUT" --output_name luna_lunaw --save_every_n_steps 200 --seed 42
# NB run 22/06 : figé à la frontière epoch 4 (deadlock dataloader). Parades intégrées :
#   --max_data_loader_n_workers 1 (évite le deadlock) + --save_every_n_steps 200
#   (checkpoint régulier même si ça gèle). Checkpoint epoch4 (832 steps) = luna_lora_e4.

echo "== TERMINÉ → $OUT/luna_lunaw.safetensors =="
