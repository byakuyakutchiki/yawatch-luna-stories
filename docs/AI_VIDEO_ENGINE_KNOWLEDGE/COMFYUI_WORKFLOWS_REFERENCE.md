# COMFYUI WORKFLOWS REFERENCE — YAWatch-LUNA

## Métier correspondant
Directeur IA Vidéo (local) · Ingénieur pipeline (génération locale)

## Sources expertes utilisées
- ComfyUI GitHub officiel : https://github.com/comfyanonymous/ComfyUI
- ComfyUI documentation : https://docs.comfy.org
- ComfyUI API documentation : https://docs.comfy.org/essentials/comfyui-server/api
- AnimateDiff-Evolved : https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved
- ComfyUI-VideoHelperSuite : https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite
- IPAdapter : https://github.com/cubiq/ComfyUI_IPAdapter_plus
- InstantID / ControlNet nodes

## Problème empêché
- Génération de clips locaux non reproductibles (résultats non identiques entre sessions)
- Confusion entre génération d'image et génération de vidéo dans ComfyUI
- Perte de cohérence personnage entre clips (visages différents d'un clip à l'autre)
- Workflows non sauvegardés ou non versionés

## Code repo qui doit respecter ce document
- Tout futur module `app/comfyui_client.py`
- Scripts d'automatisation de génération locale
- `app/visual_consistency_manager.py` (intégration seeds fixes)

## Règles bloquantes avant production vidéo
1. Tout workflow ComfyUI utilisé en production doit être sauvegardé en JSON versioné dans `workflows/`.
2. Le seed de chaque génération doit être loggé — un clip non reproductible n'est pas un actif.
3. Les clips générés localement via ComfyUI passent le même Quality Gate que les clips Kling.
4. ComfyUI nécessite un GPU NVIDIA avec ≥ 6 GB VRAM pour AnimateDiff, ≥ 10 GB pour SVD/CogVideoX.

---

## 1. Architecture ComfyUI

```
Interface web : http://127.0.0.1:8188
API REST      : http://127.0.0.1:8188/prompt (POST)
Queue         : http://127.0.0.1:8188/queue (GET)
History       : http://127.0.0.1:8188/history (GET)
Outputs       : ComfyUI/output/ (par défaut)
Workflows     : JSON bidirectionnel (import/export)
```

### Lancement
```bash
cd ComfyUI
python main.py --listen 0.0.0.0 --port 8188
# Avec GPU limité (< 6GB VRAM) :
python main.py --lowvram --listen 0.0.0.0 --port 8188
# CPU uniquement (lent) :
python main.py --cpu
```

---

## 2. Structure d'un workflow JSON ComfyUI

Un workflow ComfyUI est un graphe de nœuds :

```json
{
  "1": {
    "class_type": "CheckpointLoaderSimple",
    "inputs": {
      "ckpt_name": "v1-5-pruned-emaonly.safetensors"
    }
  },
  "2": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "cinematic portrait of Luna, dark office, rim light",
      "clip": ["1", 1]
    }
  },
  "3": {
    "class_type": "KSampler",
    "inputs": {
      "model": ["1", 0],
      "positive": ["2", 0],
      "negative": ["4", 0],
      "latent_image": ["5", 0],
      "seed": 42,
      "steps": 20,
      "cfg": 7.0,
      "sampler_name": "dpmpp_2m",
      "scheduler": "karras",
      "denoise": 1.0
    }
  }
}
```

### Règle de reproductibilité
```python
# Dans tout workflow de production YAWatch-LUNA :
"seed": 42           # TOUJOURS fixer le seed en production
"control_after_generate": "fixed"  # Jamais "randomize" en production
```

---

## 3. Nodes essentiels par usage

### Génération d'image (base)
| Node | Rôle |
|---|---|
| `CheckpointLoaderSimple` | Charger le modèle SD (SDXL, SD1.5) |
| `CLIPTextEncode` | Encoder le prompt positif/négatif |
| `EmptyLatentImage` | Définir la résolution cible |
| `KSampler` | Inférence principale |
| `VAEDecode` | Décoder le latent en image |
| `SaveImage` | Sauvegarder avec metadata |

### Cohérence personnage (IPAdapter)
| Node | Rôle |
|---|---|
| `IPAdapterModelLoader` | Charger le modèle IPAdapter |
| `IPAdapter` | Injecter une image de référence pour guider le style/visage |
| `IPAdapterFaceID` | Version spécialisée pour la cohérence du visage |

**Usage YAWatch-LUNA :**
Utiliser `IPAdapter` avec `luna_adulte_neutral_9x16_01.png` comme image de référence
pour maintenir la cohérence du visage de Luna entre les plans.

```json
"ip_adapter_node": {
  "class_type": "IPAdapter",
  "inputs": {
    "model": ["checkpoint", 0],
    "ipadapter": ["ipadapter_loader", 0],
    "image": ["load_reference_image", 0],
    "weight": 0.6,
    "weight_type": "style transfer precise",
    "start_at": 0.0,
    "end_at": 1.0
  }
}
```

### Génération vidéo (AnimateDiff)
| Node | Rôle |
|---|---|
| `ADE_LoadAnimateDiffModel` | Charger le motion module |
| `ADE_AnimateDiffSamplingSettings` | Régler fps, nb frames |
| `VHS_VideoCombine` | Assembler les frames en MP4 |
| `LoadImage` | Charger l'image source |
| `VAEEncodeForInpaint` | Pour image-to-video avec img2img |

### Génération vidéo (SVD — Stable Video Diffusion)
| Node | Rôle |
|---|---|
| `ImageOnlyCheckpointLoader` | Charger SVD XT (svd_xt.safetensors) |
| `VideoLinearCFGGuidance` | Contrôle du CFG pour SVD |
| `SVD_img2vid_Conditioning` | Encoder l'image source |
| `KSampler` | Générer les frames |
| `VHS_VideoCombine` | Assembler en MP4 |

---

## 4. Workflow AnimateDiff pour YAWatch-LUNA

### Paramètres recommandés
```json
{
  "motion_module": "mm_sd_v15_v3.ckpt",
  "num_frames": 16,
  "fps": 8,
  "context_length": 16,
  "context_stride": 1,
  "context_overlap": 4,
  "closed_loop": false,
  "motion_scale": 1.0
}
```

### Réglages par type de mouvement
| Mouvement souhaité | motion_scale | fps | notes |
|---|---|---|---|
| Très lent (respiration) | 0.5-0.7 | 8 | Atmosphérique, pluie légère |
| Lent (caméra pan) | 0.8-1.0 | 8 | Standard Luna Stories |
| Modéré (tension) | 1.0-1.3 | 12 | Plans de confrontation |
| Fort (impact) | 1.5+ | 16 | Révélations, twist |

### Résolution et mémoire requise
| Résolution | VRAM requise | Notes |
|---|---|---|
| 512 × 912 (9:16 bas) | ~4 GB | Minimum utilisable |
| 768 × 1366 (9:16 moyen) | ~6 GB | Qualité acceptable |
| 1024 × 1820 (9:16 haut) | ~10 GB | Recommandé production |
| 1080 × 1920 (9:16 natif) | ~12 GB+ | Idéal, GPU haut de gamme |

---

## 5. API ComfyUI — Automatisation Python

```python
import json
import urllib.request
import urllib.parse
import uuid
import time

COMFYUI_URL = "http://127.0.0.1:8188"

def queue_workflow(workflow_json: dict, client_id: str = None) -> str:
    """Envoyer un workflow à ComfyUI et retourner le prompt_id."""
    if client_id is None:
        client_id = str(uuid.uuid4())
    payload = json.dumps({
        "prompt": workflow_json,
        "client_id": client_id
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    response = json.loads(urllib.request.urlopen(req).read())
    return response["prompt_id"]

def wait_for_completion(prompt_id: str, timeout: int = 300) -> dict:
    """Attendre la fin d'un prompt et retourner les outputs."""
    elapsed = 0
    while elapsed < timeout:
        history_url = f"{COMFYUI_URL}/history/{prompt_id}"
        history = json.loads(urllib.request.urlopen(history_url).read())
        if prompt_id in history:
            return history[prompt_id]["outputs"]
        time.sleep(2)
        elapsed += 2
    raise TimeoutError(f"ComfyUI timeout après {timeout}s pour prompt {prompt_id}")

def download_output(filename: str, output_dir: str = "/tmp/comfyui_outputs") -> str:
    """Télécharger un fichier produit par ComfyUI."""
    url = f"{COMFYUI_URL}/view?filename={urllib.parse.quote(filename)}"
    local_path = f"{output_dir}/{filename}"
    urllib.request.urlretrieve(url, local_path)
    return local_path
```

---

## 6. Gestion des workflows en production

### Nomenclature des fichiers workflow
```
workflows/
├── image_gen/
│   ├── luna_adulte_portrait_v1.json
│   ├── luna_doll_gros_plan_v1.json
│   └── aby_observing_v1.json
├── video_gen/
│   ├── animatediff_pan_slow_v1.json
│   ├── svd_push_in_v1.json
│   └── cogvideox_cinematic_v1.json
└── README_WORKFLOWS.md
```

### Metadata obligatoire dans chaque workflow JSON
```json
{
  "_metadata": {
    "workflow_name": "luna_adulte_portrait_v1",
    "created": "2026-06-19",
    "model": "SDXL 1.0",
    "seed": 42,
    "intended_use": "Portrait Luna adulte neutre pour TEASER_PLAN_02",
    "validated": false,
    "validated_by": null,
    "validated_date": null
  }
}
```

### Règle de versioning
- `_v1.json` → première version testée
- `_v2.json` → après ajustement des paramètres (garder _v1)
- Jamais supprimer une version validée

---

## 7. Custom nodes requis pour YAWatch-LUNA

| Node package | Usage | Lien |
|---|---|---|
| ComfyUI-VideoHelperSuite | Assembler/sauvegarder des clips vidéo | github.com/Kosinkadink |
| ComfyUI-AnimateDiff-Evolved | Génération vidéo via AnimateDiff | github.com/Kosinkadink |
| ComfyUI_IPAdapter_plus | Cohérence personnage | github.com/cubiq |
| ComfyUI-ControlNet-Aux | Détection contours/profondeur | github.com/Fannovel16 |
| was-node-suite-comfyui | Utilitaires image/batch | github.com/WASasquatch |

### Installation
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite
git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved
git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus
pip install -r ComfyUI-VideoHelperSuite/requirements.txt
pip install -r ComfyUI-AnimateDiff-Evolved/requirements.txt
```

---

## 8. Limites à connaître

| Limite | Détail |
|---|---|
| Cohérence personnage | AnimateDiff ne garantit pas que Luna ressemble à Luna entre deux clips — utiliser IPAdapter |
| Mouvement précis | ComfyUI ne permet pas de dire "pan gauche" précisément — c'est un paramètre guidant, pas une instruction directe |
| VRAM requise | SVD XT nécessite 8-10 GB VRAM — impossible sur GPU < 8GB sans compromis |
| Durée clips | AnimateDiff produit 16-32 frames → ~2-4s à 8fps. SVD produit 25 frames → ~3.5s à 7fps |
| Résolution native | Pour 1080×1920, descendre à 768×1366 + upscale en post-traitement |
