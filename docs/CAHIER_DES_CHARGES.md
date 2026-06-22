# Cahier des charges — YAWatch-LUNA, API de production vidéo

> Validé le 22 juin 2026. Objectif : produire des épisodes (thriller psychologique)
> via une API maison, coût marginal **~0,015 €/clip 5s**, sans dépendance Kling
> (sauf R&D). Personnages récurrents 100 % identifiables, mouvement corps entier,
> décors cohérents, montage/son/sous-titres intégrés.

## Les 4 capacités et leurs critères MESURABLES

### Capacité 1 — Corps entier + mouvement naturel  (P1)
| Critère | Min | Idéal | Métrique |
|---|---|---|---|
| Mouvement global | ≥ 0.15 | ≥ 0.25 | `flow_full` |
| Mouvement épaules | ≥ 0.08 | ≥ 0.15 | `flow_shoulders` |
| Mouvement cheveux | ≥ 0.05 | ≥ 0.12 | `flow_hair` |
| Translation risk (cadre qui glisse) | ≤ 0.35 | ≤ 0.20 | `translation_risk` |
| Score organique | ≥ 0.6 | ≥ 0.8 | `organic_score` |

### Capacité 2 — Personnages récurrents (identité stable)  (P1)
| Critère | Min | Idéal | Métrique |
|---|---|---|---|
| Identité SSIM visage (min) | ≥ 0.85 | ≥ 0.92 | `ssim_face_min` |
| Variation de teint | ≤ 15 % | ≤ 8 % | `lighting_face_pct` |

### Capacité 3 — Décors cohérents  (P2)
| Critère | Min | Idéal | Métrique |
|---|---|---|---|
| Cohérence fond (SSIM) | ≥ 0.70 | ≥ 0.80 | `background_ssim_mean` *(à brancher)* |
| Variation lumière fond | ≤ 10 % | ≤ 5 % | `background_lighting_pct` |
| Flicker fond | ≤ 0.5 | ≤ 0.3 | `background_flicker` |

### Capacité 4 — Qualité + assemblage  (P2)
| Critère | Seuil | Métrique |
|---|---|---|
| Montage cohérent | pas de rupture brutale | inspection humaine |
| Audio sync | < 0.1 s | `audio_sync_delay` |
| Sous-titres sync | < 0.2 s | `subtitle_sync_delay` |
- Code déjà fonctionnel : `video_builder.py`, `voice_generator.py`, `subtitle_generator.py`.

## Tableau de bord (22 juin)
| Capacité | Statut | Prochaine action | Prio |
|---|---|---|---|
| 1 Corps+mouvement | 🔴 mur I2V seul | restauration + LoRA | P1 |
| 2 Identité | 🟡 FramePack 0.94 / Wan 0.77 | valider restauration sur Wan | P1 |
| 3 Décors | 🟢 bon (FramePack) | mesurer auto (`background_ssim`) | P2 |
| 4 Montage/son | 🟢 fonctionnel | brancher vrais clips | P2 |

## Feuille de route Phase 2
| # | Action | Durée | Coût |
|---|---|---|---|
| 1 | Restauration (gfpgan) sur clip Wan + mesure | ~1h pod | ~0,20 € |
| 2 | Si OK → intégrer (capacité 1+2 résolue) | ~2h local | 0 € |
| 3 | Si KO → LoRA Luna (30-50 images) | ~2h pod | ~1,50 € |
| 4 | Intégrer LoRA → capacité 1+2 résolue | ~1h local | 0 € |
| 5 | Pipeline complet teaser (9 clips) | nuit | ~0,10 € élec |
| 6-7 | Assembler + documenter | ~1h | 0 € |

**Budget Phase 2 : ~0,20 € (si restauration suffit) → ~1,80 € (si LoRA).**

## Critère de réussite final (mesurable)
« Je lance un job MotionDirector sur 9 plans, je vais me coucher, et au réveil
je trouve un teaser MP4 où Luna bouge, parle, garde le même visage, dans des
décors cohérents. »

## Gouvernance
- Chaque test → `content/experiments/` avec ses métriques (pas d'intuition).
- Décisions prises sur les chiffres. Code versionné sur GitHub.

---

## Notes d'implémentation (honnêteté technique)
- **Branche de travail : `feat/governed-i2v-engines`** (le moteur gouverné, la
  boucle de mesure et la restauration y sont — pas sur `master`).
- **Restauration : GFPGAN d'abord** (pip, robuste, auto-poids) ; CodeFormer
  optionnel (install fragile sur torch récent). ReActor/InstantID si le visage
  doit être ré-ancré vers le Luna canonique (face-swap référencé).
- **Métriques branchées dans `experiment_runner.py`** : `flow_*`, `ssim_face_min`,
  `lighting_face_pct`, `flicker_face`, **`translation_risk`, `organic_score`,
  `face_residual`**, `background_lighting_pct`, `background_flicker`.
  Reste à brancher : `background_ssim_mean` (P2), `audio/subtitle_sync` (P2).
- **GPU** : Wan 14B ne tient pas en 8 Go (4060) → 4060 = AnimateDiff ; Wan = pod
  ou GPU ≥ 16 Go. Cible coût : 4060 possédé ≈ électricité ; cloud A4000 ≈ 0,015-0,02 €.
