# VISUAL PIPELINE V1 — YAWatch-LUNA

Pipeline de production visuelle pour Shorts YouTube 9:16.

---

## Format cible

| Paramètre | Valeur |
|---|---|
| Résolution | 1080 × 1920 (9:16) |
| FPS | 30 |
| Durée | 20–60 secondes |
| Format export | MP4 H.264, AAC audio |
| Codec | libx264 + aac |

---

## Structure d'un épisode (scènes)

```
[0s–3s]   SCÈNE 1 — Hook         : gros plan Luna Doll ou phrase choc
[3s–25s]  SCÈNE 2 — Story        : Luna adulte + narration
[25s–35s] SCÈNE 3 — Twist        : ambiance YAWatch froide + révélation
[35s–45s] SCÈNE 4 — CTA          : poupée seule + call to action
```

---

## Génération d'images

### Outil recommandé (sans API payante supplémentaire)

**Option A — Local SDXL** (si GPU disponible)
```bash
# Stable Diffusion XL via ComfyUI ou AUTOMATIC1111
# Modèle recommandé : dreamshaper-xl, juggernautXL
# Sampler : DPM++ 2M Karras
# Steps : 25–30
# CFG : 7
# Seed : fixe par personnage (garantit cohérence)
```

**Option B — Replicate API** (500 runs/mois gratuits)
```python
import replicate
output = replicate.run(
    "stability-ai/sdxl:...",
    input={"prompt": master_prompt, "negative_prompt": neg_prompt,
           "width": 1080, "height": 1920, "num_inference_steps": 30}
)
```

**Option C — DALL-E 3 via OpenAI** (déjà disponible)
```python
client.images.generate(
    model="dall-e-3",
    prompt=master_prompt,
    size="1024x1792",  # ratio 9:16
    quality="standard"
)
```

### Seeds officiels par personnage

Pour garantir la cohérence entre épisodes, utiliser des seeds fixes :

```
Luna Doll (émotionnelle)  : seed = 42
Luna Doll (mystérieuse)   : seed = 1337
Luna adulte (bureau)      : seed = 2048
Luna adulte (portrait)    : seed = 777
YAWatch room              : seed = 9999
```

---

## Mouvement de caméra (parallaxe)

Pour éviter les images statiques, appliquer un **effet Ken Burns** minimal :

```python
# Via MoviePy
clip = ImageClip(img_path).with_duration(8)
# Zoom lent : 100% → 105% sur 8 secondes
clip = clip.resized(lambda t: 1 + 0.005 * t)
```

Types de mouvement par scène :

| Scène | Mouvement |
|---|---|
| Hook — Luna Doll close up | Zoom lent vers l'avant (intimité) |
| Story — Luna adulte | Pan lent de droite à gauche |
| Twist — YAWatch room | Zoom arrière lent (isolation) |
| CTA — poupée seule | Zoom avant très lent (mystère) |

## Animation Premium Image-To-Video

Le Ken Burns reste le fallback.

Pour un rendu teaser/film, produire des clips courts de 3 a 5 secondes via une brique image-to-video :

- camera push-in ;
- micro-expression ;
- respiration ;
- regard ;
- pluie, reflets, lumiere ;
- mouvement tres retenu.

Regles :

- pas de lipsync par defaut ;
- pas de gestes exageres ;
- pas de transformation de visage ;
- ne jamais demander une action complexe ;
- garder le plan court.

Voir :

```text
docs/IMAGE_TO_VIDEO_TEST_MATRIX.md
```

---

## Sous-titres

### Style recommandé

```
Police     : Inter Bold ou Montserrat Bold
Taille     : 72px (lisible sur mobile)
Couleur    : #FFFFFF (blanc)
Contour    : 3px noir (#000000) ou ombre portée
Position   : bas d'écran, marge 10% du bord
Max chars  : 35 caractères par ligne
Max lignes : 2 lignes simultanées
```

### Positionnement safe zones YouTube Shorts

```
Zone titre (haut)    : 0%–15% de la hauteur — éviter
Zone contenu         : 15%–80% — zone principale
Zone sous-titres     : 75%–90% — position idéale
Zone interface YT    : 85%–100% — éviter (boutons like/sub)
```

---

## Ambiance sonore

### Principe

Chaque épisode doit avoir une couche sonore en plus de la voix :

| Type | Caractère | Usage |
|---|---|---|
| Ambient tension | Drone bas, fréquence 60–120Hz | Scènes YAWatch |
| Ambient warm | Piano doux, réverb longue | Scènes enfance/émotion |
| Transition sting | 1–2 secondes, impact | Entre scènes |
| Silence dramatique | 0.5s de silence avant le twist | Avant le reveal |

### Sources gratuites recommandées

- Pixabay (licence libre commerciale)
- Freesound.org (CC0)
- Zapsplat (gratuit avec attribution)

---

## Assembly FFmpeg (fallback sans MoviePy)

```bash
# 1. Créer la vidéo depuis les images (8s par image)
ffmpeg -loop 1 -t 8 -i scene1_hook.png \
       -loop 1 -t 22 -i scene2_story.png \
       -loop 1 -t 10 -i scene3_twist.png \
       -loop 1 -t 8 -i scene4_cta.png \
       -filter_complex "[0][1][2][3]concat=n=4:v=1:a=0" \
       -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
       video_raw.mp4

# 2. Ajouter l'audio
ffmpeg -i video_raw.mp4 -i audio.mp3 \
       -c:v copy -c:a aac -shortest \
       video_with_audio.mp4

# 3. Ajouter les sous-titres
ffmpeg -i video_with_audio.mp4 \
       -vf "subtitles=subs.srt:force_style='FontName=Arial,FontSize=20,Bold=1,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=3'" \
       -c:a copy \
       luna_episode_final.mp4
```

---

## Quality Gate automatisé (à implémenter)

```python
def quality_gate_check(video_path: Path, story: dict) -> dict:
    checks = {
        "format_916": False,        # ratio vérifié
        "duration_ok": False,       # 20–60s
        "has_audio": False,         # piste audio présente
        "has_subtitles": False,     # srt lié
        "luna_doll_consistent": False,  # seed fixe utilisé
        "status": "prototype"
    }
    # ... implémentation
    if all(v for k, v in checks.items() if k != "status"):
        checks["status"] = "production_ready"
    return checks
```
