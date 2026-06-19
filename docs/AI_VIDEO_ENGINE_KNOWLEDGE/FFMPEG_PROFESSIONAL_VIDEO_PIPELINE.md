# FFMPEG PROFESSIONAL VIDEO PIPELINE — YAWatch-LUNA

## Métier correspondant
Ingénieur pipeline vidéo · Monteur (côté technique)

## Sources expertes utilisées
- FFmpeg documentation officielle : https://ffmpeg.org/ffmpeg-filters.html
- FFmpeg Wiki : https://trac.ffmpeg.org/wiki
- "FFmpeg — The Complete Guide" — Jan Ozer
- Référence xfade : https://ffmpeg.org/ffmpeg-filters.html#xfade
- Référence zoompan : https://ffmpeg.org/ffmpeg-filters.html#zoompan
- Référence colorspace : https://ffmpeg.org/ffmpeg-filters.html#colorspace
- Mobile encoding guidelines : https://trac.ffmpeg.org/wiki/Encode/H.264

## Problème empêché
- Zoom tremblant (zoompan mal paramétré sans fps)
- Décalage audio/vidéo (sync incorrecte avec -shortest)
- Offsets xfade négatifs (crash ou artefact)
- Dégradation colorimétrique lors de la chaîne de filtres
- Fichiers non lisibles sur mobile (manque -movflags +faststart)
- Images pillarboxées ou étirées (scale sans force_original_aspect_ratio)

## Code repo qui doit respecter ce document
- `app/video_builder.py` (entièrement)
- `app/export_manager.py`
- `docs/visual_pipeline_v1.md` (à mettre en cohérence)

## Règles bloquantes avant production vidéo
1. Tout filtre zoompan doit spécifier `fps=25` explicitement.
2. Tout xfade doit avoir un offset ≥ 0 (calculé et vérifié avant exécution).
3. L'export final doit inclure `-movflags +faststart` pour la lecture mobile.
4. Le codec doit être `libx264` avec `-profile:v baseline -level 3.1` pour compatibilité maximale.
5. La résolution de sortie est toujours `1080x1920` — jamais approximée.

---

## Format cible obligatoire

```
Résolution  : 1080 × 1920 (9:16 vertical)
FPS         : 25 (standard Europe/YouTube)
Codec vidéo : libx264
Profil      : baseline (compatibilité mobile maximale)
Niveau      : 3.1
CRF         : 20-23 (20 = haute qualité, 23 = équilibre taille/qualité)
Codec audio : aac
Bitrate audio : 128k
Canaux audio  : stereo (2)
Fréquence ech.: 44100 Hz
Container     : MP4
Faststart     : OUI (-movflags +faststart)
Pixel format  : yuv420p (obligatoire pour compatibilité)
```

---

## 1. Scale — redimensionnement correct

### Le problème
`scale=1080:1920` sans option étire l'image. Une image 941×1672 (9:16 natif)
deviendra légèrement déformée si le ratio ne correspond pas exactement à 1080×1920.

### La solution correcte

```bash
# Option A — scale + pad (préserve le ratio, ajoute des bandes si nécessaire)
-vf "scale=1080:1920:force_original_aspect_ratio=decrease,\
     pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,\
     setsar=1,\
     format=yuv420p"

# Option B — scale avec crop (remplit, coupe les débordements)
-vf "scale=1080:1920:force_original_aspect_ratio=increase,\
     crop=1080:1920,\
     setsar=1,\
     format=yuv420p"
```

### Règle
- Utiliser **Option A** (pad) pour les portraits 9:16 avec fond noir acceptable
- Utiliser **Option B** (crop) uniquement si le contenu important est centré
- **Ne jamais** utiliser `scale=1080:1920` sans option de ratio

---

## 2. Zoompan — Ken Burns sans tremblement

### Le problème
La cause principale du "zoom tremblant" en Phase 14 :
- `zoompan` sans `fps` spécifié : FFmpeg recalcule les frames de manière discontinue
- Expression `z='zoom+0.002'` sans borne : le zoom devient infini et déstabilise
- Pas d'ancrage x,y : la caméra dérive aléatoirement

### La solution correcte

```bash
# Ken Burns — zoom avant lent (intimité, rapprochement)
-vf "fps=25,\
     zoompan=\
       z='if(lte(on,1),1.0,if(lt(zoom,1.08),zoom+0.0008,1.08))'\
       :x='iw/2-(iw/zoom/2)'\
       :y='ih/2-(ih/zoom/2)'\
       :d=125\
       :s=1080x1920\
       :fps=25,\
     format=yuv420p"

# Ken Burns — zoom arrière lent (isolement, révélation)
-vf "fps=25,\
     zoompan=\
       z='if(lte(on,1),1.08,if(gt(zoom,1.0),zoom-0.0008,1.0))'\
       :x='iw/2-(iw/zoom/2)'\
       :y='ih/2-(ih/zoom/2)'\
       :d=125\
       :s=1080x1920\
       :fps=25,\
     format=yuv420p"

# Pan lent gauche→droite
-vf "fps=25,\
     zoompan=\
       z='1.05'\
       :x='if(lte(on,1),0,x+0.5)'\
       :y='ih/2-(ih/zoom/2)'\
       :d=125\
       :s=1080x1920\
       :fps=25,\
     format=yuv420p"
```

### Paramètres critiques
| Paramètre | Valeur recommandée | Raison |
|---|---|---|
| `fps=25` avant zoompan | **Obligatoire** | Évite le jitter causé par un framerate source variable |
| `fps=25` dans zoompan | **Obligatoire** | Synchronise le compteur `on` avec la durée réelle |
| Incrément zoom | `0.0006` à `0.0012` par frame | Au-delà, le mouvement devient visible et brusque |
| Borne supérieure zoom | `1.08` à `1.15` maximum | Au-delà, perte de qualité et effet grossier |
| `d` (duration en frames) | `fps × durée_secondes` | Pour 5s à 25fps : d=125 |
| `x` et `y` | Toujours calculés explicitement | Ancrage central par défaut — ne pas laisser implicite |

---

## 3. Xfade — transitions correctes

### Le problème
Un offset mal calculé produit :
- offset négatif → crash FFmpeg ou transition manquante
- offset trop tardif → plan suivant commence avant la fin de la transition

### La solution correcte

```python
# Calcul des offsets en Python
def calculate_xfade_offsets(durations: list[float], fade_duration: float = 0.5) -> list[float]:
    """
    durations : durée de chaque clip en secondes
    fade_duration : durée du fondu enchaîné
    Retourne : liste des offsets pour chaque xfade
    """
    offsets = []
    cumulative = 0.0
    for i in range(len(durations) - 1):
        cumulative += durations[i]
        offset = cumulative - fade_duration
        assert offset > 0, f"Offset négatif au clip {i}: {offset}. Durée clip trop courte."
        offsets.append(offset)
        cumulative -= fade_duration  # xfade raccourcit la durée effective
    return offsets
```

```bash
# Exemple : 3 clips de 5s chacun, fondu 0.5s
# offset_1 = 5.0 - 0.5 = 4.5
# offset_2 = 4.5 + 5.0 - 0.5 = 9.0

ffmpeg -i clip1.mp4 -i clip2.mp4 -i clip3.mp4 \
  -filter_complex \
    "[0][1]xfade=transition=fade:duration=0.5:offset=4.5[v01];\
     [v01][2]xfade=transition=fade:duration=0.5:offset=9.0[outv]" \
  -map "[outv]" -map "0:a" \
  -c:v libx264 -c:a aac output.mp4
```

### Transitions disponibles et usage YAWatch-LUNA
| Transition | Usage recommandé |
|---|---|
| `fade` | Toutes les transitions standard entre plans |
| `dissolve` | Passage enfance → présent (plus organique que fade) |
| `fadeblack` | Avant les silences dramatiques, fin de teaser |
| `wipeleft` / `wiperight` | Déconseillé — trop actif pour le ton de la série |
| `circleclose` | Interdit — trop cinéma d'animation |

---

## 4. Audio — mixage correct

### Mixage voix + musique + ambiance

```bash
# Voix narrateur (0dB référence) + musique (-18dB) + ambiance (-24dB)
-filter_complex \
  "[1:a]volume=0.15[music];\
   [2:a]volume=0.08[ambiance];\
   [0:a][music][ambiance]amix=inputs=3:duration=longest:dropout_transition=2[outa]"
```

### Niveaux de référence YAWatch-LUNA
| Source | Niveau | Raison |
|---|---|---|
| Voix narrateur | 0 dB (référence) | Clarté maximale, la voix porte la série |
| Musique (motif piano) | -18 dB | Présent mais ne couvre pas la voix |
| Ambiance (bureau, ville) | -24 dB | Texture uniquement |
| Impact SFX (jeton noir) | -6 dB | Frappe émotionnelle contrôlée |
| Silence dramatique | 0 audio sur 0.5-1.0s | Avant le twist — silence total, pas fondu |

### Sync audio-vidéo

```bash
# Éviter -shortest pour les longs contenus (peut tronquer la vidéo)
# Préférer -t pour spécifier la durée exacte

ffmpeg -i video_assembled.mp4 -i narration.mp3 -i music.mp3 \
  -filter_complex \
    "[1:a]atrim=0:28,apad[narr];\
     [2:a]volume=0.15,atrim=0:28[mus];\
     [narr][mus]amix=inputs=2:duration=first[outa]" \
  -map "0:v" -map "[outa]" \
  -c:v copy -c:a aac -b:a 128k \
  -t 28 \
  output_with_audio.mp4
```

---

## 5. Sous-titres — intégration correcte

### Règle absolue
Les sous-titres s'intègrent dans `filter_complex` UNIQUEMENT — jamais avec `-vf`
en parallèle d'un `-filter_complex` déjà présent (conflit FFmpeg).

```bash
# Correct — subtitles dans filter_complex
-filter_complex \
  "[outv]subtitles=/path/to/subs.srt:\
   force_style='FontName=Montserrat Bold,\
   FontSize=72,\
   PrimaryColour=&H00FFFFFF,\
   OutlineColour=&H00000000,\
   Outline=3,\
   Shadow=0,\
   MarginV=180,\
   Alignment=2'[finalv]"
```

### Safe zones YouTube Shorts (1080×1920)
```
Zone à éviter en haut   : 0-100px (interface YouTube)
Zone à éviter en bas    : 1750-1920px (boutons like/sub)
Zone sous-titres idéale : y = 1500-1700px (MarginV=180 depuis le bas)
Zone contenu principal  : 150-1750px
```

### Style obligatoire
| Propriété | Valeur | Raison |
|---|---|---|
| Police | Montserrat Bold ou Inter Bold | Lisibilité mobile |
| Taille | 72px (en points ASS/SRT) | Lisible à 15cm d'écran |
| Couleur | Blanc (#FFFFFF) | Contraste sur tout fond |
| Contour | 3px noir (#000000) | Lisible sur fond clair ET foncé |
| Alignement | Centré bas (2) | Standard Shorts |
| Durée min par ligne | 1.5 secondes | Lecture confortable sur mobile |
| Caractères max par ligne | 35 | Au-delà, débordement sur mobile |

---

## 6. Export final mobile-optimisé

```bash
ffmpeg -i input_assembled.mp4 \
  -c:v libx264 \
  -profile:v baseline \
  -level 3.1 \
  -preset medium \
  -crf 22 \
  -pix_fmt yuv420p \
  -c:a aac \
  -b:a 128k \
  -ar 44100 \
  -ac 2 \
  -movflags +faststart \
  -metadata title="YAWatch-LUNA — Teaser S01E00" \
  output_TEASER_S01E00_FINAL.mp4

# Vérification post-export obligatoire
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate,duration \
  -of default=noprint_wrappers=1 \
  output_TEASER_S01E00_FINAL.mp4
```

### Vérifications attendues
```
codec_name=h264
width=1080
height=1920
r_frame_rate=25/1
duration=28.XX (±0.5s)
```

---

## 7. Commandes de diagnostic courants

```bash
# Inspecter un fichier MP4
ffprobe -v quiet -print_format json -show_streams fichier.mp4

# Vérifier le ratio sans ouvrir
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height \
  -of csv=p=0 fichier.mp4

# Extraire une frame à t=5s pour vérification visuelle
ffmpeg -ss 5 -i fichier.mp4 -frames:v 1 -q:v 2 verification_frame.jpg

# Vérifier la sync audio (waveform)
ffmpeg -i fichier.mp4 -filter_complex \
  "[0:v][0:a]showwavespic=s=1080x200[out]" \
  -map "[out]" -frames:v 1 waveform.png
```
