#!/usr/bin/env bash
# ============================================================================
# YAWatch-LUNA — Provisioning idempotent du pod RunPod (comparaison moteur I2V)
# ----------------------------------------------------------------------------
# Installe sur un pod VIERGE : ComfyUI + custom nodes + modèles FramePack & Wan
# NATIF fp16 + le repo gouverné. Conçu pour la RTX PRO 4500 (32 GB), Blackwell.
#
# Idempotent : relançable sans tout retélécharger (skip si déjà présent + taille
# correcte). GARDE-FOU anti-404 silencieux : tout fichier trop petit = ÉCHEC
# bruyant (les sources du runbook d'origine renvoyaient des fichiers 0 octet).
#
# Usage (sur le pod) :  bash provision.sh
# ============================================================================
set -euo pipefail

PY=/usr/local/bin/python            # interpréteur de ComfyUI (PAS python3 système)
WORK=/workspace
COMFY="$WORK/ComfyUI"
REPO="$WORK/yawatch-luna-stories"
MODELS="$COMFY/models"
REPO_URL="https://github.com/byakuyakutchiki/yawatch-luna-stories.git"
REPO_BRANCH="${REPO_BRANCH:-feat/governed-i2v-engines}"   # branche gouvernance/moteurs

log() { echo -e "\n\033[1;36m[provision] $*\033[0m"; }
die() { echo -e "\033[1;31m[ÉCHEC] $*\033[0m" >&2; exit 1; }

# --- Téléchargement vérifié (taille mini = filet anti-404/HTML/0-octet) ------
_content_length() {  # taille réelle annoncée par le serveur (suit les redirections HF)
  curl -sIL --connect-timeout 20 "$1" | tr -d '\r' \
    | grep -i '^content-length:' | tail -1 | tr -dc '0-9'
}

dl() {  # dl <url> <dest>  (3e arg ignoré, gardé pour compat appels existants)
  local url="$1" dest="$2"
  local want; want=$(_content_length "$url")
  # Déjà présent et COMPLET (taille == Content-Length) → skip.
  if [ -f "$dest" ] && [ -n "$want" ] && [ "$(stat -c%s "$dest" 2>/dev/null || echo 0)" = "$want" ]; then
    echo "  [skip] $(basename "$dest") ($(( want/1024/1024 )) MB complet)"; return 0
  fi
  mkdir -p "$(dirname "$dest")"
  echo "  [dl  ] $(basename "$dest") ← $url"
  # curl SIMPLE (pas de -C - ni --speed-time : ces flags tronquaient le fichier
  # à 0 sur ralentissement — bug réel rencontré le 21 juin). Retry = re-download
  # propre, puis VÉRIFICATION par Content-Length (rejette toute troncature).
  local try sz
  for try in 1 2 3 4 5; do
    rm -f "$dest"
    if curl -fL --connect-timeout 30 -o "$dest" "$url"; then
      sz=$(stat -c%s "$dest" 2>/dev/null || echo 0)
      if [ -z "$want" ] || [ "$sz" = "$want" ]; then
        echo "  [ok  ] $(basename "$dest") ($(( sz/1024/1024 )) MB)"; return 0
      fi
      echo "  [retry $try] $(basename "$dest") tronqué ($sz != $want)"
    else
      echo "  [retry $try] $(basename "$dest") échec curl"
    fi
    sleep 5
  done
  die "Téléchargement impossible/incomplet : $(basename "$dest") ($url)"
}

# --- 0. Pré-requis ----------------------------------------------------------
log "GPU & disque"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || die "pas de GPU"
AVAIL_GB=$(df -BG --output=avail "$WORK" | tail -1 | tr -dc '0-9')
echo "  /workspace dispo : ${AVAIL_GB} GB"
[ "${AVAIL_GB:-0}" -ge 70 ] || echo "  ⚠️  < 70 GB libres : les modèles pèsent ~60 GB (Wan 14B fp16 ≈ 28 GB)"
command -v ffmpeg >/dev/null 2>&1 || { log "install ffmpeg"; apt-get update -qq && apt-get install -y -qq ffmpeg; }
command -v git >/dev/null 2>&1 || die "git absent"

# --- 1. Repo gouverné -------------------------------------------------------
log "Repo gouverné YAWatch-LUNA (branche $REPO_BRANCH)"
if [ -d "$REPO/.git" ]; then
  git -C "$REPO" fetch --depth 1 origin "$REPO_BRANCH"
  git -C "$REPO" checkout "$REPO_BRANCH"
  git -C "$REPO" reset --hard "origin/$REPO_BRANCH"
else
  git clone --depth 1 --branch "$REPO_BRANCH" "$REPO_URL" "$REPO"
fi
echo "  HEAD: $(git -C "$REPO" rev-parse --short HEAD)"

# --- 2. ComfyUI -------------------------------------------------------------
log "ComfyUI"
if [ ! -d "$COMFY/.git" ]; then
  git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git "$COMFY"
fi
"$PY" -m pip install --break-system-packages -q -r "$COMFY/requirements.txt"
# Deps observées manquantes au boot (cf. mémoire) :
"$PY" -m pip install --break-system-packages -q sqlalchemy alembic tqdm blake3 \
  opencv-python-headless numpy

# --- 3. Custom nodes (FramePack + VideoHelperSuite) -------------------------
# Wan NATIF n'a besoin d'AUCUN custom node (WanImageToVideo/UNETLoader = core).
log "Custom nodes"
CN="$COMFY/custom_nodes"
clone_node() {  # clone_node <url> <dir>
  local url="$1" dir="$CN/$2"
  if [ ! -d "$dir/.git" ]; then git clone --depth 1 "$url" "$dir"; else git -C "$dir" pull --ff-only || true; fi
  [ -f "$dir/requirements.txt" ] && "$PY" -m pip install --break-system-packages -q -r "$dir/requirements.txt" || true
}
clone_node https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git ComfyUI-VideoHelperSuite
clone_node https://github.com/kijai/ComfyUI-FramePackWrapper.git ComfyUI-FramePackWrapper

# --- 4. Modèles -------------------------------------------------------------
# Sources VALIDÉES (corrigent les 404 silencieux du runbook d'origine) :
#  - sigclip      = Comfy-Org/sigclip_vision_384
#  - clip_l/llava = Comfy-Org/HunyuanVideo_repackaged/.../text_encoders
#  - Wan natif    = Comfy-Org/Wan_2.1_ComfyUI_repackaged/.../diffusion_models
HF=https://huggingface.co

log "Modèles FramePack (HunyuanVideo)"
dl "$HF/Kijai/HunyuanVideo_comfy/resolve/main/FramePackI2V_HY_fp8_e4m3fn.safetensors" \
   "$MODELS/diffusion_models/FramePackI2V_HY_fp8_e4m3fn.safetensors" 8000
dl "$HF/Kijai/HunyuanVideo_comfy/resolve/main/hunyuan_video_vae_bf16.safetensors" \
   "$MODELS/vae/hunyuan_video_vae_bf16.safetensors" 200
dl "$HF/Comfy-Org/sigclip_vision_384/resolve/main/sigclip_vision_patch14_384.safetensors" \
   "$MODELS/clip_vision/sigclip_vision_patch14_384.safetensors" 500
dl "$HF/Comfy-Org/HunyuanVideo_repackaged/resolve/main/split_files/text_encoders/clip_l.safetensors" \
   "$MODELS/text_encoders/clip_l.safetensors" 200
dl "$HF/Comfy-Org/HunyuanVideo_repackaged/resolve/main/split_files/text_encoders/llava_llama3_fp16.safetensors" \
   "$MODELS/text_encoders/llava_llama3_fp16.safetensors" 8000

log "Modèles Wan2.1 I2V 14B — NATIF fp8_e4m3fn (PAS le GGUF qui échouait)"
WAN=Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files
dl "$HF/$WAN/diffusion_models/wan2.1_i2v_480p_14B_fp8_e4m3fn.safetensors" \
   "$MODELS/diffusion_models/wan2.1_i2v_480p_14B_fp8_e4m3fn.safetensors" 6000
dl "$HF/$WAN/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors" \
   "$MODELS/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors" 3000
dl "$HF/$WAN/clip_vision/clip_vision_h.safetensors" \
   "$MODELS/clip_vision/clip_vision_h.safetensors" 500
dl "$HF/$WAN/vae/wan_2.1_vae.safetensors" \
   "$MODELS/vae/wan_2.1_vae.safetensors" 100

# --- 5. Dossiers de travail -------------------------------------------------
mkdir -p "$WORK/inputs" "$WORK/outputs" "$COMFY/input" "$COMFY/output"

log "TERMINÉ ✅  Provisioning complet."
echo "  Repo    : $REPO"
echo "  ComfyUI : $COMFY"
echo "  Étape suivante :"
echo "    $PY $REPO/tools/runpod/runner.py --engine framepack"
echo "    $PY $REPO/tools/runpod/runner.py --engine wan21"
