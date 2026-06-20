# Test Result — Wan2.1 GGUF PLAN02 Luna lighting stable

Date: 2026-06-20

## Statut

```text
SUCCESS_MP4_GENERATED_LIGHTING_STABILITY_TEST
```

Wan2.1 GGUF a produit un troisieme MP4 local sur Windows avec un prompt explicitement oriente stabilite lumineuse.

Ce test est une experience comparative, pas une validation artistique finale.

## Correction de gouvernance

La recommandation source proposait de baisser un `guidance_scale` suppose entre `6` et `7` vers `5.0`.

Le workflow reel YAWatch n'etait pas dans cette situation:

- le sampler utilise `cfg=1.0`;
- il n'y avait donc pas de guidance haute a baisser;
- monter `cfg` a `5.0` aurait change deux variables a la fois et aurait potentiellement augmente la reinvention de l'image.

Decision appliquee:

```text
Garder cfg=1.0.
Garder le meme seed.
Garder 81 frames / 16 fps.
Changer uniquement le prompt positif et le prompt negatif pour isoler l'effet du verrouillage lumineux.
```

## Fichiers

- `YAWATCH_WAN21_PLAN02_LUNA_LIGHTING_STABLE_TEST_00001.mp4`
- `YAWATCH_WAN21_PLAN02_LUNA_LIGHTING_STABLE_TEST_00001.png`
- `YAWATCH_WAN21_PLAN02_LUNA_LIGHTING_STABLE_TEST_CONTACT_SHEET.jpg`
- `ffprobe.json`

Copie locale directe pour upload ChatGPT:

```text
C:\Users\saint\Downloads\YAWATCH_WAN21_PLAN02_LUNA_LIGHTING_STABLE_TEST_00001.mp4
```

Copie locale avec preuves:

```text
C:\Users\saint\Downloads\YAWatch_Wan21_Lighting_Stable_Test_001\
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
| Frames | `81` |
| FPS | `16` |
| Duree | `5.0625 s` |
| Steps | `12` |
| CFG | `1.0` |
| Sampler | `uni_pc` |
| Scheduler | `simple` |
| Seed | `2406202618` |
| Temps generation | environ `1592 s` |

## Prompt positif

```text
cinematic premium psychological thriller portrait of Luna, adult woman, same identity as source image, Luna breathing softly, subtle shoulder movement, slight natural head tilt, gentle natural hair movement, imperceptible slow push-in, restrained emotion, calm serious gaze, Paris La Defense office atmosphere, stable consistent lighting, soft diffused daylight, skin tone constant, same lighting throughout the entire video, realistic skin, shallow depth of field, film grain, high quality, no text
```

## Prompt negatif

```text
different person, identity change, face swap, deformed face, distorted eyes, asymmetric eyes, melting face, bad anatomy, child, teen, glamour, sexualized, cartoon, anime, cyberpunk, neon, purple dominant lighting, changing skin tone, inconsistent lighting, exposure flicker, flickering light, harsh shadows, changing colors, text, watermark, logo, low quality, heavy flicker, jitter, violent motion
```

## Observation visuelle Codex sur contact sheet

Sur les 10 frames extraites:

- identite de Luna globalement stable;
- visage non monstrueux sur les frames inspectees;
- cadrage et mouvement proches du test motion precedent;
- les variations de lumiere/teint semblent encore presentes;
- le prompt de stabilite lumineuse ne montre pas, sur contact sheet, une amelioration massive;
- il faut verifier le flicker en lecture video reelle.

## Comparaison rapide avec le test motion precedent

| Critere | Motion test | Lighting stable test |
|---|---|---|
| Seed | `2406202618` | `2406202618` |
| FPS | `16` | `16` |
| Frames | `81` | `81` |
| CFG | `1.0` | `1.0` |
| Changement principal | prompt mouvement naturel | prompt stabilite lumineuse |
| Hash MP4 | `738DCDC59CE32E1C85DBA60349DDE097215147A734343A506503B3BF74A20594` | `8B90894FA41D74A4C5DAE9BF8BC887AF9969711DE38805A580A4562768468C47` |
| Observation contact sheet | stable mais lumiere variable | tres proche, lumiere encore variable |

## Verdict provisoire

```text
Le prompt de stabilite lumineuse produit un nouveau MP4 valide techniquement.
Il ne prouve pas encore que le probleme de lumiere est resolu.
La validation doit se faire sur le MP4 en lecture reelle.
```

## Prochaine action recommandee

1. Ludovic regarde le MP4 en boucle.
2. Comparer avec `YAWATCH_WAN21_PLAN02_LUNA_MOTION_TEST_00001.mp4`.
3. Si le flicker/lumiere reste genant, tester une vraie solution de post-traitement ou FramePack plutot que multiplier les prompts Wan.
