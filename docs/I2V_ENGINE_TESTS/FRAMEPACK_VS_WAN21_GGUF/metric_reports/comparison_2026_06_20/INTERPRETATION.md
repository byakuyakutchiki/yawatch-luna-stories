# Interpretation — Wan GGUF vs FramePack Objective Metrics

Date: 2026-06-20

## Verdict chiffres

FramePack est objectivement meilleur sur les deux problemes les plus critiques detectes par Ludovic:

- stabilite lumiere / teint;
- stabilite identite proxy sur la zone visage.

Wan GGUF montre plus de mouvement optique, mais ce mouvement accompagne aussi de fortes variations de lumiere et une instabilite plus importante de la zone visage.

## Donnees clefs

| Critere | Wan motion | Wan lighting stable | FramePack |
|---|---:|---:|---:|
| Face SSIM min | `0.522` | `0.500` | `0.925` |
| Face light peak-to-peak | `27.42%` | `28.37%` | `10.69%` |
| Face flicker | `1.307` | `1.297` | `0.162` |
| Shoulder flow | `0.5636` | `0.5517` | `0.0720` |
| Hair flow | `0.5299` | `0.5280` | `0.0724` |

## Lecture production

### Ce que FramePack gagne

FramePack reduit massivement la variation lumineuse:

- visage Wan: environ `27-28%` de variation peak-to-peak;
- visage FramePack: `10.69%`.

FramePack reduit aussi le flicker visage:

- Wan: environ `1.30`;
- FramePack: `0.162`.

La stabilite identite proxy est nettement meilleure:

- Wan tombe autour de `0.50-0.52` au minimum;
- FramePack reste a `0.925`.

Conclusion technique provisoire:

```text
FramePack est meilleur candidat que Wan pour la stabilite image.
```

### Ce que FramePack ne gagne pas encore

Le mouvement optique est faible:

- epaules: `0.0720`;
- cheveux: `0.0724`.

Le script classe donc:

```text
shoulder_motion = LOW_MOTION
hair_motion = LOW_MOTION
```

Conclusion artistique provisoire:

```text
FramePack stabilise mieux, mais reste trop timide sur mouvement organique.
```

## Decision recommandee

Ne pas multiplier les prompts Wan pour regler la lumiere.

Prochaine experience utile:

```text
FramePack test 002
Objectif: garder la stabilite lumineuse FramePack, augmenter legerement le mouvement organique.
```

Parametres a explorer:

- `steps`: conserver `20` ou tester `25`;
- `guidance_scale`: tester `8.0` ou conserver `10.0`;
- `latent_window_size`: tester impact sur duree et mouvement;
- prompt: plus grave, moins souriant, plus directif sur micro-respiration cou/epaules.

Point bloquant a corriger:

```text
La duree FramePack n'est pas maitrisee: demande 5.0 s, sortie 9.06 s.
```

Avant production teaser, il faut comprendre ce comportement.

## Regle pour l'usine YAWatch-LUNA

Un moteur ne doit pas etre choisi uniquement parce qu'il "semble plus beau".

Il doit passer trois niveaux:

1. metrics objectives;
2. contact sheet;
3. validation humaine Ludovic sur MP4 reel.

Etat actuel:

```text
FramePack passe niveau 1 sur lumiere / identite.
FramePack reste a valider niveau 3 sur mouvement et emotion.
```
