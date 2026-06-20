# FramePack-HY — Mur identité/mouvement (4 itérations mesurées)

Date : 2026-06-21 — RunPod RTX PRO 4500 — PLAN02 Luna adulte
Pour audit : DeepSeek / ChatGPT (coordinateurs)

## Nouveau code : app/motion_metrics.py
Sépare le flux optique en TRANSLATION GLOBALE (cadre qui glisse) vs MOUVEMENT LOCAL RÉSIDUEL
(respiration, tête, épaules). Donne `organic_score`, `translation_risk`, résidus par zone.
But : rejeter une "carte postale qui glisse" même quand le flow brut est élevé.

## Les 4 itérations (mêmes image/seed sauf v2)

| ver | teacache | guidance | seed | organic | translation_risk | SSIM identité | lecture |
|---|---|---|---|---:|---:|---:|---|
| v1 | ON  | 10 | A | 0.279 | 0.091 | 0.955 | figé |
| v2 | OFF | 7  | B | 0.612 | 0.344 | 0.439 | bouge mais glisse + identité cassée |
| v3 | OFF | 9  | A | 0.189 | 0.031 | 0.969 | sur-corrigé, encore plus figé |
| v4 | OFF | 8  | A | 0.266 | 0.045 | 0.928 | meilleur compromis stable, mais retenu |

Cible visée : organic > 0.35, translation_risk < 0.20, SSIM > 0.85.

## Conclusion (data-driven)

FramePack-HY ÉCHANGE le mouvement contre l'identité. Dès qu'on garde SSIM > 0.9 sans glissement,
l'organic_score plafonne ~0.2-0.28 (v1, v3, v4). Le seul cas avec de la vraie vie (v2, 0.61) casse
l'identité (0.44) ET glisse (0.34). Ce n'est pas un problème de prompt/guidance/teacache : c'est la
nature du modèle (conçu anti-dérive). Sur une image unique, "vivant + identité + sans glissement"
n'est pas atteignable par tuning de paramètres.

## Options moteur (décision Ludovic, pas un réglage)

1. ACCEPTER FramePack v4 comme look "premium retenu" (stable, identité, micro-vie).
2. ESSAYER un I2V à plus fort mouvement : Wan2.2 I2V, LTX-Video, CogVideoX — risque identité (mesuré sur Wan).
3. PIPELINE 2 ÉTAGES : modèle-mouvement puis restauration/lock du visage (le plus proche d'un "Kling maison", + d'ingénierie).
4. (faible espoir) dernier levier FramePack : latent_window_size plus court / modèle FramePack-F1.

Recommandation : passer d'un débat de réglage à un choix de moteur (option 2 ou 3), arrêter le tuning v5/v6.
