# Test Result — Wan2.1 GGUF PLAN02 Luna motion

Date: 2026-06-20

## Statut

```text
SUCCESS_MP4_GENERATED_NEEDS_HUMAN_REVIEW
```

Wan2.1 GGUF a produit un second MP4 local sur Windows avec un prompt plus oriente mouvement naturel.

Ce resultat ne doit pas etre considere comme une validation artistique finale.

## Fichiers

- `YAWATCH_WAN21_PLAN02_LUNA_MOTION_TEST_00001.mp4`
- `YAWATCH_WAN21_PLAN02_LUNA_MOTION_TEST_00001.png`
- `YAWATCH_WAN21_PLAN02_LUNA_MOTION_TEST_CONTACT_SHEET.jpg`
- `ffprobe.json`

Copie locale pratique pour upload ChatGPT:

```text
C:\Users\saint\Downloads\YAWatch_Wan21_Motion_Test_001\
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
| Temps generation | environ `2192 s` |

## Prompt positif

```text
cinematic premium psychological thriller portrait of Luna, adult woman, same identity as source image, Luna breathing softly, subtle shoulder movement, slight natural head tilt, gentle natural hair movement, imperceptible slow push-in, restrained emotion, calm serious gaze, Paris La Defense office atmosphere, consistent stable lighting throughout, consistent natural skin tone, realistic skin, shallow depth of field, film grain, high quality, no text
```

## Prompt negatif

```text
different person, identity change, face swap, deformed face, distorted eyes, asymmetric eyes, melting face, bad anatomy, child, teen, glamour, sexualized, cartoon, anime, cyberpunk, neon, purple dominant lighting, changing skin tone, inconsistent lighting, exposure flicker, text, watermark, logo, low quality, heavy flicker, jitter, violent motion
```

## Observation visuelle Codex sur contact sheet

Sur les 10 frames extraites:

- identite de Luna globalement stable;
- visage non monstrueux sur les frames inspectees;
- mouvement visible, plus present que le premier test a 8 fps;
- rendu encore tres portrait pose;
- variations de lumiere et de teint encore visibles;
- expression legerement changeante mais pas incoherente sur la planche.

Limite importante: une contact sheet ne remplace pas le visionnage du MP4. Le flicker, les micro-tremblements et la sensation emotionnelle doivent etre juges en lecture reelle.

## Comparaison rapide avec le premier test

| Critere | Premier test | Motion test |
|---|---|---|
| FPS | 8 | 16 |
| Frames | 41 | 81 |
| Duree | 5.125 s | 5.0625 s |
| Mouvement percu | faible | plus visible |
| Stabilite identite sur contact sheet | correcte | correcte |
| Risque visible | teint/lumiere variables | teint/lumiere variables |

## Verdict provisoire

```text
Wan GGUF reste candidat reel.
Motion test techniquement produit.
Validation artistique en attente Ludovic / analyse video complete.
```

## Prochaine action

Regarder le MP4 en boucle et noter:

1. stabilite du visage;
2. flicker reel;
3. naturel du mouvement;
4. coherence emotionnelle YAWatch-LUNA;
5. difference ressentie par rapport au premier Wan test.
