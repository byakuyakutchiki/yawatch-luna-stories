# YAWatch-LUNA — Roadmap Phase 2 : l'usine maison (indépendance + coût)

> Décision (22 juin) : **Phase 1 = produire avec Kling** (rapide, fiable, ~0,2-1 €/clip)
> pour sortir le teaser et valider le créatif. **Phase 2 = construire la machine
> maison en parallèle** — bascule seulement quand elle est plus rapide ET moins
> chère pour le volume réel. Ce soir = coût de développement, l'actif compose.

## Ce qui est DÉJÀ en banque (poussé sur GitHub, branche `feat/governed-i2v-engines`)

- Moteur vidéo gouverné : API `/generate-shot`, adaptateurs Wan/FramePack réels
  (job scellé `job_hash` → backend ComfyUI → Quality Gate). `app/yawatch_video_engine/`.
- Boucle de mesure anti-aveugle : `tools/experiment_runner.py` (gate/experiment/restore),
  tableau versionné `content/experiments/`.
- Étage 2 restauration visage : `app/yawatch_video_engine/face_restore.py` (gfpgan).
- Provisioning robuste : `tools/runpod/provision.sh` (curl+Content-Length), `README.md`.
- Données prouvées : FramePack stable/figé vs Wan vivant/dérive — `docs/I2V_ENGINE_TESTS/GOVERNED_COMPARE_2026_06_22/`.

## Les 3 pièces manquantes (dans l'ordre, chacune = une session courte)

### Pièce 1 — Volume persistant stable (tue la galère d'infra)
- 1 network volume nommé ≥ 80 Go, modèles téléchargés **une seule fois**.
- Pod jetable rattaché ; **Stop** (jamais Terminate). Régime visé : génération en
  ~3-5 min, sans re-download. Cf. `tools/runpod/README.md`.
- ✅ Critère de succès : 2 sessions d'affilée sans re-télécharger.

### Pièce 2 — Restauration visage validée (étage 2)
- Sur le pod : `experiment_runner.py restore --clip <wan.mp4> --backend gfpgan`.
- ✅ Critère : Δ SSIM > 0 **sans** casser flicker ni mouvement.
- Si gfpgan insuffisant → tester **ReActor/InstantID** (face-swap vers Luna canonique).

### Pièce 3 — LoRA Luna (identité dans le modèle)
- Dataset : 30-50 images Luna, angles/expressions/lumières variés, fond simple,
  captions auto (BLIP/Florence). Source : `assets/luna_stories_assets/01_luna_adulte/`.
- Entraînement sur pod (A100 40 Go confortable ; 4090 24 Go = juste, batch 1 fp16).
  Outillage vidéo Wan immature → **valider la faisabilité avant** (pièce 2 d'abord).
- ✅ Critère : Luna marche/se retourne, SSIM identité ≥ 0,85 **avec** mouvement corps entier.

## Condition de bascule Kling → maison (la vraie métrique business)

Basculer quand, **mesuré** :
1. génération maison ≤ 5 min/clip en régime stable, ET
2. coût GPU/clip < coût Kling/clip à ton volume mensuel, ET
3. identité (SSIM) ≥ 0,85 sur mouvement corps entier (pièce 3 réussie).

Tant que les 3 ne sont pas vrais → **Kling reste rationnel pour produire.**

## Première action au retour (zéro réflexion)
1. Démarrer pod (template runpod/pytorch, rattacher LE volume persistant).
2. `provision.sh` (une fois sur volume neuf) puis lancer la **pièce 2** (restore).
3. Loguer le résultat dans `content/experiments/`. Décider pièce 3 sur données.
