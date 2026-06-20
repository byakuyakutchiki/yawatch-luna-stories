# REVUE RÉALISATEUR — 3 clips tests YAWatch-LUNA

> Fiche de visionnage pour Ludovic, directeur artistique.
> Le code a validé le NIVEAU CLIP (technique). Cette revue juge l'ART.
> Date : 2026-06-20

## Clips à visionner
```
~/PROJETS/YAWATCH_LUNA_STORIES/outputs/clips_local_tests/
  plan02_luna_adulte_portrait.mp4   (230 KB)
  plan06_luna_enfant_poupee.mp4     (287 KB)
  plan09_aby_jeton_noir.mp4         (467 KB)
```
Tous : 1080×1920, h264, 25fps, 2 secondes.

---

## ⚠ À SAVOIR AVANT DE JUGER (honnêteté technique)

**Ces 3 clips ont été générés SANS IPAdapter actif.**

Le custom node IPAdapter est installé sur Windows, mais le **modèle**
`ip-adapter_sd15.safetensors` est **absent**. L'IPAdapter n'a donc pas pu tourner.

**Conséquence pour ton jugement :** l'identité des personnages dans ces clips
repose **uniquement sur le denoise faible**, pas encore sur l'IPAdapter.

- Si l'identité te paraît **suffisante** → le denoise seul suffit, tant mieux.
- Si l'identité **dérive** → le correctif (IPAdapter) est **déjà codé**, il suffit
  d'installer le modèle et de régénérer. Ce n'est pas un échec de conception.

Tu juges donc la **baseline denoise-only**, pas la version finale IPAdapter.

---

## CLIP 1 — plan02 · Luna adulte portrait

### 1. Intention du plan
Introduire Luna comme **fausse suspecte**. Présence sérieuse, humaine, protectrice.
Push-in très lent qui crée le mystère sans accuser. C'est le visage qui doit donner
envie de comprendre : *pourquoi connaît-elle des choses qu'elle ne devrait pas ?*

### 2. Règles MotionDirector appliquées (profil `portrait_adult`)
| Paramètre | Valeur | Pourquoi |
|---|---|---|
| denoise | 0.40 | Fidélité au visage, mouvement subtil |
| cfg | 4.5 | Modéré → moins de flicker |
| steps | 16 | Stabilité du visage |
| ipadapter_weight | 0.75 *(configuré, non actif ici)* | Identité forte |
| motion_scale | 0.7 | Push-in lent, jamais brusque |

### 3. Critères artistiques à observer
- [ ] **Stabilité du visage** — pas de morphing entre les frames
- [ ] **Identité** — c'est bien Luna canon (brune, cheveux longs, tenue sombre)
- [ ] **Qualité du mouvement** — push-in lent et crédible, pas un zoom mécanique
- [ ] **Flicker** — pas de scintillement sur la peau / les yeux
- [ ] **Cohérence émotionnelle** — sérieuse, protectrice, pas souriante ni froide
- [ ] **Cohérence YAWatch-LUNA** — présent parisien lumineux, pas de bascule sombre injustifiée

### 4. Verdict
```
[ ] ACCEPTÉ        — utilisable tel quel pour le teaser
[ ] À AJUSTER      — préciser : ______________________________
[ ] À REJETER      — raison : ________________________________
```

---

## CLIP 2 — plan06 · Luna enfant + poupée

### 1. Intention du plan
L'enfance de Luna. La **poupée violette** est le symbole émotionnel central de la série.
Scène de réconfort, douceur. C'est le cœur tendre du teaser — le contraste avec
le thriller. La poupée doit être **artisanale, tissu, jamais robotique**.

### 2. Règles MotionDirector appliquées (profil `portrait_child` — le plus conservateur)
| Paramètre | Valeur | Pourquoi |
|---|---|---|
| denoise | 0.35 | Le plus bas — visages d'enfant fragiles |
| cfg | 4.0 | Bas → traits non durcis |
| steps | 18 | Plus de steps → visage net et stable |
| ipadapter_weight | 0.85 *(configuré, non actif ici)* | Identité maximale |
| motion_scale | 0.6 | Mouvement très doux, réconfort |

### 3. Critères artistiques à observer
- [ ] **Stabilité du visage** — visage d'enfant stable, proportions enfantines préservées
- [ ] **Identité** — enfant cohérente avec Luna enfant canon
- [ ] **Qualité du mouvement** — push-in doux vers la poupée, tendre
- [ ] **Flicker** — pas de scintillement (surtout sur le visage et le tissu)
- [ ] **Cohérence émotionnelle** — réconfort, douceur, pas d'émotion exagérée
- [ ] **Cohérence YAWatch-LUNA** — poupée brune robe violette velours, **texture tissu**,
      **jamais plastique, jamais robotique** (cf. CHARACTER_BIBLE Luna Doll)

### 4. Verdict
```
[ ] ACCEPTÉ        — utilisable tel quel pour le teaser
[ ] À AJUSTER      — préciser : ______________________________
[ ] À REJETER      — raison : ________________________________
```

---

## CLIP 3 — plan09 · Aby enfant + jeton noir

### 1. Intention du plan
**Aby, la manipulatrice cachée.** La main d'enfant qui dépose le **jeton noir** sur
la maquette = l'indice qu'Aby agit dans l'ombre depuis le début. Geste délibéré,
stratégique. Fin sur le noir. C'est l'indice que le public ne comprendra qu'au final.

### 2. Règles MotionDirector appliquées (profil `hand_object`)
| Paramètre | Valeur | Pourquoi |
|---|---|---|
| denoise | 0.45 | Mouvement de main visible |
| cfg | 5.0 | Respect du geste décrit |
| steps | 16 | — |
| ipadapter_weight | 0.50 *(configuré, non actif ici)* | Identité secondaire, geste prioritaire |
| motion_scale | 0.8 | Geste de main délibéré |

### 3. Critères artistiques à observer
- [ ] **Stabilité de la main** — mains = cas difficile : pas de doigts fondus/multipliés
- [ ] **Identité** — enfant blonde cohérente avec Aby enfant canon
- [ ] **Qualité du mouvement** — geste délibéré de dépôt, focus pull, fin sur le noir
- [ ] **Flicker** — pas de scintillement sur la main / le jeton
- [ ] **Cohérence émotionnelle** — calme, stratégique, froid (pas méchante évidente)
- [ ] **Cohérence YAWatch-LUNA** — le jeton noir reste un **indice subtil**, Aby pas
      présentée comme la coupable évidente avant le final

### 4. Verdict
```
[ ] ACCEPTÉ        — utilisable tel quel pour le teaser
[ ] À AJUSTER      — préciser : ______________________________
[ ] À REJETER      — raison : ________________________________
```

---

## SYNTHÈSE (à remplir après visionnage)

| Clip | Verdict | Note dominante |
|---|---|---|
| plan02 Luna adulte | | |
| plan06 Luna enfant + poupée | | |
| plan09 Aby enfant + jeton | | |

**Décision globale :**
- [ ] Les 3 sont sur la bonne voie → on installe IPAdapter + on affine
- [ ] La grammaire de mouvement est bonne, l'identité doit être renforcée (→ IPAdapter)
- [ ] Un ou plusieurs clips à repenser → préciser lesquels et pourquoi

**Rappel gouvernance :** aucun de ces clips ne devient `teaser_candidat` sans passer
le Quality Gate complet (au stade assemblage), et aucun ne devient `teaser_valide`
sans ton approbation explicite via `mark_human_approved("Ludovic")`.
