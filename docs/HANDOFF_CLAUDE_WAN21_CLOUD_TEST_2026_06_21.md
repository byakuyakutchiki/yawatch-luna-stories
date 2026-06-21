# Handoff Claude — Wan2.1 Cloud Test

Date: 2026-06-21

## Objectif

Tester Wan2.1 sur RunPod comme challenger prioritaire, parce que le local est trop lent pour produire.

But concret:

```text
générer vite sur cloud
→ comparer Wan2.1 contre FramePack
→ appliquer les mêmes métriques
→ choisir le moteur de production sur preuve MP4 + Quality Gate
```

## Correction importante

Ne pas écrire:

```text
Wan2.1 est officiellement validé.
```

État réel:

```text
FramePack = seul moteur qui a déjà passé le Quality Gate I2V.
Wan GGUF local = a échoué au Quality Gate.
Wan2.1 cloud / natif / meilleur GPU = pas encore validé.
```

Décision produit:

```text
Wan2.1 devient le challenger prioritaire à tester sur cloud.
Il devient moteur officiel seulement si MP4 + Quality Gate + validation Ludovic passent.
```

## État RunPod connu

Dernier retour Claude:

```text
GPU: NVIDIA RTX PRO 4500 Blackwell
VRAM: 32623 MiB
Direct SSH: root@213.173.104.7 -p 22531
Pod: dramatic_silver_orangutan
```

Conséquence:

```text
32 GB VRAM ouvre la possibilité de tester un Wan2.1 moins dégradé que le GGUF local,
voire un workflow plus qualitatif si les modèles sont disponibles.
```

## Ce qui existe vraiment dans le repo

Workflows existants:

```text
docs/I2V_ENGINE_TESTS/FRAMEPACK_VS_WAN21_GGUF/workflows/framepack_plan02_luna_api_test_001.json
docs/I2V_ENGINE_TESTS/FRAMEPACK_VS_WAN21_GGUF/workflows/wan21_gguf_plan02_luna_api_workflow_success_001.json
docs/I2V_ENGINE_TESTS/FRAMEPACK_VS_WAN21_GGUF/workflows/wan21_gguf_plan02_luna_motion_test_success_001.json
docs/I2V_ENGINE_TESTS/FRAMEPACK_VS_WAN21_GGUF/workflows/wan21_gguf_plan02_luna_lighting_stable_test_001.json
```

Quality Gate:

```text
app/i2v_quality_gate.py
app/video_metrics_evaluator.py
```

Rapports existants:

```text
docs/I2V_ENGINE_TESTS/FRAMEPACK_VS_WAN21_GGUF/metric_reports/comparison_2026_06_20/
docs/I2V_ENGINE_TESTS/FRAMEPACK_VS_WAN21_GGUF/quality_gate_reports/comparison_2026_06_20/
```

## Commande initiale obligatoire côté VM

Avant toute action:

```bash
cd /home/ludo/PROJETS/YAWATCH_LUNA_STORIES
git pull --rebase origin master
```

Puis vérifier:

```bash
ls docs/I2V_ENGINE_TESTS/FRAMEPACK_VS_WAN21_GGUF/workflows/
ls app/i2v_quality_gate.py app/video_metrics_evaluator.py
```

## Ce qu'il ne faut pas faire

Ne pas utiliser ces commandes telles quelles:

```bash
podctl start yawatch-wan-test
python app/motion_director.py --job teaser_wan --batch 9 --engine wan21
python app/generate_report.py --output ...
```

Raison:

```text
Ces commandes ne correspondent pas à l'état réel du repo.
Elles risquent de faire perdre du temps ou de produire des artefacts non gouvernés.
```

## Protocole correct du test Wan cloud

### Étape 1 — Vérifier le pod

Sur le pod:

```bash
nvidia-smi
df -h
python --version
python -c "import torch; print(torch.__version__, torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

### Étape 2 — Synchroniser le repo sur le pod

```bash
cd /workspace
if [ ! -d yawatch-luna-stories ]; then
  git clone https://github.com/byakuyakutchiki/yawatch-luna-stories.git
fi
cd /workspace/yawatch-luna-stories
git pull --rebase origin master
```

### Étape 3 — Vérifier les modèles Wan disponibles

Chercher:

```bash
find /workspace/ComfyUI/models -iname "*wan*" -o -iname "*umt5*" -o -iname "*clip_vision_h*" -o -iname "*vae*"
```

À noter dans le rapport:

- modèle Wan exact;
- text encoder exact;
- VAE exact;
- CLIP Vision exact;
- format: GGUF ou non-GGUF.

### Étape 4 — Lancer un seul test Wan Luna

Utiliser comme base un workflow réellement présent:

```text
docs/I2V_ENGINE_TESTS/FRAMEPACK_VS_WAN21_GGUF/workflows/wan21_gguf_plan02_luna_motion_test_success_001.json
```

Si Claude crée un nouveau workflow Wan natif, il doit le commiter ensuite dans:

```text
docs/I2V_ENGINE_TESTS/WAN21_CLOUD_TESTS/workflows/
```

Et documenter:

```text
modèle exact + paramètres + seed + durée + fps + génération time
```

### Étape 5 — Appliquer le Quality Gate actuel

Ne pas assouplir les seuils avant preuve.

Commande:

```bash
cd /workspace/yawatch-luna-stories
python -m app.i2v_quality_gate /workspace/ComfyUI/output/YOUR_WAN_TEST.mp4 \
  --output-json /workspace/ComfyUI/output/YOUR_WAN_TEST.i2v_quality_gate.json
```

Seuils actuels:

| Métrique | Seuil |
|---|---:|
| `face_identity_ssim_min` | `>= 0.85` |
| `face_lighting_peak_to_peak_pct` | `<= 15.0` |
| `face_flicker_mean_abs_delta` | `<= 0.5` |

### Étape 6 — Décision

Si Wan passe:

```text
Wan devient candidat production prioritaire.
Ludovic doit visionner le MP4.
```

Si Wan échoue:

```text
Ne pas forcer la production Wan.
Comparer pourquoi: identité, lumière ou flicker.
FramePack reste baseline.
```

Si Wan échoue mais offre clairement un meilleur mouvement:

```text
option hybride:
Wan pour plans où le mouvement compte,
FramePack pour portraits / plans émotionnels stables.
```

## Livrables obligatoires

Claude doit produire ou déposer:

```text
MP4 Wan test
contact sheet
ffprobe.json
i2v_quality_gate.json
workflow JSON utilisé
rapport court d'interprétation
```

Emplacement recommandé dans le repo:

```text
docs/I2V_ENGINE_TESTS/WAN21_CLOUD_TESTS/outputs/wan21_cloud_plan02_luna_test_001/
docs/I2V_ENGINE_TESTS/WAN21_CLOUD_TESTS/workflows/
```

## Message opérationnel à Claude

```text
Claude, la décision est de tester Wan2.1 en priorité sur cloud, pas de le déclarer officiel sans preuve.

Fais d'abord git pull --rebase origin master.
Utilise les vrais workflows dans docs/I2V_ENGINE_TESTS/FRAMEPACK_VS_WAN21_GGUF/workflows/.
Applique le Quality Gate actuel app/i2v_quality_gate.py sans assouplir les seuils.

Livrables obligatoires:
- MP4
- contact sheet
- ffprobe.json
- .i2v_quality_gate.json
- workflow JSON exact
- rapport d'interprétation

Si Wan passe le gate et que Ludovic valide visuellement, on l'adopte.
Sinon FramePack reste baseline ou on passe en stratégie hybride.
```

## Règle coût

Le GPU coûte à l'heure.

Donc:

```text
1 test Wan d'abord.
Pas de batch 9 clips tant que le test unique n'a pas produit MP4 + Quality Gate.
Arrêter le pod si blocage.
```
