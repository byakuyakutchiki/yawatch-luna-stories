# NEXT ACTIONS — YAWatch-LUNA (réel, versionné)

> Document de vérité, aligné sur l'**audit Codex** `da13360`
> (`docs/I2V_ENGINE_TESTS/WAN_FACESWAP_COLORMATCH_AUDIT_2026_06_22/AUDIT_REPORT.md`).
> Branche : `feat/frontend-queue`.

## Verdict de l'audit (Codex, 22 juin) — à respecter

**Ne PAS lancer le batch 9 plans avec le pipeline actuel.** Mesuré, avec référence Kling :

| Étape | Verdict | Fait clé |
|---|---|---|
| WAN original | REVIEW | visage appartient à la scène mais variation luma 47% (instable) |
| WAN + GFPGAN | FAIL (identité) | lisse trop, identité baisse (0.775→0.768) |
| WAN + face-swap | REVIEW / limite FAIL | identité +0.014 mais **netteté 18.7→9.3** (visage « posé ») |
| WAN + face-swap + colormatch | **FAIL** | **flicker 1.62→2.06**, variation 43→45%, perçu « recollé » |
| Kling (référence) | PASS | visage sombre **stable** (~15% variation), intégré à la scène |

## Le VRAI problème (révélé par l'audit)

Ce n'est **pas** la couleur ni la luminosité — c'est la **STABILITÉ LUMINEUSE temporelle** : Kling varie ~**15%** sur le visage, nos sorties WAN ~**42-47%**. Le visage « scintille » en exposition d'une frame à l'autre. C'est un problème de **génération**, pas réparable par un transfert couleur a posteriori (le colormatch empire même le flicker).

## Actions précises (ordre = par impact réel)

### A. Stabilité lumineuse (P1 — le vrai verrou)  [CODE + R&D]
- Cible : variation luma visage ≤ **15%** (niveau Kling), flicker ≤ 0.5.
- Pistes : (1) génération Wan plus stable (prompt « stable consistent lighting », seed fixe, cfg modéré) ; (2) **stabilisation d'exposition temporelle** (normaliser la luma frame-à-frame, ≠ transfert couleur) ; (3) prompt négatif anti-flicker renforcé.
- ✅ Critère : variation luma visage ≤ 15% mesurée, sans perte de netteté.

### B. Identité par LoRA, pas par swap (P1)  [pod, R&D]
- Le face-swap coûte trop de netteté pour un gain d'identité faible (audit). → entraîner un **LoRA Luna** pour que l'identité soit **dans le modèle** (pas de swap, pas de perte de matière).
- Pré-requis : meilleure image canonique (action C) + dataset 30-50 images.

### C. Meilleure image canonique Luna (ASSET — Ludovic/Codex)
- HD, bien éclairée, frontale, neutre. Dans `assets/luna_stories_assets/01_luna_adulte/`. Désigner LE fichier de référence.

### D. Colormatch : NE PAS utiliser tel quel (FAIL audit)
- Le transfert LAB global augmente le flicker. À **abandonner** ou refaire en **masque peau léger** seulement si A est résolu — basse priorité.

### E. Métriques artistiques (CODE — moi)
- Codex a déjà calculé netteté / artefact bord / delta LAB (`metrics.json` de l'audit). → **les brancher dans `tools/experiment_runner.py`** (en plus de SSIM suivi / organic) pour mesurer la matière cinéma à chaque test.

## Pré-requis BLOQUANTS pour le teaser 9 clips
1. **9 images sources** `plan01..plan09` — **n'existent pas** (`assets/teaser/` absent). À créer (assets).
2. **Modèles Wan sur volume persistant** (download unique — `tools/runpod/README.md`).
3. **Vrai pipeline batch** câblé avec nos commandes réelles. ⚠️ `experiment_runner generate`/`stabilize` **n'existent pas**.

## État des références (anti-confusion)
- ✅ RÉEL : commit `da13360` + `docs/I2V_ENGINE_TESTS/WAN_FACESWAP_COLORMATCH_AUDIT_2026_06_22/` (audit Codex, vérifié).
- ❌ ABSENT / inventé ailleurs : commit `632907c`, dossier `assets/teaser/`, `tools/batch_generate_teaser.sh` (jamais commité dans le repo).

## Décisions en attente (Ludovic)
- Valider/écarter la piste face-swap+colormatch (l'audit dit FAIL → je penche pour A+B au lieu de patcher le colormatch).
- Merger `feat/frontend-queue` → `master` ?

## Ordre recommandé
1. **A** (stabilité lumineuse) — c'est LE verrou identifié, testable d'abord sur la génération Wan.
2. **E** (brancher les métriques artistiques) en parallèle, sans pod.
3. **C** puis **B** (canonique → LoRA) pour l'identité propre, sans le coût netteté du swap.
4. Quand A+B tiennent (variation ≤15% + identité ≥0.85 + netteté préservée) → planifier le teaser (pré-requis 1-2-3).
