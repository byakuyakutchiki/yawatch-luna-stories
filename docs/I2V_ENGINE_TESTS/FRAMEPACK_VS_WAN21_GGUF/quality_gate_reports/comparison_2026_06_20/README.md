# I2V Quality Gate Reports — 2026-06-20

## Objectif

Tester le nouveau gate automatique sur les clips bruts I2V Luna.

Ce gate ne valide pas artistiquement une video. Il filtre automatiquement les clips avant visionnage humain.

## Seuils bloquants

| Metrique | Seuil |
|---|---:|
| `face_identity_ssim_min` | `>= 0.85` |
| `face_lighting_peak_to_peak_pct` | `<= 15.0` |
| `face_flicker_mean_abs_delta` | `<= 0.5` |

## Resultats

| Clip | Status | Identite | Lumiere visage | Flicker visage |
|---|---|---:|---:|---:|
| Wan motion | `FAIL` | `0.5222` | `27.4215%` | `1.3071` |
| Wan lighting stable | `FAIL` | `0.5002` | `28.3726%` | `1.2967` |
| FramePack | `PASS` | `0.9254` | `10.6931%` | `0.1616` |

## Decision

```text
Wan GGUF est rejete par le gate automatique pour ce plan Luna.
FramePack passe le gate automatique pour stabilite identite/lumiere/flicker.
FramePack reste soumis a validation humaine Ludovic.
```

## Fichiers

- `wan_motion.i2v_quality_gate.json`
- `wan_lighting_stable.i2v_quality_gate.json`
- `framepack.i2v_quality_gate.json`

## Commande type

```powershell
$repo="C:\Users\saint\Documents\Codex\2026-06-09\yawatch-luna-stories-public-yawatch-luna\work\yawatch-luna-stories"
$py="C:\Users\saint\Documents\Codex\ComfyUI\.venv\Scripts\python.exe"
& $py -m app.i2v_quality_gate "$repo\docs\I2V_ENGINE_TESTS\FRAMEPACK_VS_WAN21_GGUF\outputs\framepack_plan02_luna_test_001\YAWATCH_FRAMEPACK_PLAN02_LUNA_TEST_00001.mp4"
```
