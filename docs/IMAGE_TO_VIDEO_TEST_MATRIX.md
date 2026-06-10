# Image-To-Video - Matrice De Test

## Objectif

Choisir une brique image-to-video stable pour donner un rendu film aux images fixes.

Le test doit etre court, concret et mesure sur les besoins de YAWatch-LUNA.

## Outils Candidats

Tester un ou deux outils maximum au depart :

- Runway
- Kling
- Luma
- Pika
- Hailuo
- ComfyUI / AnimateDiff local si disponible

Ne pas tout tester en meme temps.

## Plans Tests

### Test 01 - Luna Bureau

Image source :

```text
assets/luna_stories_assets/09_decors_paris_la_defense/pack_01_yawatch_industries/luna_bureau_la_defense_jour_logo_01.png
```

Prompt mouvement :

```text
Cinematic 5-second shot. Slow camera push-in toward Luna's bright office at La Defense. Subtle reflections on glass, realistic daylight, premium corporate thriller mood, no text changes, no distorted logo, no people appearing.
```

Critere :

- logo stable ;
- architecture stable ;
- mouvement premium.

### Test 02 - Photo Retournee

Image a generer ou utiliser quand disponible :

```text
photo familiale retournee sur bureau Luna
```

Prompt mouvement :

```text
Cinematic 4-second close-up. Slow push-in toward a turned family photo frame on an elegant desk. Subtle dust, soft office light, emotional mystery, shallow depth of field, no hand movement unless specified, no text.
```

Critere :

- tension sans surjeu ;
- pas d'objet qui fond ;
- profondeur de champ credible.

### Test 03 - Aby Enfant

Image source :

```text
assets/luna_stories_assets/03_aby/aby_enfant_canon_apk_maquette_ville_01.png
```

Prompt mouvement :

```text
Cinematic 4-second shot. Very subtle eye movement and controlled breathing. The child looks at the miniature city with a calm strategic expression. Tiny warm lights flicker in the miniature houses. No smile, no exaggerated motion, no face distortion.
```

Critere :

- visage stable ;
- pas de cartoon ;
- regard inquietant mais naturel.

### Test 04 - Pere De Luna

Image source :

```text
assets/luna_stories_assets/10_famille_luna/luna_pere_bureau_verre_silence_01.png
```

Prompt mouvement :

```text
Cinematic 5-second close-up. The father sits in a dark office, calm and threatening. Subtle breathing, slight eye movement, slow camera push-in, warm desk lamp, no aggressive gesture, no speaking, realistic film look.
```

Critere :

- menace calme ;
- visage stable ;
- aucun geste caricatural.

### Test 05 - Malik Silence

Image source :

```text
assets/luna_stories_assets/06_personnage_masculin_noir/personnage_masculin_noir_scene_salon_seul_01.png
```

Prompt mouvement :

```text
Cinematic 5-second shot. Malik sits alone in a Paris apartment at night. Subtle breathing, tired eyes, slow camera push-in, soft window light, emotional silence, no dramatic movement, realistic film look.
```

Critere :

- emotion retenue ;
- pas de deformation du visage ;
- ambiance humaine.

## Grille De Score

Noter chaque outil de 1 a 5 :

| Critere | Note |
|---|---:|
| Stabilite visage | /5 |
| Respect image source | /5 |
| Mouvement camera | /5 |
| Ambiance cinema | /5 |
| Peu d'artefacts | /5 |
| Cout / credits | /5 |
| Simplicite workflow | /5 |

Decision :

> Garder l'outil qui atteint au moins 25/35 sur 3 plans differents.

## Regle De Production

Pour le teaser :

- 70 % des plans peuvent etre image-to-video sans lipsync ;
- 20 % peuvent rester Ken Burns propre ;
- 10 % maximum peuvent utiliser avatar/lipsync.

Le rendu doit paraitre filme, pas "demo IA".
