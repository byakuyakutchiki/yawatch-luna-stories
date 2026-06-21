# Interpretation — Kling Target vs YAWatch Local/Cloud Tests

Date: 2026-06-22

## Source Kling mesurée

```text
C:\Users\saint\Downloads\kling_20260619_VIDEO_Cinematic__4730_0.mp4
```

Specs:

| Champ | Valeur |
|---|---:|
| Résolution | `1956x1060` |
| FPS | `24` |
| Durée | `5.04 s` |
| Frames vidéo | `121` |
| Taille | `4.99 MB` |
| Audio | oui |

## Point méthodologique important

La vidéo Kling est en paysage, très sombre, avec Luna dans un bureau de nuit.

Les clips FramePack/Wan comparés sont en portrait.

Donc:

```text
Les métriques Kling ne doivent pas être comparées brutalement aux métriques portrait.
Elles servent à définir une cible esthétique et technique, pas un gate direct.
```

## Métriques Kling principales

| Critère | Kling |
|---|---:|
| Face SSIM min | `0.729` |
| Face light peak-to-peak | `28.68%` |
| Face flicker | `0.085` |
| Shoulder flow | `0.1590` |
| Hair flow | `0.1602` |
| Hands/frame flow | `0.1635` |
| Full-frame flow | `0.2346` |

## Lecture correcte

### Ce que Kling fait très bien

Kling a un flicker extrêmement faible:

```text
face_flicker = 0.085
```

C'est meilleur que:

- FramePack cloud: environ `0.190`;
- Wan cloud: environ `0.250`.

Kling répartit le mouvement dans tout le plan:

- visage;
- cheveux;
- épaules;
- mains/cadre;
- décor.

Le mouvement n'est pas seulement un visage qui bouge: la scène respire.

### Ce que les chiffres bruts peuvent mal représenter

Le `Face light peak-to-peak = 28.68%` semble mauvais, mais la scène Kling est très sombre.

La luminance moyenne du visage est seulement:

```text
8.73
```

Quand la moyenne est aussi basse, de petites variations absolues deviennent de gros pourcentages.

Conclusion:

```text
Pour des scènes de nuit, le gate doit regarder aussi flicker_mean_abs_delta et pas seulement peak-to-peak %.
```

### Face SSIM min

Kling obtient:

```text
Face SSIM min = 0.729
```

Ce score est inférieur au seuil YAWatch actuel `0.85`, mais il ne signifie pas forcément que le visage dérive.

Raisons possibles:

- Kling anime davantage la tête;
- le visage est sombre;
- la zone visage est petite dans un plan paysage;
- la tête tourne légèrement;
- la lumière directionnelle change avec le mouvement.

Conclusion:

```text
SSIM visage seul punit les vrais mouvements cinématiques.
Il faut ajouter un indicateur de mouvement contrôlé / traduction caméra.
```

## Comparaison opérationnelle

| Signal | FramePack | Wan cloud | Kling target |
|---|---:|---:|---:|
| Identité stable | excellent | correct | à juger visuellement |
| Flicker | bon | bon | excellent |
| Mouvement cheveux/épaules | faible à moyen | fort | naturel / global |
| Mouvement mains/objet | non mesuré ou faible | à surveiller | présent |
| Sensation cinéma | moyenne | meilleure | référence cible |

## Avis Codex pour Claude/DeepSeek

Il ne faut pas essayer de copier Kling avec un seul modèle brut.

La cible réaliste est:

```text
Wan/FramePack pour mouvement de base
→ restauration visage / identité
→ stabilisation luminance / color matching
→ upscale / post-traitement
→ Quality Gate
```

C'est exactement le pipeline 2 étages évoqué:

```text
mouvement + restauration visage = Kling maison
```

## Décision recommandée

Ne pas assouplir le Quality Gate global pour faire passer Wan de force.

Créer plutôt deux profils:

### Profil portrait stable

Utiliser seuils actuels:

| Critère | Seuil |
|---|---:|
| Face SSIM min | `>= 0.85` |
| Face flicker | `<= 0.5` |
| Face light peak-to-peak | `<= 15%` |

### Profil cinéma nuit / mouvement

À créer, inspiré de Kling:

| Critère | Cible |
|---|---:|
| Face flicker | `<= 0.15` |
| Hair flow | `>= 0.14` |
| Shoulder flow | `>= 0.14` |
| Hands/object flow | `>= 0.14` |
| Full-frame flow | `>= 0.20` |
| Face SSIM min | à valider visuellement si mouvement fort |

## Prochaine action de code recommandée

Avant de coder le pipeline 2 étages complet:

1. Ajouter un mode `profile` au Quality Gate:
   - `portrait_stable`;
   - `cinematic_motion_dark`.
2. Ajouter `hands_object` et `full_frame_flow` aux métriques standard.
3. Ajouter un rapport “Kling target delta”:
   - distance du clip généré à la cible Kling;
   - pas seulement PASS/FAIL.

Ensuite seulement:

```text
Coder la chaîne 2 étages mouvement + restauration visage.
```

## Conclusion courte

Kling n'est pas seulement meilleur parce qu'il bouge plus.

Il est meilleur parce que:

```text
le mouvement est distribué,
le flicker est très bas,
la caméra semble vivante,
l'objet dans les mains existe,
l'ambiance reste cohérente.
```

Notre usine doit donc viser:

```text
pas seulement "faire bouger Luna",
mais faire bouger la scène sans perdre l'identité.
```
