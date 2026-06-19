# DIFFUSERS VIDEO MODELS REFERENCE — YAWatch-LUNA

## Métier correspondant
Ingénieur pipeline (génération locale) · Directeur IA Vidéo

## Sources expertes utilisées
- HuggingFace Diffusers documentation : https://huggingface.co/docs/diffusers
- Stable Video Diffusion : https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt
- CogVideoX : https://huggingface.co/THUDM/CogVideoX-5b-I2V
- AnimateDiff via Diffusers : https://huggingface.co/docs/diffusers/api/pipelines/animatediff
- Wan2.1 : https://huggingface.co/Wan-AI/Wan2.1-I2V-14B-480P
- "Diffusion Models" — lecture Stanford CS236

## Problème empêché
- Utiliser un modèle inadapté (génération image pour une tâche vidéo)
- OOM (Out of Memory) par mauvais choix de modèle vs VRAM disponible
- Générer des clips de mauvaise qualité par méconnaissance des paramètres
- Confusion entre modèles image-to-image et image-to-video

## Code repo qui doit respecter ce document
- Tout futur module `app/diffusers_client.py`
- Scripts de génération locale
- `requirements.txt` (versions compatibles)

## Règles bloquantes avant production vidéo
1. Vérifier la VRAM disponible avant de charger un modèle (`nvidia-smi`).
2. Utiliser `torch.float16` ou `torch.bfloat16` — jamais `float32` pour la vidéo (OOM garanti).
3. Fixer le `generator` (seed) pour toute génération de production.
4. Valider un clip test avant de lancer un batch complet.

---

## 1. Comparatif des modèles vidéo

| Modèle | Type | Frames | FPS sortie | VRAM min | Qualité | Usage |
|---|---|---|---|---|---|---|
| SVD XT (Stability AI) | img2vid | 25 | 7 | 8 GB | ★★★☆ | Plans statiques avec mouvement subtil |
| CogVideoX-5B I2V | img2vid | 49 | 8 | 6 GB (bf16) | ★★★★ | Plans narratifs, mouvements guidés par prompt |
| CogVideoX-2B I2V | img2vid | 49 | 8 | 4 GB | ★★★☆ | Compromis qualité/mémoire |
| AnimateDiff v3 | img2vid | 16-32 | 8 | 6 GB | ★★★☆ | Plans dynamiques, personnages en mouvement |
| Wan2.1 I2V 14B | img2vid | 81 | 16 | 16 GB | ★★★★★ | Meilleure qualité open source |
| Wan2.1 I2V 1.3B | img2vid | 81 | 16 | 8 GB | ★★★☆ | Version allégée |

**Recommandation pour YAWatch-LUNA :**
- GPU ≥ 16 GB VRAM : Wan2.1 I2V 14B (meilleure option open source)
- GPU 8-10 GB : CogVideoX-5B I2V (excellent rapport qualité/mémoire)
- GPU 6-8 GB : CogVideoX-2B I2V ou SVD XT avec `--lowvram`
- GPU < 6 GB ou CPU : Externaliser vers Kling (cloud) — ne pas forcer local

---

## 2. Stable Video Diffusion (SVD XT)

### Installation
```bash
pip install diffusers transformers accelerate torch torchvision
```

### Code de base
```python
import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video
from PIL import Image

pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.enable_model_cpu_offload()  # Si VRAM < 10 GB

# Charger l'image source
image = load_image("assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png")
image = image.resize((1024, 576))  # SVD fonctionne mieux en 16:9 — voir note ci-dessous

generator = torch.manual_seed(42)  # Toujours fixer le seed en production

frames = pipe(
    image,
    num_frames=25,          # Durée : 25 frames à 7fps = ~3.6s
    decode_chunk_size=8,    # Réduire si OOM
    generator=generator,
    motion_bucket_id=60,    # 0-255 : 0=statique, 127=standard, 255=très dynamique
    noise_aug_strength=0.02 # 0.0-0.1 : plus élevé = plus de variation
).frames[0]

export_to_video(frames, "output_luna_clip.mp4", fps=7)
```

### Note SVD et format vertical 9:16
SVD est entraîné sur des images 16:9 (1024×576 ou 1152×640).
Pour du contenu 9:16, deux options :
1. Générer en 576×1024 (rotation du ratio) — résultats variables
2. Utiliser CogVideoX à la place (entraîné sur des résolutions mixtes)

### Paramètres clés SVD
| Paramètre | Plage | Effet |
|---|---|---|
| `motion_bucket_id` | 0-255 | Intensité du mouvement. Luna : 40-80. Twist/tension : 100-150 |
| `noise_aug_strength` | 0.0-0.1 | Variation par rapport à l'image source. Recommandé : 0.02 |
| `num_frames` | 14-25 | SVD XT supporte jusqu'à 25 frames |
| `decode_chunk_size` | 1-8 | Réduire si OOM. 1 = plus lent mais moins de mémoire |
| `fps` à l'export | 7-25 | 7 fps = vitesse native SVD. 25 fps pour YouTube |

### Interpolation pour 25fps
SVD génère en 7fps. Pour l'exporter en 25fps, utiliser RIFE ou FFmpeg :
```bash
# Simple (FFmpeg — interpole les frames manquantes)
ffmpeg -i output_7fps.mp4 -vf "fps=25,minterpolate=fps=25:mi_mode=mci" output_25fps.mp4

# Qualité supérieure : RIFE (interpolation par IA)
# pip install rife-ncnn-vulkan
```

---

## 3. CogVideoX I2V (Recommandé pour YAWatch-LUNA)

### Pourquoi CogVideoX est préféré à SVD pour Luna Stories
- Supporte les résolutions verticales nativement
- Guidé par **prompt texte** : on peut décrire le mouvement précisément
- 49 frames à 8fps = ~6 secondes (durée idéale pour un plan teaser)
- CRF plus bas = meilleure cohérence de personnage

### Code CogVideoX-5B I2V
```python
import torch
from diffusers import CogVideoXImageToVideoPipeline
from diffusers.utils import export_to_video, load_image

pipe = CogVideoXImageToVideoPipeline.from_pretrained(
    "THUDM/CogVideoX-5b-I2V",
    torch_dtype=torch.bfloat16
)
pipe.enable_sequential_cpu_offload()   # Si VRAM < 10 GB
pipe.vae.enable_tiling()               # Réduit la mémoire
pipe.vae.enable_slicing()              # Réduit la mémoire

image = load_image("assets/.../luna_adulte_neutral_9x16_01.png")

generator = torch.Generator().manual_seed(42)

video = pipe(
    prompt=(
        "Cinematic vertical portrait. Luna, 32-year-old woman, brown hair, "
        "dark professional attire, sits at her office desk. "
        "Very slow push-in camera movement, imperceptible breathing, "
        "moody blue rim lighting, Paris night visible through window. "
        "Ultra realistic, 4K, film grain."
    ),
    negative_prompt=(
        "cartoon, anime, drawing, illustration, blur, shaky, "
        "fast movement, bright colors, smiling"
    ),
    image=image,
    num_videos_per_prompt=1,
    num_inference_steps=50,    # 50 = qualité production, 25 = test rapide
    num_frames=49,
    guidance_scale=6.0,        # 5.0-8.0 : plus élevé = plus fidèle au prompt
    generator=generator,
    use_dynamic_cfg=True,      # Améliore la cohérence
).frames[0]

export_to_video(video, "luna_plan_02_clip.mp4", fps=8)
```

### Prompts de mouvement pour YAWatch-LUNA
```python
MOUVEMENTS_YAWATCH = {
    "push_in_slow": (
        "Extremely slow imperceptible push-in camera movement, "
        "1mm per second forward drift, barely perceptible depth increase"
    ),
    "pull_back_reveal": (
        "Very slow pull-back camera movement, "
        "subject remains centered, subtle reveal of environment"
    ),
    "pan_left_slow": (
        "Slow camera pan from right to left, "
        "smooth continuous movement, no shake"
    ),
    "static_breathing": (
        "Completely static camera, ultra slow breathing motion in subject, "
        "subtle hair movement from air conditioning, pulsing shadows"
    ),
    "rack_focus": (
        "Static camera with slow rack focus from background to subject, "
        "gradual depth of field shift"
    )
}
```

---

## 4. AnimateDiff via Diffusers

```python
import torch
from diffusers import AnimateDiffPipeline, MotionAdapter, DDIMScheduler
from diffusers.utils import export_to_gif, export_to_video

adapter = MotionAdapter.from_pretrained(
    "guoyww/animatediff-motion-adapter-v1-5-3",
    torch_dtype=torch.float16
)
pipe = AnimateDiffPipeline.from_pretrained(
    "SG161222/Realistic_Vision_V6.0_B1_noVAE",
    motion_adapter=adapter,
    torch_dtype=torch.float16
)
pipe.scheduler = DDIMScheduler.from_pretrained(
    "SG161222/Realistic_Vision_V6.0_B1_noVAE",
    subfolder="scheduler",
    clip_sample=False,
    timestep_spacing="linspace",
    beta_schedule="linear",
    steps_offset=1
)
pipe.enable_vae_slicing()
pipe.enable_model_cpu_offload()

output = pipe(
    prompt="cinematic portrait luna woman brown hair dark office",
    negative_prompt="bad quality, blur, anime, cartoon",
    num_frames=16,
    guidance_scale=7.5,
    num_inference_steps=25,
    generator=torch.Generator().manual_seed(42),
    width=768,
    height=1366
)

export_to_video(output.frames[0], "animatediff_luna.mp4", fps=8)
```

---

## 5. Wan2.1 (meilleure option open source si GPU ≥ 16 GB)

```python
import torch
from diffusers import WanImageToVideoPipeline
from diffusers.utils import export_to_video, load_image

pipe = WanImageToVideoPipeline.from_pretrained(
    "Wan-AI/Wan2.1-I2V-14B-480P",
    torch_dtype=torch.bfloat16
)
pipe.enable_model_cpu_offload()
pipe.vae.enable_tiling()

image = load_image("assets/.../luna_adulte_neutral_9x16_01.png")
image = image.resize((480, 832))  # 9:16 à 480p

video = pipe(
    image=image,
    prompt=(
        "Cinematic vertical portrait, Luna, slow push-in, "
        "moody blue lighting, Paris at night, film grain"
    ),
    negative_prompt="cartoon, blur, fast movement, anime",
    height=832,
    width=480,
    num_frames=81,        # ~5s à 16fps
    guidance_scale=5.0,
    num_inference_steps=50,
    generator=torch.Generator().manual_seed(42)
).frames[0]

export_to_video(video, "wan_luna_clip.mp4", fps=16)
```

---

## 6. Gestion mémoire — règles pratiques

```python
# Libérer la mémoire GPU entre deux générations
import gc
import torch

def clear_gpu_memory():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

# Vérifier la VRAM disponible avant de charger
def check_vram_gb() -> float:
    if not torch.cuda.is_available():
        return 0.0
    props = torch.cuda.get_device_properties(0)
    return props.total_memory / (1024 ** 3)

# Choisir le modèle selon la VRAM
def select_model_for_vram(vram_gb: float) -> str:
    if vram_gb >= 16:
        return "Wan-AI/Wan2.1-I2V-14B-480P"
    elif vram_gb >= 8:
        return "THUDM/CogVideoX-5b-I2V"
    elif vram_gb >= 6:
        return "THUDM/CogVideoX-2b-I2V"
    else:
        return "USE_KLING_CLOUD"  # Pas assez de VRAM pour le local
```

---

## 7. Checklist avant génération batch

```
□ nvidia-smi confirme VRAM suffisante
□ seed fixé (generator avec seed constant)
□ prompt écrit selon les templates MOUVEMENTS_YAWATCH
□ image source vérifiée (9:16, resolution ≥ 941×1672)
□ dossier output créé et versioné (clips/teaser/PLAN_01/)
□ test sur 1 clip avant le batch complet
□ 1 clip de test visionné avant validation du batch
```
