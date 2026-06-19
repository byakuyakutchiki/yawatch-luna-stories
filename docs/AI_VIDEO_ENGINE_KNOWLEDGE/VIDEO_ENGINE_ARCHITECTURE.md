# VIDEO ENGINE ARCHITECTURE — YAWatch-LUNA

## Métier correspondant
Ingénieur pipeline vidéo IA · Directeur IA Vidéo

## Sources expertes utilisées
- FFmpeg documentation officielle : https://ffmpeg.org/documentation.html
- HuggingFace Diffusers : https://huggingface.co/docs/diffusers
- Kling AI documentation : https://klingai.com/docs
- "Video Production with AI" — pipelines de studios indépendants 2024-2025
- Architecture des pipelines Runway ML et Pika Labs (documentation publique)

## Problème empêché
Confusion entre les étapes du pipeline — en particulier utiliser FFmpeg comme outil
d'animation alors qu'il est uniquement un outil d'assemblage. Cette confusion a produit
le résultat catastrophique de la Phase 14 (zoom tremblant sur photo présenté comme teaser).

## Code repo qui doit respecter ce document
- `app/video_builder.py`
- `app/scene_composer.py`
- `app/export_manager.py`
- Tout futur module d'intégration Kling, Runway, SVD, CogVideoX

## Règles bloquantes avant production vidéo
1. Aucun clip ne peut être déclaré "production_ready" s'il ne provient pas d'un vrai
   outil image-to-video (Kling, SVD, CogVideoX, AnimateDiff) ou d'un Ken Burns validé.
2. FFmpeg ne doit jamais être présenté comme l'étape de génération de mouvement.
3. Chaque étape du pipeline doit produire un artefact validé avant de passer à la suivante.
4. Le pipeline ne s'exécute pas si les assets source ne sont pas validés en amont.

---

## Architecture complète du moteur

```
ÉTAPE 0 — Préparation des assets
    ↓ images 9:16 validées (CHARACTER_LIBRARY_CHECKLIST + TEASER_PRODUCTION_PACK)
    ↓ format : 1080×1920 PNG, profondeur 8-bit, sRGB

ÉTAPE 1 — Génération des clips image-to-video
    ↓ outil : Kling / Runway / Luma / SVD / CogVideoX / AnimateDiff (ComfyUI)
    ↓ entrée : 1 image par plan
    ↓ sortie : 1 clip MP4 de 3-6 secondes par plan, 1080×1920 ou natif
    ↓ validation : visionnage humain obligatoire (Quality Gate visuel)

ÉTAPE 2 — Production audio
    ↓ voix narrateur : ElevenLabs (CANON_NARRATEUR validé)
    ↓ motif musical : fichier validé (version Luna + version Aby)
    ↓ SFX : palette définie dans BIBLE_SFX (à créer)
    ↓ format : WAV 44100 Hz 16-bit ou MP3 320kbps

ÉTAPE 3 — Assemblage (FFmpeg)
    ↓ RÔLE : concaténer les clips, mixer l'audio, incruster les sous-titres
    ↓ entrée : N clips MP4 validés + 1 audio WAV/MP3 + 1 fichier SRT
    ↓ FFmpeg NE génère PAS de mouvement — il assemble uniquement
    ↓ sortie : 1 fichier MP4 assemblé

ÉTAPE 4 — Quality Gate (technique + artistique)
    ↓ validation technique : format, résolution, fps, codec, durée, sync audio
    ↓ validation artistique : lore, personnage, esthétique, rythme
    ↓ validation humaine : visionnage Ludovic sur mobile (casque obligatoire)
    ↓ résultat : STATUS=production_ready ou retour en étape 1/2/3

ÉTAPE 5 — Export final
    ↓ 1080×1920, H.264 (libx264), AAC 128k, -movflags +faststart
    ↓ optimisation mobile : profil baseline, niveau 3.1, bitrate adaptatif
    ↓ vérification automatique des métadonnées
```

---

## Séparation fondamentale des outils

| Outil | Rôle dans le pipeline | Ce qu'il NE fait PAS |
|---|---|---|
| **Kling / Runway / Luma** | Génère du mouvement réel à partir d'une image fixe | N'assemble pas, n'ajoute pas de son |
| **SVD / CogVideoX** | Génère des frames vidéo via modèle diffusion | N'a pas de contrôle précis du mouvement |
| **ComfyUI / AnimateDiff** | Génère des clips localement via workflows | Nécessite GPU, lent, paramétrage complexe |
| **FFmpeg** | Assemble les clips, mixe le son, incruste les sous-titres | **Ne génère pas de mouvement. Jamais.** |
| **MoviePy** | Interface Python pour FFmpeg | Mêmes limites que FFmpeg |
| **Ken Burns (zoompan FFmpeg)** | Effet de recadrage progressif sur image fixe | N'anime pas les éléments dans l'image |
| **ElevenLabs** | Génère la voix off | N'est pas un outil de mixage |

---

## Hiérarchie des outils image-to-video (qualité décroissante)

```
1. Kling Pro / Runway Gen-3 Alpha   → meilleure qualité, cloud payant, ~0.30-0.50€/clip
2. Luma Dream Machine               → qualité élevée, cloud payant, concurrent direct Kling
3. Kling Standard                   → qualité correcte, cloud payant, ~0.05-0.10€/clip
4. CogVideoX (local GPU)            → open source, 5B params, 6GB VRAM min
5. SVD XT (local GPU)               → open source, stabilité moyenne, 8GB VRAM
6. AnimateDiff + SDXL (local GPU)   → open source, 16-32 frames, cohérence variable
7. Ken Burns FFmpeg zoompan         → FALLBACK UNIQUEMENT — 20% des plans max
```

---

## Règles d'intégration entre étapes

### Étape 0 → Étape 1
- Vérifier que chaque image source est en 9:16 (ratio tolérance ±2%)
- Vérifier que la résolution est ≥ 941×1672
- Vérifier que le personnage correspond au canon (CHARACTER_LIBRARY_CHECKLIST)
- Si une image échoue : générer un remplacement, NE PAS continuer avec une image non conforme

### Étape 1 → Étape 3
- Chaque clip doit avoir été visionné avant l'assemblage
- Durée cible par clip : 3-6 secondes selon le plan
- Format cible clip : MP4, H.264, 1080×1920 ou supérieur (FFmpeg redimensionnera)
- Un clip "pas terrible mais passable" n'est pas un clip validé — régénérer

### Étape 2 → Étape 3
- La voix narrateur doit correspondre à CANON_NARRATEUR (fichier validé)
- La durée audio doit correspondre à la durée vidéo totale planifiée ±10%
- Si la voix est générée en plusieurs parties, les jointures doivent être invisibles

### Étape 3 → Étape 4
- FFmpeg doit sortir avec code 0 (pas d'erreur)
- Le fichier MP4 produit doit être lisible sur mobile (test avec vlc ou mpv)
- La sync audio/vidéo doit être vérifiée à la seconde de transition la plus critique

---

## Anti-patterns interdits

```
✗ Utiliser FFmpeg zoompan comme substitut de Kling
✗ Présenter un assemblage FFmpeg d'images fixes comme un "teaser animé"
✗ Valider un clip sans l'avoir regardé
✗ Déclarer STATUS=production_ready depuis le pipeline sans validation humaine
✗ Assembler avant que tous les clips aient été validés individuellement
✗ Utiliser des images placeholder (episode_test/) dans un rendu teaser
✗ Ignorer les erreurs FFmpeg et présenter le fichier de sortie comme valide
```
