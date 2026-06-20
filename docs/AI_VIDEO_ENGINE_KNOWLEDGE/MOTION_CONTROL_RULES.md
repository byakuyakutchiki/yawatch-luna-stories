# MOTION CONTROL RULES — YAWatch-LUNA

> Bibliothèque de connaissances : contrôle du mouvement IA (image-to-video).
> Source de vérité pour le rôle **MotionDirector** qui prépare les VideoJob.
> Les valeurs ci-dessous sont reflétées en machine dans
> `app/motion_director/motion_profiles.json` (un test garantit la cohérence).

## Métier correspondant
Directeur du mouvement (MotionDirector) · Ingénieur image-to-video

## Sources expertes utilisées
- ComfyUI AnimateDiff-Evolved — documentation officielle et paramètres de contexte
- IPAdapter_plus (cubiq) — préservation d'identité de personnage
- Stable Diffusion img2img — relation denoise / fidélité à l'image source
- Post-mortem Phase 14 + 1er clip local plan02 (denoise 0.45 sans IPAdapter)

## Problème empêché
Générer des clips "au hasard" : visages qui dérivent, flicker, déformations,
mouvement violent, perte d'identité de Luna entre deux plans. Ce document
remplace le réglage manuel par des profils documentés et justifiés.

## Code repo qui doit respecter ce document
- `app/motion_director/director.py` (lit ce doc + les profils)
- `app/motion_director/motion_profiles.json` (reflet machine de ce doc)
- `app/i2v_engine/comfyui_backend.py` (exécute le job, IPAdapter inclus)

---

## RÈGLE 0 — La hiérarchie des leviers

Le mouvement IA se contrôle par 4 leviers, dans cet ordre d'importance :

```
1. IDENTITÉ    → IPAdapter (image de référence du personnage) + denoise faible
2. STABILITÉ   → steps suffisants + CFG modéré + seed fixe
3. MOUVEMENT   → motion_scale + denoise (plus haut = plus de mouvement, plus de risque)
4. CADRAGE     → résolution + ratio source
```

**Loi fondamentale denoise :**
- denoise **bas** (0.30–0.45) = fidèle à l'image source, identité préservée, mouvement subtil
- denoise **haut** (0.55+) = plus de mouvement mais le visage dérive et se déforme

> Pour un personnage récurrent (Luna, Aby), on privilégie TOUJOURS l'identité
> sur l'ampleur du mouvement. Un beau mouvement avec un mauvais visage = clip rejeté.

---

## Profils de mouvement par type de plan

Chaque plan du teaser appartient à un **type**. Le MotionDirector choisit le profil
selon le type, puis applique le mouvement spécifique du plan.

### Type `establishing` — décor / architecture (ex : plan 1 tour YAWatch)
Pas de visage humain. On peut se permettre plus de mouvement de caméra.

| Paramètre | Valeur | Raison |
|---|---|---|
| denoise | 0.50 | Pas d'identité à préserver, mouvement de caméra ample acceptable |
| cfg | 5.5 | Respect du prompt de caméra |
| steps | 14 | Décor tolère moins de steps |
| num_frames | 16 | Fenêtre AnimateDiff standard |
| fps | 8 | — |
| ipadapter_weight | 0.0 | Aucun personnage → IPAdapter désactivé |
| motion_scale | 0.9 | Travelling / pan ample |

### Type `portrait_adult` — visage adulte (ex : plan 2 Luna, plan 3 bureau, plan 8 Aby)
**Identité critique.** Le visage doit rester exactement celui du personnage canon.

| Paramètre | Valeur | Raison |
|---|---|---|
| denoise | 0.40 | Fidélité au visage source, mouvement subtil |
| cfg | 4.5 | CFG modéré = moins de flicker |
| steps | 16 | Stabilité du visage |
| num_frames | 16 | — |
| fps | 8 | — |
| ipadapter_weight | 0.75 | Forte préservation d'identité |
| motion_scale | 0.7 | Push-in lent, respiration — jamais brusque |

### Type `portrait_child` — visage enfant (ex : plan 5 Luna enfant, plan 6 enfant+poupée)
**Le plus fragile.** Les visages d'enfant se déforment plus facilement (proportions,
yeux). Réglages les plus conservateurs.

| Paramètre | Valeur | Raison |
|---|---|---|
| denoise | 0.35 | Le plus bas — préserve les proportions enfantines |
| cfg | 4.0 | Bas = visage stable, pas de durcissement des traits |
| steps | 18 | Plus de steps = visage plus net et stable |
| num_frames | 16 | — |
| fps | 8 | — |
| ipadapter_weight | 0.85 | Identité maximale |
| motion_scale | 0.6 | Mouvement très doux, scène de réconfort |

### Type `hand_object` — main + objet (ex : plan 4 photo, plan 9 jeton noir)
Les mains sont un cas difficile pour l'IA. On accepte un peu plus de mouvement
mais on réduit l'IPAdapter (l'identité du visage compte moins ici).

| Paramètre | Valeur | Raison |
|---|---|---|
| denoise | 0.45 | Mouvement de main visible |
| cfg | 5.0 | Respect du geste décrit |
| steps | 16 | — |
| num_frames | 16 | — |
| fps | 8 | — |
| ipadapter_weight | 0.5 | Identité secondaire, geste prioritaire |
| motion_scale | 0.8 | Geste de main délibéré |

### Type `macro_object` — gros plan objet (ex : plan 7 yeux de la poupée)
Pas de visage humain. Mouvement très lent et contemplatif.

| Paramètre | Valeur | Raison |
|---|---|---|
| denoise | 0.40 | Préserve la texture de la poupée |
| cfg | 4.5 | — |
| steps | 14 | — |
| num_frames | 16 | — |
| fps | 8 | — |
| ipadapter_weight | 0.3 | Cohérence de l'objet sans forcer |
| motion_scale | 0.5 | Macro très lente vers les yeux |

---

## Règles anti-flicker (scintillement)

Le flicker AnimateDiff vient de l'incohérence entre frames. Réduction :

1. **Seed fixe** sur toute la génération d'un clip (jamais aléatoire en production).
2. **CFG modéré** (≤ 5.5) — un CFG élevé amplifie le flicker.
3. **Steps suffisants** (≥ 14, idéalement 16-18 pour les visages).
4. **motion_scale contenu** (≤ 0.9) — un mouvement excessif crée de l'incohérence.
5. **Motion module v2/v3** (mm_sd_v15_v2) — plus stable que v1.
6. Pour > 16 frames : **context_options** (fenêtre glissante, overlap 4) — sinon
   rupture de cohérence. Le teaser reste à 16 frames donc non requis pour l'instant.
7. *(Post-production optionnelle)* interpolation RIFE pour lisser — hors scope V1.

---

## Règles anti-déformation

1. **Résolution minimale visage** : le visage doit faire ≥ 1/3 de la hauteur du cadre.
   En dessous, trop peu de pixels → déformation. Générer ≥ 512px de large.
2. **denoise plafonné** selon le type (voir profils). Ne jamais dépasser 0.50 sur un visage.
3. **Negative prompt déformation** (obligatoire, injecté par le MotionDirector) :
   `deformed face, distorted face, asymmetric eyes, extra fingers, fused fingers,
   melting, warping, mutated, disfigured, bad anatomy`.
4. **steps** suffisants — un visage sous 14 steps durcit et se déforme.

---

## Règles de préservation d'identité

1. **IPAdapter obligatoire** dès qu'un personnage récurrent est présent
   (Luna adulte, Luna enfant, Aby, Père, Malik). Image de référence = l'asset canon.
2. **ipadapter_weight** selon le type (0.75 adulte, 0.85 enfant — voir profils).
3. **denoise bas** en complément (l'IPAdapter seul ne suffit pas si denoise trop haut).
4. **Negative identité** : `different person, identity change, face swap, wrong face`.
5. **L'image de référence IPAdapter = l'image source du plan**, jamais une autre —
   sinon on mélange deux identités.

---

## Règles spécifiques par sujet

| Sujet | Règle clé |
|---|---|
| **Portrait adulte** | Respiration + push-in lent uniquement. Jamais de sourire ajouté, jamais de clignement forcé. |
| **Enfant** | Réglages les plus conservateurs. Mouvement minimal. Émotion retenue, jamais exagérée. |
| **Main** | Geste unique et délibéré (déposer, tourner). Pas de doigts qui bougent sans raison. |
| **Objet / poupée** | Texture tissu préservée. Jamais d'aspect plastique ou robotique (cf. CHARACTER_BIBLE Luna Doll). |
| **Décor** | Mouvement de caméra ample autorisé. Logo et architecture doivent rester stables. |

---

## Bibliothèques que le MotionDirector DOIT consulter avant de préparer un job

1. `docs/CHARACTER_BIBLE.md` — identité visuelle exacte du personnage du plan
2. `docs/VISUAL_DIRECTION.md` — grammaire présent/souvenir, palette autorisée
3. `docs/TEASER_S01E00_PRODUCTION_PACK.md` — image source et mouvement par plan
4. `docs/AI_VIDEO_ENGINE_KNOWLEDGE/IMAGE_TO_VIDEO_ENGINE_RULES.md` — Règle 0 (FFmpeg ≠ génération)
5. **Ce document** — profils de mouvement et valeurs par type

> Le MotionDirector ne génère rien. Il LIT ces sources, choisit le profil,
> assemble le prompt (positif + négatif), et produit un VideoJob.
> L'exécution reste au backend ComfyUI. La validation reste au Quality Gate.
> La décision finale reste à Ludovic.

---

*Motion Control Rules v1.0 — 2026-06-20*
