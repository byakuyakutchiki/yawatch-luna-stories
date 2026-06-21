# Comparaison gouvernée FramePack vs Wan natif — plan02 Luna (2026-06-22)

Générée via le **pipeline gouverné** (MotionDirector → job scellé `job_hash` → backend ComfyUI → Quality Gate I2V), même prompt de mouvement, mêmes seuils. RTX 6000 Ada (cloud RunPod).

- FramePack : `FramePackI2V_HY_fp8_e4m3fn` (HunyuanVideo)
- Wan : `wan2.1_i2v_480p_14B_fp8_e4m3fn` — **natif fp8** (PAS le GGUF Q5 qui s'était effondré le 20 juin)

## Quality Gate I2V (clip entier — seuils intacts)

| Métrique (seuil) | FramePack | Wan natif fp8 | Wan GGUF (20 juin) |
|---|---|---|---|
| Identité SSIM (≥ 0.85) | 0.77 ❌ | 0.728 ❌ | 0.50 ❌ |
| Lumière visage (≤ 15 %) | 10.6 % ✅ | 23.5 % ❌ | 28 % ❌ |
| Flicker visage (≤ 0.5) | 0.10 ✅ | 0.39 ✅ | 1.3 ❌ |
| **Verdict** | FAIL (identité) | FAIL (identité + lumière) | FAIL (tout) |

## Mouvement réel (optical flow mean — échantillon 60 frames)

| Région | FramePack | Wan natif | Ratio |
|---|---|---|---|
| Visage | 0.111 | 0.231 | **2.1×** |
| Cheveux | 0.086 | 0.185 | **2.2×** |
| Épaules | 0.096 | 0.270 | **2.8×** |
| Image entière | 0.058 | 0.142 | **2.4×** |
| Pic visage (p95) | 0.23 | 1.01 | **4.4×** |

## Conclusions

1. **Wan natif >> Wan GGUF** : le natif fp8 corrige massivement le GGUF (identité 0.73 vs 0.50, flicker 0.39 vs 1.3). La quantization GGUF était bien la cause de l'échec du 20 juin.
2. **Wan est ~2.5× plus vivant** que FramePack sur toutes les régions — c'est le mouvement recherché, que FramePack (figé) ne donne pas.
3. **Mur identité-vs-mouvement confirmé** : ce mouvement coûte la stabilité (identité 0.728, lumière épaules 41 %). FramePack est plus stable mais mou.
4. **Aucun moteur seul ne passe le gate** avec du vrai mouvement → la solution cible est le **pipeline 2 étages** (mouvement Wan + restauration visage = « Kling maison »).

> Les métriques sont des signaux machine. La décision finale reste à Ludovic (visionnage humain des 2 clips).

Fichiers : `motion_metrics_report.md`, `motion_metrics.json`.
