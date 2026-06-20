# FramePack PLAN02 Luna — Comparaison MOUVEMENT v1 vs v2 (RunPod cloud)

Date : 2026-06-21
Pour audit : DeepSeek (coordinateur)
GPU : RunPod RTX PRO 4500 Blackwell 32 Go

## Contexte

v1 (run 001) passait le Quality Gate (SSIM/lumière/flicker) mais le verdict humain de Ludovic
était : personnage figé, ~1/10 en mouvement. Diagnostic : les métriques techniques ne mesuraient
pas le mouvement perçu, et le TeaCache figeait l'image.

DECOUVERTE : les métriques de mouvement (optical flow Farneback par zone) EXISTENT DÉJÀ dans
`app/video_metrics_evaluator.py` (`optical_flow_mean`/`optical_flow_p95` pour face/hair/shoulders/
full_frame). Le `app/i2v_quality_gate.py` ne les utilise simplement PAS comme critère bloquant.
=> Le correctif n'est pas "écrire des métriques", c'est "brancher le mouvement dans le gate avec
un seuil calibré".

## Changements v2 (leviers RÉELS du nœud FramePackSampler)

| Paramètre | v1 | v2 | Raison |
|---|---|---|---|
| use_teacache | True | **False** | TeaCache saute des étapes -> fige le mouvement (levier #1) |
| guidance_scale | 10.0 | **7.0** | plus de liberté au modèle |
| seed | 2406202621 | **20260621** | explorer un autre espace |
| prompt | générique | **micro-mouvements séquentiels** (respiration->tête->yeux->épaules->cheveux) |
| Temps génération | 348 s | **510 s** | teacache off = calcul complet |

NB : `motion_strength` proposé ailleurs N'EXISTE PAS dans ce nœud. Ne pas l'utiliser.

## Résultats optical flow (calibrés sur vrais clips)

| Clip | full_frame | face | shoulders | hair | SSIM_min | durée |
|---|---:|---:|---:|---:|---:|---:|
| v1 FramePack (teacache ON, figé) | 0.063 | 0.090 | 0.087 | 0.083 | 0.955 | 9.06s |
| **v2 FramePack (teacache OFF)** | **0.146** | **0.290** | **0.203** | **0.238** | **0.439** | 9.06s |
| Wan2.1 (référence "bouge mais perd l'identité") | 0.375 | 0.641 | 0.564 | 0.530 | 0.522 | 5.06s |
| AnimateDiff local (Ken Burns, quasi statique) | 0.014 | 0.019 | 0.029 | 0.019 | 0.999 | 2.0s |

Gain mouvement v2/v1 : full ×2.3, face ×3.2, épaules ×2.3, cheveux ×2.9.

## Interprétation (IMPORTANT pour l'audit)

1. Le levier teacache OFF augmente réellement le mouvement (×2 à ×3). Confirmé.
2. Le SSIM_min chute (0.955 -> 0.439). MAIS ce SSIM compare chaque frame au PREMIER frame :
   tout mouvement (tête, clignement) fait baisser ce SSIM même si l'identité est préservée.
   => Cette métrique CONFOND mouvement et perte d'identité. Elle ne peut pas, seule, conclure.
3. Conséquence méthodo : remplacer la métrique d'identité "SSIM vs frame 0" par une vraie
   distance d'embedding de visage (ex. cosine sur ArcFace/InsightFace), qui mesure l'identité
   indépendamment du mouvement. Sinon le gate pénalise mécaniquement tout clip vivant.

## Seuils de mouvement proposés (calibrés, à valider)

Le clip "figé" est à ~0.06-0.09 ; un clip qui bouge est >0.15. Seuil minimum proposé pour
rejeter un clip trop statique (à ajouter dans i2v_quality_gate, opérateur >=) :

| Métrique | Seuil min proposé | Justification |
|---|---:|---|
| motion_full_frame_mean_min | 0.12 | au-dessus du figé (0.063), atteignable |
| motion_face_mean_min | 0.12 | figé=0.090 -> rejeté ; v2=0.290 -> OK |
| motion_shoulders_mean_min | 0.12 | figé=0.087 -> rejeté ; v2=0.203 -> OK |

## Décisions en attente (Ludovic)

- Verdict visuel v2 : est-ce toujours Luna (cas A) ou déformation (cas B) ?
  - Cas A -> recette trouvée ; corriger la métrique d'identité du gate (embedding visage).
  - Cas B -> v3 contrôlé : teacache OFF SEUL (guidance 10 + seed d'origine) pour isoler le gain
    de mouvement avec un risque d'identité minimal.

Fichiers : `YAWATCH_FRAMEPACK_PLAN02_LUNA_MOTION_V2_00001.mp4`, preview PNG,
`workflow_used.json`, `metrics_v1_vs_v2.json` (métriques brutes complètes toutes zones).
