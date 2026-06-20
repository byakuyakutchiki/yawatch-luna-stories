# Test Result — Wan2.1 GGUF PLAN02 Luna adulte

Date: 2026-06-20

## Statut

```text
SUCCESS_MP4_GENERATED
```

Wan2.1 GGUF a produit un premier MP4 local sur Windows.

## Fichiers

- `YAWATCH_WAN21_PLAN02_LUNA_TEST_00001.mp4`
- `YAWATCH_WAN21_PLAN02_LUNA_TEST_contact.jpg`

Copie locale pratique:

```text
C:\Users\saint\Downloads\YAWatch_Wan21_Test_001\
```

## Parametres principaux

| Champ | Valeur |
|---|---|
| Modele | `wan2.1-i2v-14b-480p-Q5_K_S.gguf` |
| Text encoder | `umt5_xxl_fp8_e4m3fn_scaled.safetensors` |
| CLIP Vision | `clip_vision_h.safetensors` |
| VAE | `wan_2.1_vae.safetensors` |
| Image | `luna.png` |
| Resolution | `480x832` |
| Frames | `41` |
| FPS | `8` |
| Duree | `5.125 s` |
| Steps | `12` |
| CFG | `1.0` |
| Sampler | `uni_pc` |
| Scheduler | `simple` |
| Seed | `2406202618` |
| Temps generation | environ `872 s` |

## Incident corrige

Premier essai: crash ComfyUI lors du chargement de `umt5_xxl_fp8_e4m3fn_scaled.safetensors` via `CLIPLoaderGGUF`.

Cause: mauvais loader. Le modele video est GGUF, mais le text encoder Wan est un `.safetensors`.

Correction:

- `UnetLoaderGGUF` pour `wan2.1-i2v-14b-480p-Q5_K_S.gguf`
- `CLIPLoader` standard pour `umt5_xxl_fp8_e4m3fn_scaled.safetensors`

## Observation visuelle rapide Codex

Sur la planche extraite:

- visage globalement coherent;
- variation de lumiere et de teint visible au milieu;
- expression legerement plus dure sur certaines frames;
- pas de deformation monstrueuse evidente sur les frames extraites.

Ce jugement est insuffisant pour validation artistique. Ludovic doit regarder le MP4 en lecture reelle.

## Verdict provisoire

```text
Wan GGUF = premier MP4 produit, candidat reel.
Validation artistique = en attente Ludovic.
```

## Prochaine action

Ludovic doit regarder le MP4 et noter:

1. stabilite du visage;
2. flicker;
3. naturel du mouvement;
4. coherence emotionnelle YAWatch-LUNA.

