# Test Result — FramePack PLAN02 Luna

Date: 2026-06-20

## Statut

```text
SUCCESS_MP4_GENERATED_FRAMEPACK_CANDIDATE
```

FramePack a produit un premier MP4 local sur Windows avec la meme image canonique de Luna que les tests Wan.

Ce test sert a comparer FramePack contre Wan GGUF sur:

- stabilite lumiere;
- maintien identite;
- mouvement organique;
- rigidite cou / epaules / cheveux;
- exploitabilite YAWatch-LUNA.

## Fichiers

- `YAWATCH_FRAMEPACK_PLAN02_LUNA_TEST_00001.mp4`
- `YAWATCH_FRAMEPACK_PLAN02_LUNA_TEST_00001.png`
- `YAWATCH_FRAMEPACK_PLAN02_LUNA_TEST_CONTACT_SHEET.jpg`
- `YAWATCH_FRAMEPACK_PLAN02_LUNA_TEST_CONTACT_SHEET_FULL.jpg`
- `ffprobe.json`

Copie locale directe pour upload ChatGPT:

```text
C:\Users\saint\Downloads\YAWATCH_FRAMEPACK_PLAN02_LUNA_TEST_00001.mp4
```

Copie locale avec preuves:

```text
C:\Users\saint\Downloads\YAWatch_FramePack_PLAN02_Luna_Test_001\
```

## Parametres principaux

| Champ | Valeur |
|---|---|
| Moteur | FramePack |
| Modele | `FramePackI2V_HY_fp8_e4m3fn.safetensors` |
| Base precision | `bf16` |
| Quantization | `fp8_e4m3fn` |
| VAE | `hunyuan_video_vae_bf16.safetensors` |
| Text encoders | `clip_l.safetensors` + `llava_llama3_fp16.safetensors` |
| CLIP Vision | `sigclip_vision_patch14_384.safetensors` |
| Image | `luna.png` |
| Resolution sortie | `480x832` |
| Frames sortie | `145` |
| FPS | `16` |
| Duree sortie | `9.0625 s` |
| Steps | `20` |
| CFG | `1.0` |
| Guidance scale | `10.0` |
| Sampler | `unipc_bh1` |
| Seed | `2406202621` |
| Temps generation | environ `1776 s` |

## Comportement inattendu

Le workflow demandait:

```text
total_second_length = 5.0
frame_rate = 16
```

La sortie reelle est:

```text
9.0625 s
145 frames
```

Ce comportement doit etre compris avant production. FramePack peut arrondir ou etendre la duree selon `latent_window_size` et sa logique interne de fenetres temporelles.

## Prompt positif

```text
Luna breathing softly, subtle coordinated shoulder movement, slight natural head tilt, gentle natural hair inertia following the head motion, stable consistent lighting, same lighting as the input image, soft diffused daylight, skin tone constant, same lighting throughout the entire video, portrait photography, natural human presence, premium psychological thriller, restrained emotion, realistic skin, no text
```

## Prompt negatif

```text
different person, identity change, face swap, deformed face, distorted eyes, asymmetric eyes, melting face, bad anatomy, child, teen, glamour, sexualized, cartoon, anime, cyberpunk, neon, purple dominant lighting, changing skin tone, inconsistent lighting, exposure flicker, flickering light, harsh shadows, changing colors, stiff statue, frozen shoulders, frozen hair, text, watermark, logo, low quality, heavy flicker, jitter, violent motion
```

## Observation visuelle Codex sur contact sheet complete

Sur les 18 frames extraites couvrant toute la duree:

- identite de Luna globalement stable;
- visage non monstrueux sur les frames inspectees;
- lumiere visuellement plus stable que les tests Wan precedents;
- teint moins fluctuant sur la planche que Wan;
- expression legerement plus adoucie / souriante par moments;
- mouvement apparent mais encore a confirmer en lecture reelle;
- cheveux et epaules ne peuvent pas etre juges correctement uniquement sur contact sheet.

Limite importante: la contact sheet ne permet pas de juger le flicker fin, la qualite du mouvement, la respiration ou la sensation cinematographique. Ludovic doit regarder le MP4.

## Comparaison provisoire avec Wan

| Critere | Wan GGUF motion / lighting tests | FramePack test |
|---|---|---|
| Identite | stable | stable |
| Lumiere sur contact sheet | variations visibles | plus stable visuellement |
| Teint | fluctuant | moins fluctuant |
| Duree controlee | oui, environ 5 s | non, sortie 9.06 s |
| Temps generation | 26 a 36 min | 29 min 36 s |
| Mouvement organique | insuffisant selon diagnostic | a evaluer en lecture reelle |
| Risque principal | lumiere/teint | expression peut s'adoucir, duree non maitrisee |

## Verdict provisoire

```text
FramePack devient candidat serieux pour corriger la stabilite lumineuse.
Il n'est pas encore valide comme moteur officiel.
Il faut visionner le MP4 complet et maitriser la duree de sortie.
```

## Prochaine action

1. Ludovic regarde `YAWATCH_FRAMEPACK_PLAN02_LUNA_TEST_00001.mp4`.
2. Comparer directement contre:
   - `YAWATCH_WAN21_PLAN02_LUNA_MOTION_TEST_00001.mp4`
   - `YAWATCH_WAN21_PLAN02_LUNA_LIGHTING_STABLE_TEST_00001.mp4`
3. Noter:
   - stabilite lumiere;
   - identite Luna;
   - respiration;
   - cou / epaules;
   - cheveux;
   - emotion YAWatch-LUNA.
4. Si FramePack est meilleur, lancer un second test FramePack avec duree maitrisee et expression plus grave.
