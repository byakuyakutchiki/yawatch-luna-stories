# GRAPHICS ENGINE RULES — YAWatch-LUNA

## Métier correspondant
Directeur artistique · Direction photo · (Cohérence visuelle sur toute la série)

## Sources expertes utilisées
- "The Visual Story" — Bruce Block (composition, couleur, espace)
- "Five C's of Cinematography" — Joseph Mascelli (cadrage, couleur, continuité)
- "Color and Light" — James Gurney (théorie colorimétrique appliquée à l'image)
- Roger Deakins interviews (cohérence lumineuse, *Blade Runner 2049*)
- FFmpeg colorspace/lut3d filter documentation
- CHARACTER_BIBLE.md, VISUAL_DIRECTION.md (documents internes)
- Python Pillow / OpenCV pour analyse automatique de cohérence

## Problème empêché
- Dérive chromatique entre images générées lors de sessions différentes
- Incohérence de blanc-point (une image chaude, la suivante froide)
- Composition incorrecte pour le format 9:16 (safe zones, règle des tiers)
- Personnage reconnaissable dans une session mais pas dans la suivante
- Perte de la grammaire visuelle présent/souvenir

## Code repo qui doit respecter ce document
- `app/visual_consistency_manager.py` (entièrement)
- `app/graphics_validator.py` (à créer)
- Master prompts dans `assets/reference_prompts/`

## Règles bloquantes avant production vidéo
1. Toute nouvelle image générée doit être validée sur 3 critères : ratio, exposition, palette.
2. Les plans du TEASER ne peuvent pas avoir un écart ΔE > 15 en Lab entre eux.
3. La grammaire présent/souvenir (bleu-gris froid vs sépia-brun chaud) est non-négociable.
4. Tout plan avec le personnage Luna ou la poupée passe par `CHARACTER_LIBRARY_CHECKLIST`.

---

## 1. Espaces colorimétriques — bases

### Ce que génèrent les IA (Midjourney, DALL-E, SD)
Les modèles génèrent des images en **sRGB**, 8 bits par canal (RGB 0-255).
Pas de profil ICC garanti. La température de blanc varie selon le prompt.

### Ce que veut YouTube Shorts
YouTube accepte **sRGB** ou **BT.709** (identiques pour la pratique).
Les conversions exotiques (HDR, rec2020) sont inutiles pour du contenu mobile.

### Conséquence pratique
Toutes les images sources et tous les clips doivent être en **sRGB, 8 bits, yuv420p**.
FFmpeg garantit la conversion si on spécifie `-pix_fmt yuv420p`.

---

## 2. Grammaire visuelle YAWatch-LUNA (non-négociable)

### Présent (Luna adulte, bureau, Paris)
```
Température de couleur : 5000-5500 K (blanc neutre légèrement frais)
Dominante couleur      : Bleu-gris (#3A4A5E, #2C3E50)
Lumière                : Dure, directionnelle, ombres marquées
Saturation             : Modérée (80-90%)
Contraste              : Élevé
Profondeur de champ    : Peu profonde (sujet net, arrière-plan flou)
Grain film             : Présent (léger)
```

### Souvenir (Luna enfant, appartement familial, chaleur)
```
Température de couleur : 3200-4000 K (chaud, ambré)
Dominante couleur      : Brun-doré (#8B6914, #C4892A)
Lumière                : Douce, diffuse, halos, légère surexposition
Saturation             : Élevée (100-110%)
Contraste              : Modéré (voilé, comme une vieille photo)
Profondeur de champ    : Plus profonde (nostalgie = tout net)
Grain film             : Plus marqué (âge du souvenir)
```

### Aby (plans de surveillance, bureau Aby)
```
Température de couleur : 6500 K (très froid, fluorescent)
Dominante couleur      : Blanc-bleu acier (#C8D8E8, #A0B4C8)
Lumière                : Lumière artificielle plate, pas de chaleur
Saturation             : Basse (70-80%)
Contraste              : Très élevé (dur, sans ambiguïté)
```

---

## 3. Cohérence chromatique entre plans — mesure ΔE

### Le problème de dérive
Deux sessions de génération Midjourney/DALL-E produisent des images
avec des températures de blanc différentes même avec le même prompt.
Plan 2 peut avoir un Luna avec un teint légèrement orangé,
Plan 3 avec le même Luna avec un teint légèrement bleuté.
Sur un téléphone mobile, cela se voit immédiatement.

### Mesure automatique (Python OpenCV + scikit-image)
```python
import cv2
import numpy as np
from skimage.color import rgb2lab, deltaE_cie76

def check_chromatic_coherence(image_paths: list[str], threshold_delta_e: float = 15.0) -> dict:
    """
    Vérifie que toutes les images ont une cohérence colorimétrique acceptable.
    Returns : dict avec les paires problématiques et leur ΔE
    """
    lab_averages = []
    for path in image_paths:
        img = cv2.imread(path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        lab = rgb2lab(img_rgb)
        # Moyenne Lab sur la zone centrale (évite les bords noirs)
        h, w = lab.shape[:2]
        center_lab = lab[h//4:3*h//4, w//4:3*w//4]
        lab_averages.append(center_lab.mean(axis=(0, 1)))

    problems = {}
    for i in range(len(lab_averages)):
        for j in range(i + 1, len(lab_averages)):
            delta_e = deltaE_cie76(lab_averages[i], lab_averages[j])
            if delta_e > threshold_delta_e:
                key = f"{image_paths[i]} vs {image_paths[j]}"
                problems[key] = round(delta_e, 2)
    return problems

# Usage
teaser_images = [
    "assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png",
    "assets/luna_stories_assets/01_luna_adulte/luna_adulte_office_desk_01.png",
    # ...
]
problems = check_chromatic_coherence(teaser_images, threshold_delta_e=15.0)
if problems:
    print("ALERTE COHÉRENCE CHROMATIQUE :")
    for pair, delta in problems.items():
        print(f"  ΔE = {delta:.1f} — {pair}")
```

### Seuils ΔE
| ΔE | Interprétation | Action |
|---|---|---|
| 0-5 | Imperceptible | OK |
| 5-10 | Visible à l'expert | Acceptable pour plans différents |
| 10-15 | Visible sur mobile | Traiter en post (LUT ou color correction) |
| 15-25 | Visible clairement | Régénérer l'image |
| > 25 | Incohérence flagrante | BLOQUANT — ne pas assembler |

---

## 4. Correction colorimétrique FFmpeg post-génération

### Cas 1 — Réchauffer légèrement (plan trop froid)
```bash
ffmpeg -i input.mp4 \
  -vf "colorchannelmixer=rr=1.05:gg=1.0:bb=0.92" \
  output_warmed.mp4
```

### Cas 2 — Refroidir légèrement (plan trop chaud)
```bash
ffmpeg -i input.mp4 \
  -vf "colorchannelmixer=rr=0.95:gg=1.0:bb=1.06" \
  output_cooled.mp4
```

### Cas 3 — Réduction de saturation (Aby, plans durs)
```bash
ffmpeg -i input.mp4 \
  -vf "eq=saturation=0.75:contrast=1.1" \
  output_aby.mp4
```

### Cas 4 — Voile nostalgique (plans souvenir)
```bash
ffmpeg -i input.mp4 \
  -vf "eq=brightness=0.05:saturation=1.1:gamma_r=1.08:gamma_b=0.92,\
       colorchannelmixer=rr=1.08:gg=1.02:bb=0.88" \
  output_memory.mp4
```

### Cas 5 — Application d'un LUT (future LUT YAWatch)
```bash
# Quand la LUT officielle YAWatch sera créée :
ffmpeg -i input.mp4 \
  -vf "lut3d=file=luts/yawatch_luna_present.cube" \
  output_graded.mp4
```

---

## 5. Composition — Règles pour le format 9:16

### Règle des tiers en 9:16
```
Lignes horizontales des tiers :
  Tiers supérieur : y = 640 (sur 1920)
  Tiers inférieur : y = 1280

Colonnes des tiers (9:16) :
  Tiers gauche  : x = 360 (sur 1080)
  Tiers droit   : x = 720

Points d'intérêt forts (intersections) :
  (360, 640), (720, 640), (360, 1280), (720, 1280)
```

### Positionnement des personnages par intention

| Intention | Position du visage | Espace | Exemple |
|---|---|---|---|
| Luna présente, confidente | Tiers supérieur centré | Espace vide en bas | Plans neutres présent |
| Luna vulnérable, enfant | Tiers inférieur gauche | Espace vide en haut (ciel, plafond) | Plans souvenir |
| Aby menaçante | Tiers supérieur droit | Hors centre, dominante | Plans observation |
| Révélation d'objet | Centre bas, objet en focus | Personnage flou arrière | Jeton, poupée |
| Plan environnement | Pas de personnage centré | Décor remplit l'espace | Tour, bureau vide |

### Safe zones YouTube Shorts
```
Zone d'interface YouTube (à éviter pour le sujet principal) :
  Haut    : 0 → 120px (titre/nom de compte)
  Bas     : 1750 → 1920px (boutons like/sub/share)
  Droite  : 900 → 1080px (boutons verticaux)

Zone de contenu sûre :
  x : 0 → 880px (80% de la largeur)
  y : 120 → 1750px (85% de la hauteur)
```

---

## 6. Profondeur de champ — règles par type de plan

### Luna adulte (présent)
- **Plans proches** (buste) : arrière-plan très flou (bokeh f/1.8 simulé)
- **Plans moyens** (mi-corps) : arrière-plan légèrement flou (bokeh f/2.8)
- **Plans larges** (pleine pièce) : tout net pour montrer l'environnement

### Luna enfant (souvenir)
- **Règle nostalgie** : profondeur de champ plus profonde que pour le présent
- L'enfant ET l'environnement sont nets → la mémoire fixe tout dans le détail

### Aby
- **Règle de distance** : Aby est toujours légèrement plus nette que ce qu'elle observe
- Le regard d'Aby est toujours net ; sa cible peut être floue

### Poupée Luna
- **Plans gros** : extrême profondeur de champ sélective (yeux nets, robe floue)
- **Plans contextuels** : la poupée au premier plan floue, Luna nette derrière

---

## 7. Cohérence personnage — checklist visuelle

À vérifier sur chaque nouvelle image avant intégration dans le catalogue :

### Luna adulte
```
□ Cheveux : brun foncé (pas auburn, pas noir, pas roux)
□ Teint   : méditerranéen (olivâtre, ni trop clair ni trop foncé)
□ Vêtements présent : foncés, professionnels (noir, gris anthracite, marine)
□ Expression : réservée, légère mélancolie (jamais sourire commercial)
□ Âge visible : ~32 ans (jamais adolescente, jamais plus de 40 ans)
```

### Luna enfant
```
□ Cheveux : brun identique à l'adulte (cohérence temporelle)
□ Âge visible : 7-9 ans
□ Vêtements souvenir : tons chauds (beige, brun, crème — jamais vif)
□ Expression : inquiète OU rassurée (jamais neutre)
```

### Poupée Luna
```
□ Matière : tissu/chiffon artisanal (JAMAIS plastique, JAMAIS métal)
□ Cheveux : brun cousu/brodé
□ Robe    : velours violet (#7B4FA6 ±10%)
□ Taille  : petite (tient dans une main d'enfant)
□ Yeux    : brodés ou en boutons (JAMAIS électroniques, JAMAIS LED)
□ État    : légèrement usée, aimée, non neuve
```

### Aby adulte
```
□ Cheveux : blond (clair, discipliné, ramené en arrière ou lisse)
□ Expression : froide, calculée (JAMAIS chaleureuse, JAMAIS souriante)
□ Vêtements : tailleur, stricte, tons froids (gris, beige corporate)
□ Regard   : toujours décalé (jamais dans l'axe caméra avant S1 finale)
```

---

## 8. Grain film — spécification

Le grain film est une signature visuelle de YAWatch-LUNA. Il doit être présent
mais discret — il renforce l'authenticité sans nuire à la lisibilité mobile.

### Ajout via FFmpeg
```bash
# Grain léger (présent — plans bureau Luna)
ffmpeg -i input.mp4 \
  -vf "noise=alls=8:allf=t+u" \
  output_grain.mp4

# Grain marqué (souvenir — plans enfance)
ffmpeg -i input.mp4 \
  -vf "noise=alls=15:allf=t+u" \
  output_grain_memory.mp4
```

### Paramètre `noise`
| Valeur `alls` | Effet | Usage |
|---|---|---|
| 4-8 | Grain très fin, quasi imperceptible | Plans bureau présent |
| 10-15 | Grain visible, cinématique | Plans souvenir, transitions |
| > 20 | Grain excessif | Interdit — détériore la lisibilité |
