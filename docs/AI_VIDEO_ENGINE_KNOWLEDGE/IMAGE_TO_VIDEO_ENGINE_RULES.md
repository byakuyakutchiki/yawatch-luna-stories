# IMAGE-TO-VIDEO ENGINE RULES — YAWatch-LUNA

## Métier correspondant
Directeur IA Vidéo · Ingénieur pipeline · (Décision architecturale fondamentale)

## Sources expertes utilisées
- Kling AI Documentation : https://klingai.com
- Runway Gen-3 Alpha : https://runwayml.com
- Luma Dream Machine : https://lumalabs.ai
- Post-mortem Phase 14 YAWatch-LUNA (zoom tremblant)
- FFmpeg documentation (pour définir ce que FFmpeg NE peut PAS faire)

## Problème empêché
**LA** cause racine du désastre Phase 14 : FFmpeg présenté comme outil de génération
de mouvement. Ce document établit la séparation stricte et irrévocable entre les outils.

## Code repo qui doit respecter ce document
- `app/video_builder.py` (TOUT le fichier doit respecter la Règle 0)
- `app/scene_composer.py`
- Tout futur agent ou script qui génère des clips

## Règles bloquantes avant production vidéo
1. **Règle 0 — Séparation absolue** : FFmpeg assemble. Kling/SVD/CogVideoX génèrent.
2. Le Ken Burns FFmpeg ne peut pas dépasser 20% des plans d'un épisode.
3. Tout plan nécessitant un mouvement dans l'image (pluie, souffle, reflet) = outil IA obligatoire.
4. Un assemblage FFmpeg d'images fixes n'est jamais appelé "clip animé" ni "plan".

---

## RÈGLE 0 — La séparation fondamentale (INVIOLABLE)

```
┌─────────────────────────────────────────────────────────────────────┐
│  FFmpeg est un outil d'ASSEMBLAGE.                                  │
│  Il concatène des clips existants.                                  │
│  Il mixe du son sur une vidéo existante.                            │
│  Il ajoute des sous-titres à une vidéo existante.                   │
│  Il redimensionne une vidéo existante.                              │
│                                                                     │
│  FFmpeg NE GÉNÈRE PAS de mouvement.                                 │
│  FFmpeg NE PEUT PAS faire bouger un rideau, tomber de la pluie,     │
│  faire respirer un personnage, ni simuler un appareil photo.        │
│                                                                     │
│  zoompan = recadrage progressif d'une image FIXE.                   │
│  Ce n'est PAS une caméra. Ce n'est PAS de l'animation.             │
│  C'est une illusion de faible qualité acceptable dans 20% des cas. │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Arbre de décision par type de plan

Pour chaque plan du TEASER_S01E00_PRODUCTION_PACK, utiliser cet arbre :

```
Le plan nécessite-t-il un mouvement DANS l'image ?
(pluie, souffle, yeux qui clignotent, reflet, flamme, fumée...)
    OUI → OUTIL IA OBLIGATOIRE (Kling / SVD / CogVideoX)
    NON ↓

Le plan nécessite-t-il un mouvement de CAMÉRA réaliste ?
(travelling, zoom cinématique, profondeur de champ changeante...)
    OUI → OUTIL IA OBLIGATOIRE (Kling / SVD / CogVideoX)
    NON ↓

Le plan est un portrait statique avec RECADRAGE PROGRESSIF acceptable ?
(effet de rapprochement doux, plan contemplatif sans mouvement)
    OUI → Ken Burns FFmpeg acceptable (FALLBACK — 20% max)
    NON ↓

Le plan doit rester complètement fixe ?
    OUI → Image fixe + FFmpeg pour durée (pas de zoompan)
```

---

## Tableau de décision par plan — Teaser S01E00

| Plan | Asset | Mouvement requis | Outil requis | Ken Burns OK ? |
|---|---|---|---|---|
| 1 | Tour YAWatch La Défense | Pan vertical, logo révélé | **Kling** | Non |
| 2 | Luna adulte portrait | Push-in imperceptible | **Kling** | En dernier recours |
| 3 | Luna au bureau | Micro-mouvement (respiration) | **Kling** | Non |
| 4 | Luna + photo retournée | Main qui bouge / tension | **Kling** | Non |
| 5 | Luna enfant nuit | Ombre qui passe / peur | **Kling** | Non |
| 6 | Luna enfant + poupée | Scène de réconfort / douceur | **Kling** | Non |
| 7 | Gros plan yeux poupée | Léger zoom sur yeux mystérieux | **Kling** ou Ken Burns | Oui (acceptable) |
| 8 | Aby observe Luna | Pan de Luna vers Aby / révélation | **Kling** | Non |
| 9 | Aby + jeton noir | Main qui dépose le jeton | **Kling** | Non |

**Conclusion teaser** : 8/9 plans nécessitent un outil IA. Plan 7 seul acceptable en Ken Burns.

---

## Prompts de mouvement par plan (Kling / CogVideoX)

Ces prompts doivent être utilisés verbatim ou adaptés depuis :

```python
TEASER_PROMPTS_MOUVEMENT = {
    "plan_01_tour_defense": (
        "Cinematic vertical shot. Slow tilt-up camera movement revealing "
        "the YAWatch tower facade from bottom to top. "
        "Cold blue morning light, overcast sky, glass reflections, film grain. "
        "4K vertical 9:16. Ultra realistic."
    ),
    "plan_02_luna_portrait": (
        "Cinematic portrait. Imperceptible slow push-in camera movement, "
        "1mm per second forward drift. Luna 32yo woman, brown hair, "
        "dark professional attire, neutral expression, slight breathing. "
        "Blue-grey rim lighting, bokeh background, film grain."
    ),
    "plan_03_luna_bureau": (
        "Luna at her office desk, late evening Paris skyline behind her. "
        "Very slow push-in camera. Fluorescent light flicker barely perceptible. "
        "Her eyes scan the screen, micro-expressions of tension."
    ),
    "plan_04_photo_retournee": (
        "Luna's hand reaches toward a face-down photograph on her desk. "
        "Slow zoom-in on the hand, hesitation movement, fingers stop 2cm before touching. "
        "Ultra slow motion feeling, cinematic depth of field."
    ),
    "plan_05_luna_enfant_nuit": (
        "Young girl 8 years old in dark bedroom, moonlight through window. "
        "Shadow passes across the wall behind her. "
        "Her eyes widen slightly, micro-fear expression. "
        "Slow push-in on face, shallow depth of field."
    ),
    "plan_06_luna_poupee_reconfort": (
        "Young girl hugs a small fabric doll with brown hair and violet dress. "
        "Gentle sway movement, comforting. Warm orange bedside lamp. "
        "Slow pull-back, dreamy atmosphere, bokeh."
    ),
    "plan_07_yeux_poupee": (
        "Extreme close-up of fabric doll's embroidered eyes. "
        "Very slow push-in, rack focus from doll's dress to its eyes. "
        "Mysterious, slightly unsettling. Shallow depth of field."
    ),
    "plan_08_aby_observe": (
        "Woman in her 30s, blonde hair pulled back, cold expression, "
        "observing someone off-frame. "
        "Slow rack focus from blurry subject in foreground to her sharp face. "
        "Cool blue office lighting, glass reflections."
    ),
    "plan_09_jeton_noir": (
        "Young girl's hand gently places a small black token on a surface. "
        "Overhead shot, slow tilt-down. "
        "The token catches the light as it settles. "
        "Dark, deliberate, ritualistic movement."
    )
}
```

---

## Spécifications techniques Kling

### Paramètres recommandés par type de plan
| Paramètre | Valeur teaser | Raison |
|---|---|---|
| Mode | Standard ou Pro | Standard suffisant pour le test, Pro pour la finale |
| Durée | 5 secondes | Standard Kling, correspond aux durées du PRODUCTION_PACK |
| Aspect ratio | 9:16 | **Obligatoire** — ne pas générer en 16:9 |
| Résolution | 1080×1920 | Standard Kling |
| Camera control | Prompt-guided | Décrire le mouvement dans le prompt |

### Workflow Kling pour le teaser
```
1. Uploader l'image source (PNG 9:16)
2. Coller le prompt de mouvement (depuis TEASER_PROMPTS_MOUVEMENT)
3. Sélectionner : Mode Standard, 5s, 9:16
4. Générer (2-4 minutes d'attente)
5. Prévisualiser dans l'interface Kling AVANT de télécharger
6. Si insatisfaisant : régénérer avec prompt modifié (ajouter "more subtle" ou "more dramatic")
7. Télécharger le clip validé
8. Nommer : TEASER_PLAN_01_TOUR_v1.mp4, TEASER_PLAN_02_LUNA_v1.mp4, etc.
```

### Critères de rejet d'un clip Kling
Régénérer immédiatement si :
- Le visage de Luna change par rapport à l'image source
- La couleur des vêtements n'est pas identique
- Le mouvement est trop rapide ou saccadé
- La poupée apparaît en métal, LED, ou robotique (voir CHARACTER_BIBLE)
- Artefacts visuels (distorsion, corruption de pixels)
- La scène dérive vers une autre ambiance que le prompt

---

## Ce que Kling ne fait PAS (et comment contourner)

| Limite Kling | Contournement |
|---|---|
| Ne maintient pas la cohérence visage entre 2 clips | Utiliser la même image source + même prompt, régénérer si dérive |
| Ne garantit pas le mouvement exact décrit | Reformuler le prompt (plus précis / plus court) ou régénérer |
| Limité à 5-10 secondes par clip | Découper les plans longs en deux clips + raccord au montage |
| Ne génère pas de sons | Tout son = étape audio séparée (ElevenLabs + SFX) |
| Peut déformer les détails texte (logo YAWatch) | Recropper le clip ou ajouter le logo en post (FFmpeg overlay) |

---

## Le cas Ken Burns — quand et comment

### Quand utiliser Ken Burns
- Plan contemplatif sans mouvement dans l'image (objets inanimés, décors)
- Plan à durée très courte (< 2s) où Kling serait du gaspillage de crédits
- Test rapide pour valider la structure du montage avant génération finale
- Maximum **20% des plans** d'un épisode

### Ken Burns acceptable vs inacceptable
```
ACCEPTABLE : plan 7 (gros plan yeux poupée, zoom lent et mystérieux)
             → Pas de vie dans l'image attendue, zoom renforce le mystère

NON ACCEPTABLE : plan 2 (portrait Luna adulte, respiration attendue)
                 → Le spectateur voit qu'elle ne respire pas = rupture immersion

NON ACCEPTABLE : tout plan où un personnage vivant est présent
NON ACCEPTABLE : tout plan où un mouvement diégétique est impliqué par le script
```

### Paramètres Ken Burns corrects (voir FFMPEG_PROFESSIONAL_VIDEO_PIPELINE.md)
- Incrément zoom : 0.0006 à 0.0008 par frame (très subtil)
- fps=25 obligatoire avant ET dans zoompan
- Borne zoom max : 1.08 (jamais plus)
- x,y ancrés explicitement

---

## Historique — Post-mortem Phase 14

**Ce qui s'est passé :**
Le pipeline Phase 14 a utilisé `video_builder.py` avec `zoompan` FFmpeg sur les images
de `content/images/episode_test/` (images placeholder, pas les assets canon).
Le résultat a été présenté comme un "teaser" alors que :
- C'étaient des images test (scene_hook.jpg, scene_story.jpg)
- FFmpeg ne peut pas animer des personnages
- Le zoom était paramétré sans `fps=25` → tremblement
- Le STATUS dans le manifest était "prototype" mais le fichier MP4 a été utilisé

**Ce qui ne doit plus se passer :**
- `video_builder.py` ne peut plus déclarer un fichier "production_ready" automatiquement
- Aucun clip ne peut utiliser les images de `content/images/episode_test/`
- Toute exécution de `video_builder.py` sur les assets teaser doit déclencher une alerte :
  "Ce pipeline génère un PROTOTYPE. Pour le teaser, utiliser Kling."
