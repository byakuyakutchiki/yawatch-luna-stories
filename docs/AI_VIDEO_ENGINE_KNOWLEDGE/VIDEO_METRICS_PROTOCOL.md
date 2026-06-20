# Video Metrics Protocol

## Objectif

Transformer les observations artistiques recurrentes en mesures objectives.

Ce protocole ne remplace pas la validation humaine. Il sert a detecter rapidement:

- instabilite lumiere;
- flicker;
- derive visage;
- manque de mouvement organique;
- differences objectives entre moteurs I2V.

## Outil local actuel

Script:

```text
app/video_metrics_evaluator.py
```

Python utilise sur Windows:

```text
C:\Users\saint\Documents\Codex\ComfyUI\.venv\Scripts\python.exe
```

Dependances deja presentes dans le venv ComfyUI:

```text
numpy
opencv-python
```

## Commande type

```powershell
$repo="C:\Users\saint\Documents\Codex\2026-06-09\yawatch-luna-stories-public-yawatch-luna\work\yawatch-luna-stories"
$py="C:\Users\saint\Documents\Codex\ComfyUI\.venv\Scripts\python.exe"
& $py "$repo\app\video_metrics_evaluator.py" `
  "$repo\docs\I2V_ENGINE_TESTS\FRAMEPACK_VS_WAN21_GGUF\outputs\wan21_plan02_luna_motion_test_001\YAWATCH_WAN21_PLAN02_LUNA_MOTION_TEST_00001.mp4" `
  "$repo\docs\I2V_ENGINE_TESTS\FRAMEPACK_VS_WAN21_GGUF\outputs\framepack_plan02_luna_test_001\YAWATCH_FRAMEPACK_PLAN02_LUNA_TEST_00001.mp4" `
  --output-dir "$repo\docs\I2V_ENGINE_TESTS\FRAMEPACK_VS_WAN21_GGUF\metric_reports\comparison_YYYY_MM_DD"
```

## Zones mesurees

Les regions sont approximatives pour les portraits verticaux YAWatch-LUNA:

| Region | Role |
|---|---|
| `face` | stabilite visage, lumiere visage, proxy identite |
| `hair` | mouvement cheveux + variation lumiere cheveux |
| `shoulders` | respiration / corps / rigidite |
| `background` | stabilite decor |
| `full_frame` | signal global |

Ces regions doivent etre adaptees pour:

- plans larges;
- objets;
- vehicules;
- decors sans personnage;
- groupes de personnages.

## Metriques

### Face SSIM

Compare la zone visage de la premiere frame aux frames suivantes.

Lecture:

- haut = visage stable;
- bas = derive, variation lumineuse forte ou changement morphologique.

Limite:

```text
Ce n'est pas une vraie reconnaissance faciale.
```

### Luminance peak-to-peak

Mesure l'amplitude entre la frame la plus sombre et la plus claire.

Lecture:

- faible = lumiere stable;
- elevee = changement de teint / lumiere / exposition.

### Flicker mean abs delta

Mesure la variation moyenne de luminance entre frames consecutives.

Lecture:

- faible = peu de clignotement temporel;
- elevee = flicker visible probable.

### Optical flow

Mesure le mouvement pixel entre frames.

Lecture:

- trop bas = image figee;
- trop haut = mouvement brutal, jitter ou deformation possible.

## Seuils actuels

Ces seuils sont provisoires et bases sur les premiers tests Luna:

| Signal | PASS provisoire |
|---|---:|
| `identity_ssim_face_min` | `>= 0.72` |
| `face.luminance_peak_to_peak_pct` | `<= 10%` |
| `face.flicker_mean_abs_delta` | `<= 2.0` |
| `shoulders.optical_flow_mean` | `>= 0.08` |
| `hair.optical_flow_mean` | `>= 0.08` |

Ils doivent evoluer avec plus de clips.

## Regle de gouvernance

Aucun clip ne doit etre promu uniquement avec ces chiffres.

Statut valide seulement si:

```text
metrics objectives + contact sheet + visionnage humain Ludovic
```

## Gate automatique I2V

Script:

```text
app/i2v_quality_gate.py
```

Seuils bloquants actuels:

| Metrique | Seuil |
|---|---:|
| `face_identity_ssim_min` | `>= 0.85` |
| `face_lighting_peak_to_peak_pct` | `<= 15.0` |
| `face_flicker_mean_abs_delta` | `<= 0.5` |

Regle:

```text
FAIL automatique = clip rejete avant validation humaine.
PASS automatique = clip autorise pour visionnage humain, pas validation finale.
```

Commande:

```powershell
$repo="C:\Users\saint\Documents\Codex\2026-06-09\yawatch-luna-stories-public-yawatch-luna\work\yawatch-luna-stories"
$py="C:\Users\saint\Documents\Codex\ComfyUI\.venv\Scripts\python.exe"
& $py -m app.i2v_quality_gate "$repo\path\to\clip.mp4"
```

## Extensions futures

Outils a evaluer plus tard:

- VBench;
- Surveyor2;
- NVIDIA Cosmos Evaluator;
- FovVideoVDP;
- metrics LPIPS / CLIPScore / FVD.

Priorite actuelle:

```text
OpenCV local d'abord, car il donne deja des chiffres exploitables sans cloud ni installation lourde.
```
