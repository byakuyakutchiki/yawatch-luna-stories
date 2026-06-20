# STATION LÉGÈRE YAWATCH-LUNA — PLAN D'INSTALLATION

> **Document de référence pour la configuration de la machine Windows de production.**
> Ce document ne touche pas au pipeline validé (88 tests, statuts, quality gate).
> Toute génération I2V produite sur cette station reste un `prototype_technique`
> jusqu'à ce que les 3 plans tests passent le quality gate.

**Date :** 2026-06-20  
**Machine cible :** Windows (station de production légère)  
**VM Linux :** porte le repo Git, le pipeline Python, les tests, les statuts  
**Référence :** `YAWATCH_LUNA_FACTORY_MASTER_PLAN.md` — Partie 5.2

---

## Architecture globale de la station

```
┌─────────────────────────────────────────────────────────────────────┐
│  MACHINE WINDOWS (station de génération)                            │
│                                                                     │
│  ComfyUI (port 8188)                                                │
│    └── AnimateDiff SD1.5 + IPAdapter                                │
│                                                                     │
│  CogVideoX-2B (environnement Python isolé — test uniquement)        │
│                                                                     │
│  Dossier partagé : C:\yawatch-luna-outputs\clips\                  │
│    └── clips MP4 générés → accessibles depuis la VM Linux           │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  VM LINUX (pipeline)                                                │
│                                                                     │
│  app/i2v_engine/ (module expérimental — ne touche pas au pipeline)  │
│    └── appelle http://[IP Windows]:8188 via API ComfyUI             │
│                                                                     │
│  FFmpeg + Quality Gate + Export Manager + Tests → inchangés         │
└─────────────────────────────────────────────────────────────────────┘
```

**Flux production sur cette station :**

```
Image canonique (Linux VM / assets/)
    ↓ copie vers Windows
ComfyUI + AnimateDiff (Windows)
    ↓ clip MP4 généré
Dossier partagé
    ↓ accessible Linux VM
Quality Gate (Linux VM) → verdict technique + contenu
    ↓ si PASS sur les 5 verdicts automatiques
advance_to_candidat()
    ↓ visionnage Ludovic
mark_human_approved("Ludovic")
    → TEASER_VALIDE
```

---

## ÉTAPE 1 — Nettoyage disque cible

Avant toute installation, libérer de l'espace sur la partition Windows cible.

### Espace disque minimum requis

| Composant | Espace estimé |
|---|---|
| ComfyUI (base) | ~2 GB |
| SD1.5 checkpoint (1 modèle) | ~2-4 GB |
| AnimateDiff motion module | ~1.7 GB |
| IPAdapter models | ~3-5 GB |
| CogVideoX-2B (test séparé) | ~6-8 GB |
| Clips générés (production) | ~500 MB / épisode |
| **Total minimum recommandé** | **~20 GB libres** |

### Nettoyage recommandé

```
Vérifier dans l'explorateur Windows :
  C:\Users\[user]\AppData\Local\Temp        → vider
  C:\Users\[user]\Downloads                 → vider les anciens fichiers
  Corbeille                                 → vider

Outil : Nettoyage de disque Windows (cleanmgr.exe)
  → cocher : Fichiers temporaires, Vignettes, Fichiers Internet temporaires
```

### Vérifier la VRAM disponible

```powershell
# Dans PowerShell ou CMD :
nvidia-smi
# ou
dxdiag  # → onglet Affichage → Mémoire d'affichage dédiée

# Si nvidia-smi non disponible :
# Gestionnaire des tâches → Performances → GPU
# Lire : "Mémoire GPU dédiée"
```

**Enregistrer la VRAM disponible — cette valeur conditionne les modèles utilisables.**

| VRAM constatée | Modèles accessibles |
|---|---|
| 4 GB | AnimateDiff SD1.5 seul · CogVideoX-2B serré |
| 6 GB | AnimateDiff SD1.5 correct · CogVideoX-2B confortable |
| 8 GB | AnimateDiff SD1.5 optimal · CogVideoX-2B + SVD XT |
| 10+ GB | Tous les modèles de la station légère |

---

## ÉTAPE 2 — Installation ComfyUI (Windows)

ComfyUI est un framework de génération IA en nœuds (node-based) qui expose une API REST
sur `localhost:8188`. Le pipeline Linux l'appellera via cette API.

### 2.1 Choix de la méthode d'installation

**Option A — Portable (recommandé pour démarrer rapidement)**

```
1. Aller sur : https://github.com/comfyanonymous/ComfyUI/releases
2. Télécharger : ComfyUI_windows_portable_nvidia.zip (dernière version stable)
3. Extraire dans : C:\ComfyUI\
4. Structure attendue :
   C:\ComfyUI\
   ├── run_nvidia_gpu.bat   ← lancer ComfyUI
   ├── ComfyUI\
   │   ├── models\
   │   ├── custom_nodes\
   │   └── output\
   └── python_embeded\
```

**Option B — Git + Python (recommandé pour contrôle complet)**

```powershell
# Prérequis : Python 3.11, Git, CUDA 12.1
python --version   # vérifier 3.11.x
git --version

git clone https://github.com/comfyanonymous/ComfyUI.git C:\ComfyUI
cd C:\ComfyUI
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

### 2.2 Premier démarrage et vérification

```batch
# Double-clic sur run_nvidia_gpu.bat (option portable)
# ou :
cd C:\ComfyUI && python main.py --listen 0.0.0.0 --port 8188
```

```
Vérifier dans le navigateur : http://localhost:8188
→ Interface ComfyUI doit s'ouvrir
→ En bas à droite : "VRAM libre" affiché
```

**`--listen 0.0.0.0`** est obligatoire pour que la VM Linux puisse appeler l'API Windows.

### 2.3 Installation du Manager (gestionnaire d'extensions)

Le Manager permet d'installer les extensions AnimateDiff sans manipulation manuelle.

```powershell
cd C:\ComfyUI\custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
# Redémarrer ComfyUI
# → Menu "Manager" apparaît dans l'interface
```

### 2.4 Test de l'API REST

Depuis la VM Linux (ou PowerShell Windows) :

```bash
# Depuis VM Linux :
curl http://[IP-WINDOWS]:8188/system_stats
# Réponse attendue : JSON avec vram_total, vram_free, ...

# Trouver l'IP Windows depuis la VM Linux :
ip route show default   # → la passerelle est l'IP Windows
# ou
cat /etc/resolv.conf    # nameserver = IP Windows VirtualBox
```

---

## ÉTAPE 3 — Installation AnimateDiff SD1.5

AnimateDiff génère des clips vidéo à partir d'images fixes en animant des frames
via le module de mouvement SD1.5. C'est le premier axe local réaliste pour la station.

### 3.1 Extension ComfyUI-AnimateDiff-Evolved

```powershell
cd C:\ComfyUI\custom_nodes
git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git
```

Extensions complémentaires nécessaires (via Manager ou git) :

```powershell
# IPAdapter (cohérence personnage — critique pour Luna/Aby)
git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git

# ControlNet (guide de mouvement optionnel)
git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git
```

Redémarrer ComfyUI après chaque groupe d'extensions.

### 3.2 Téléchargement des modèles

#### Checkpoint SD1.5 — 1 seul, choisi pour le réalisme

**Recommandé pour YAWatch-LUNA :** Realistic Vision V6 (portraits photoréalistes, stable pour visages)

```
Télécharger depuis : https://civitai.com/models/4201
Fichier : realisticVisionV60B1_v51HyperVAE.safetensors (~2 GB)
Placer dans : C:\ComfyUI\models\checkpoints\
```

Alternative si Realistic Vision est trop "hyperréaliste" pour l'esthétique YAWatch :

```
DreamShaper 8 (cinématique + réalisme équilibré)
Fichier : dreamshaper_8.safetensors (~2 GB)
Placer dans : C:\ComfyUI\models\checkpoints\
```

**Règle : ne télécharger qu'un seul checkpoint au départ.** Le choix final se fait
après le test des 3 plans de validation (Étape 7).

#### Module de mouvement AnimateDiff

```
Fichier : mm_sd_v15_v3.safetensors (1.7 GB)
Source   : https://huggingface.co/guoyww/animatediff/tree/main
Placer dans : C:\ComfyUI\custom_nodes\ComfyUI-AnimateDiff-Evolved\models\
```

#### IPAdapter — cohérence de personnage (priorité haute pour Luna)

```
Fichier 1 : ip-adapter_sd15.safetensors (~1.7 GB)
Source    : https://huggingface.co/h94/IP-Adapter/tree/main/models
Placer dans : C:\ComfyUI\models\ipadapter\

Fichier 2 : CLIP Vision encoder (requis par IPAdapter)
            clip_vision_g.safetensors (~1.7 GB)
Source    : https://huggingface.co/h94/IP-Adapter/tree/main/models
Placer dans : C:\ComfyUI\models\clip_vision\
```

**Rôle de l'IPAdapter :** injecter l'image de référence du personnage (Luna adulte, Aby, etc.)
comme condition visuelle. Le modèle génère du mouvement en respectant l'identité visuelle
de la personne, pas seulement sa pose.

### 3.3 Structure des dossiers après installation complète

```
C:\ComfyUI\
├── models\
│   ├── checkpoints\
│   │   └── realisticVisionV60B1_v51HyperVAE.safetensors
│   ├── ipadapter\
│   │   └── ip-adapter_sd15.safetensors
│   └── clip_vision\
│       └── clip_vision_g.safetensors
├── custom_nodes\
│   ├── ComfyUI-Manager\
│   ├── ComfyUI-AnimateDiff-Evolved\
│   │   └── models\
│   │       └── mm_sd_v15_v3.safetensors
│   ├── ComfyUI_IPAdapter_plus\
│   └── comfyui_controlnet_aux\
└── output\
    └── AnimateDiff\   ← clips générés ici
```

### 3.4 Workflow de test minimal AnimateDiff

Avant de connecter au pipeline, valider que ComfyUI + AnimateDiff fonctionnent
en chargeant le workflow de référence disponible dans la documentation AnimateDiff-Evolved.

**Critères de validation à ce stade (hors quality gate) :**
- ComfyUI génère un clip MP4 sans erreur
- Le clip contient du mouvement (pas une image statique)
- Pas d'OOM (Out of Memory) pendant la génération

---

## ÉTAPE 4 — Test CogVideoX-2B (environnement isolé)

CogVideoX-2B est testé dans un environnement Python séparé pour éviter les conflits
de dépendances avec ComfyUI. Ce test est **parallèle** à ComfyUI, pas en remplacement.

### 4.1 Créer l'environnement isolé

```powershell
# Dans PowerShell Windows :
python -m venv C:\yawatch-cogvideox-env
C:\yawatch-cogvideox-env\Scripts\activate

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install diffusers transformers accelerate sentencepiece imageio[ffmpeg]
```

### 4.2 Script de test CogVideoX-2B

```python
# C:\yawatch-luna-test\test_cogvideox_2b.py
# ATTENTION : script de test uniquement — ne pas intégrer dans le pipeline
import torch
from diffusers import CogVideoXImageToVideoPipeline
from diffusers.utils import load_image, export_to_video
from pathlib import Path

MODEL_ID = "THUDM/CogVideoX-2b"
IMAGE_PATH = r"C:\yawatch-luna-assets\luna_adulte_neutral_9x16_01.png"
OUTPUT_PATH = r"C:\yawatch-luna-outputs\clips\test_cogvideox_plan2.mp4"
PROMPT = (
    "Cinematic 5-second shot. Slow imperceptible push-in toward Luna's face. "
    "Emotional thriller mood, Parisian office, soft window light. "
    "Stable face, no distortion, no smile."
)

pipe = CogVideoXImageToVideoPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16,
)
pipe.enable_model_cpu_offload()   # si VRAM serrée (4-6 GB)
pipe.vae.enable_slicing()

image = load_image(IMAGE_PATH).resize((768, 1360))  # ratio 9:16 approximatif

video = pipe(
    prompt=PROMPT,
    image=image,
    num_videos_per_prompt=1,
    num_inference_steps=50,
    num_frames=49,     # ~6s à 8fps
    guidance_scale=6,
    generator=torch.Generator(device="cuda").manual_seed(42),
).frames[0]

export_to_video(video, OUTPUT_PATH, fps=8)
print(f"Clip généré : {OUTPUT_PATH}")
```

### 4.3 Critères de validation CogVideoX-2B

Après génération, inspecter visuellement le clip `test_cogvideox_plan2.mp4` :

| Critère | Seuil acceptable |
|---|---|
| Stabilité du visage de Luna | Pas de déformation notable |
| Respect de l'image source | Tenue, carnation, contexte conservés |
| Mouvement de caméra | Push-in visible mais discret |
| Artefacts | Moins de 2 artefacts notables sur 6 secondes |
| Durée générée | ≥ 4 secondes effectives |

**Si CogVideoX-2B passe ces critères visuels :** le soumettre ensuite au quality gate
de la VM Linux (Étape 7) comme tout autre clip de production.

**Si CogVideoX-2B échoue :** ne pas persister. AnimateDiff SD1.5 reste l'axe principal.

---

## ÉTAPE 5 — Création du I2V_ENGINE local expérimental

Ce module s'installe dans le repo Linux (VM) et communique avec ComfyUI via son API REST.
**Il ne modifie aucun composant existant validé.** Il est marqué EXPÉRIMENTAL.

### 5.1 Structure du module

```
app/
├── i2v_engine/                    ← nouveau module (ne touche à rien d'existant)
│   ├── __init__.py
│   ├── base.py                    ← interface abstraite
│   ├── comfyui_adapter.py         ← appelle ComfyUI Windows
│   ├── cogvideox_adapter.py       ← appelle CogVideoX-2B local (optionnel)
│   └── workflows/
│       └── animatediff_sd15_yawatch.json   ← workflow ComfyUI pour YAWatch
├── [tous les autres modules existants — inchangés]
```

### 5.2 Interface abstraite (base.py)

```python
# app/i2v_engine/base.py
from abc import ABC, abstractmethod
from pathlib import Path

class I2VEngine(ABC):
    """Interface abstraite pour les moteurs image-to-video.
    
    Toute implémentation concrète doit respecter ce contrat.
    Le pipeline ne connaît que cette interface — pas les détails de l'outil.
    """

    @abstractmethod
    def generate(
        self,
        image_path: Path,
        prompt: str,
        duration_seconds: float = 5.0,
        seed: int = 42,
    ) -> Path:
        """Génère un clip MP4 à partir d'une image fixe.
        
        Retourne le chemin du clip généré.
        Lève RuntimeError si la génération échoue.
        Le clip retourné est toujours un prototype_technique.
        """
        raise NotImplementedError

    @abstractmethod
    def health_check(self) -> bool:
        """Vérifie que le moteur est disponible et opérationnel."""
        raise NotImplementedError
```

### 5.3 Adaptateur ComfyUI (comfyui_adapter.py — squelette)

```python
# app/i2v_engine/comfyui_adapter.py
# STATUT : EXPÉRIMENTAL — ne pas utiliser en production sans validation quality gate
import json
import time
import uuid
import requests
from pathlib import Path
from .base import I2VEngine

COMFYUI_HOST = "http://192.168.1.XXX:8188"   # IP Windows à configurer
WORKFLOW_PATH = Path(__file__).parent / "workflows" / "animatediff_sd15_yawatch.json"


class ComfyUIAdapter(I2VEngine):
    """Adaptateur vers ComfyUI (AnimateDiff SD1.5) sur la station Windows.
    
    EXPÉRIMENTAL : validé uniquement après passage du quality gate sur 3 plans tests.
    """

    def __init__(self, host: str = COMFYUI_HOST):
        self.host = host
        self.workflow_template = json.loads(WORKFLOW_PATH.read_text())

    def health_check(self) -> bool:
        try:
            r = requests.get(f"{self.host}/system_stats", timeout=5)
            return r.status_code == 200
        except requests.ConnectionError:
            return False

    def generate(
        self,
        image_path: Path,
        prompt: str,
        duration_seconds: float = 5.0,
        seed: int = 42,
    ) -> Path:
        raise NotImplementedError(
            "ComfyUIAdapter.generate() — implémentation à compléter "
            "après validation du workflow AnimateDiff SD1.5 sur les 3 plans tests."
        )
```

**Note :** l'implémentation complète de `generate()` sera codée APRÈS que le workflow
ComfyUI manual soit validé sur les 3 plans tests. On ne code pas l'automatisation
avant d'avoir validé le résultat à la main.

### 5.4 Règle de non-régression

```python
# app/i2v_engine/__init__.py
"""Module I2V_ENGINE — EXPÉRIMENTAL.

Ce module ne modifie aucun composant existant du pipeline.
Il est importé uniquement par les scripts de test expérimentaux,
jamais par app/main.py, app/batch_processor.py ou app/export_manager.py
tant que le quality gate n'a pas validé les 3 plans tests.

Statut officiel de tout clip généré par ce module : PROTOTYPE_TECHNIQUE.
"""
```

---

## ÉTAPE 6 — Dossier partagé Windows ↔ Linux VM

Le dossier partagé permet de transférer les clips générés sur Windows vers
la VM Linux pour les soumettre au quality gate.

### 6.1 Configuration VirtualBox (dossier partagé)

```
VirtualBox → Machine → Paramètres → Dossiers partagés
→ Ajouter un dossier :
  Chemin hôte (Windows) : C:\yawatch-luna-outputs
  Nom du partage        : yawatch_outputs
  Accès automatique     : oui
  Point de montage      : /mnt/yawatch-outputs

# Dans la VM Linux :
sudo mount -t vboxsf yawatch_outputs /mnt/yawatch-outputs
# ou ajouter dans /etc/fstab :
yawatch_outputs /mnt/yawatch-outputs vboxsf defaults,uid=1000,gid=1000 0 0
```

### 6.2 Structure du dossier partagé

```
C:\yawatch-luna-outputs\          ← dossier Windows
├── clips\                        ← clips I2V générés (MP4)
│   ├── plan_01_tour_yawatch.mp4
│   ├── plan_02_luna_portrait.mp4
│   └── ...
├── test_results\                 ← résultats des tests (notes manuelles)
└── quality_gate_reports\         ← rapports JSON du quality gate (VM Linux)
```

---

## ÉTAPE 7 — Protocole de validation sur les 3 plans tests

**Aucun clip ne devient TEASER_CANDIDAT avant ce protocole.**

### 7.1 Les 3 plans choisis (discriminants)

| Plan | Image source | Mouvement cible | Difficulté principale |
|---|---|---|---|
| **Plan 2** | `luna_adulte_neutral_9x16_01.png` | Push-in imperceptible | Stabilité visage adulte en portrait serré |
| **Plan 6** | `luna_enfant_comforted_with_doll_01.png` | Push-in doux vers la poupée | Visage enfant + texture tissu poupée |
| **Plan 9** | `aby_enfant_main_jeton_noir_maquette_01.png` | Focus pull, main + objet | Mains (cas difficile pour tous les modèles I2V) |

### 7.2 Prompt de mouvement pour chaque plan test

**Plan 2 — Luna adulte portrait**
```
Cinematic 5-second shot. Slow imperceptible push-in toward Luna's face.
Soft Parisian office window light. Emotional thriller mood.
Face completely stable, no smile added, no expression change, no eye blink forced.
Natural breathing only. No hair movement. Realistic film look.
```

**Plan 6 — Luna enfant + poupée**
```
Cinematic 4-second shot. Slow gentle push-in toward a small purple velvet doll
held by a child. Warm indoor light, emotional comfort scene.
Child's face stable, no expression drift. Doll's fabric texture preserved.
Soft focus pull onto the doll. No exaggerated emotion.
```

**Plan 9 — Aby enfant + jeton noir**
```
Cinematic 4-second close-up. A child's hand slowly deposits a black token
on a miniature city model. Focus pull from the hand to the token.
Then gradual fade to black. No face distortion. Deliberate, calm movement.
Strategic mood. No sudden cuts.
```

### 7.3 Grille de score par plan (35 points max)

Utiliser la grille de `IMAGE_TO_VIDEO_TEST_MATRIX.md` :

| Critère | /5 | Plan 2 | Plan 6 | Plan 9 |
|---|---|---|---|---|
| Stabilité visage / objet | /5 | | | |
| Respect image source | /5 | | | |
| Mouvement de caméra | /5 | | | |
| Ambiance cinéma | /5 | | | |
| Peu d'artefacts | /5 | | | |
| Coût / crédits | /5 | | | |
| Simplicité workflow | /5 | | | |
| **Total** | /35 | | | |

**Seuil de validation : 25/35 minimum sur les 3 plans.**

Si un seul plan passe < 25/35, l'outil n'est pas validé pour la production du teaser.

### 7.4 Soumission au Quality Gate (VM Linux)

```bash
# Sur la VM Linux, après génération des clips sur Windows :
cd ~/PROJETS/YAWATCH_LUNA_STORIES
python3 - <<'EOF'
from app.quality_gate import QualityGate
from pathlib import Path

gate = QualityGate()

# Tester chaque clip généré
for clip_path in [
    "/mnt/yawatch-outputs/clips/plan_02_luna_portrait.mp4",
    "/mnt/yawatch-outputs/clips/plan_06_luna_enfant_poupee.mp4",
    "/mnt/yawatch-outputs/clips/plan_09_aby_jeton.mp4",
]:
    context = {
        "i2v_tool": "comfyui_animatediff_sd15",  # ou "cogvideox_2b"
        "image_paths": [clip_path],  # pour le check placeholder
        "plan_count": 1,
        "duration": 5.0,
        "audio_present": False,  # test clip uniquement, pas le montage final
    }
    report = gate.run(video_context=context)
    print(f"\n{Path(clip_path).name}")
    print(f"  Technique  : {report.verdict_technique.status}")
    print(f"  Mouvement  : {report.verdict_mouvement.status}")
    print(f"  Son        : {report.verdict_son.status}")
    print(f"  Cohérence  : {report.verdict_coherence_personnage.status}")
    print(f"  Statut     : {report.current_status.value}")
EOF
```

### 7.5 Décision après les tests

| Score moyen | Décision |
|---|---|
| ≥ 28/35 sur les 3 plans | Outil **validé** — intégrer dans I2V_PRODUCTION_PACK |
| 25-27/35 | Outil **conditionnel** — utiliser uniquement pour les plans simples (plan 1, plan 7) |
| < 25/35 | Outil **non retenu** — ne pas lancer la production du teaser avec cet outil |

---

## ÉTAPE 8 — Règles de non-régression pipeline

Ces règles s'appliquent pendant toute la phase d'installation et de test.

1. **Aucune modification de `app/main.py`, `app/export_manager.py`, `app/quality_gate.py`** pendant la phase de test.

2. **`app/i2v_engine/` est un module additionnel** — il n'est jamais importé par les modules existants.

3. **Les 88 tests existants doivent rester verts** à tout moment. Après chaque modification du repo : `python3 -m pytest tests/ -q`.

4. **Tout clip généré sur Windows reste `prototype_technique`** jusqu'à `advance_to_candidat()` explicite depuis la VM Linux.

5. **Le statut `teaser_valide` ne peut être assigné que par `mark_human_approved("Ludovic")`** — aucune automatisation ne peut atteindre ce statut.

6. **Le dossier `KLING_READY_PACK_001/` n'est pas utilisé** dans ce workflow — les images source viennent de `assets/luna_stories_assets/`.

---

## Résumé des décisions verrouillées

| Décision | Statut |
|---|---|
| Wan2.1 14B | **Exclu** — VRAM insuffisante sur cette station |
| CogVideoX-5B | **Non retenu** — trop serré sur cette station |
| CogVideoX-2B | **Test uniquement** — si passe les 3 plans, peut être retenu |
| ComfyUI + AnimateDiff SD1.5 | **Premier axe local** — installation prioritaire |
| Kling | **Exclu définitivement** (décision 2026-06-20) |
| Machine cible finale | RTX 4090 24 GB · 64 GB RAM · 2 TB NVMe |
| Statut officiel sur cette station | **Station légère** — pas l'usine finale complète |

---

## Ordre d'exécution recommandé

```
☐ 1. Vérifier VRAM disponible (nvidia-smi ou dxdiag)
☐ 2. Nettoyage disque — libérer 20 GB minimum
☐ 3. Installer ComfyUI portable (option A)
☐ 4. Tester API ComfyUI : http://localhost:8188 répond
☐ 5. Installer ComfyUI-Manager
☐ 6. Installer ComfyUI-AnimateDiff-Evolved via Manager
☐ 7. Installer ComfyUI_IPAdapter_plus via Manager
☐ 8. Télécharger Realistic Vision V6 checkpoint
☐ 9. Télécharger mm_sd_v15_v3.safetensors (motion module)
☐ 10. Télécharger ip-adapter_sd15.safetensors + clip_vision_g.safetensors
☐ 11. Configurer le dossier partagé Windows ↔ Linux VM
☐ 12. Tester un clip AnimateDiff minimal (image test, pas asset YAWatch)
☐ 13. [Optionnel] Installer CogVideoX-2B dans environnement isolé
☐ 14. Générer les 3 plans tests avec les prompts définis en Étape 7
☐ 15. Soumettre au Quality Gate (VM Linux)
☐ 16. Score ≥ 25/35 → décision de Ludovic sur la validation officielle
```

---

*Station Légère YAWatch-LUNA Setup v1.0 — 2026-06-20*  
*Référence : `YAWATCH_LUNA_FACTORY_MASTER_PLAN.md` · `I2V_ENGINE_DECISION_MATRIX.md`*
