# Analyse de production — Teaser S01E00 + EP01 + faisabilité Kling

> Avis rédigé par Kimi Code CLI le 2026-06-16.  
> Objectif : donner un état factuel des assets et du budget Kling pour que ChatGPT puisse critiquer / valider la stratégie.

---

## 1. Synthèse exécutive

| Projet | Assets | Format | Prêt pour Kling ? | Budget Kling estimé |
|---|---|---|---|---|
| **Teaser S01E00** (28 s) | 9 plans listés, 8 images existantes | 8/9 en 9:16 | ⚠️ Presque — 1 image carrée à corriger | ~2-4 € en standard |
| **EP01** (35-45 s) | 7 plans, 7 images générées | 7/7 en 9:16 | ✅ Oui | ~2-3 € en standard |
| **Teaser + EP01** | 16 clips | — | ✅ Réalisable avec 10 € | ~4-7 € |
| **Épisode 7 minutes** | ~60-90 clips nécessaires | — | ❌ Non réaliste avec Kling seul | 15-40 €+ |

**Verdict rapide** : avec 10 €, on peut produire le teaser ET EP01. Un épisode de 7 minutes avec Kling seul est un objectif de budget/temps supérieur.

---

## 2. Teaser S01E00 — État détaillé

Fichier de référence : `docs/TEASER_S01E00_PRODUCTION_PACK.md`.

### Plans requis vs images disponibles

| # | Asset requis | Fichier trouvé | Dimensions | Format | Statut |
|---|---|---|---|---|---|
| 1 | Tour YAWatch La Défense | `09_decors_paris_la_defense/pack_01_yawatch_industries/yawatch_tour_la_defense_exterieur_jour_logo_01.png` | 474 × 500 | presque carré | ⚠️ **À recadrer ou regénérer en 9:16** |
| 2 | Luna adulte portrait | `01_luna_adulte/luna_adulte_neutral_9x16_01.png` | 941 × 1672 | 9:16 | ✅ OK |
| 3 | Luna au bureau | `01_luna_adulte/luna_adulte_office_desk_01.png` | 941 × 1672 | 9:16 | ✅ OK |
| 4 | Luna regarde photo retournée | `01_luna_adulte/luna_adulte_looking_at_turned_photo_01.png` | 941 × 1672 | 9:16 | ✅ OK |
| 5 | Luna enfant inquiète | `02_luna_enfant/luna_enfant_worried_night_01.png` | 941 × 1672 | 9:16 | ✅ OK |
| 6 | Luna enfant rassurée avec poupée | `02_luna_enfant/luna_enfant_comforted_with_doll_01.png` | 941 × 1672 | 9:16 | ✅ OK |
| 7 | Gros plan yeux Luna Doll | `05_objets_symboliques_poupees/poupee_luna_gros_plan_yeux_mystere_01.png` | 941 × 1672 | 9:16 | ✅ OK |
| 8 | Aby observe Luna | `03_aby/aby_adulte_observing_luna_01.png` | 941 × 1672 | 9:16 | ✅ OK |
| 9 | Aby enfant + jeton noir | `03_aby/aby_enfant_main_jeton_noir_maquette_01.png` | 941 × 1672 | 9:16 | ✅ OK |

### Problème identifié

Le plan 1 (`yawatch_tour_la_defense_exterieur_jour_logo_01.png`) est en 474 × 500. Sur un Short vertical 1080 × 1920, il apparaîtrait avec des bandes noires importantes ou une perte de résolution après recadrage.

**Options** :
1. **Recadrer** l'image existante en 9:16 (perte de contenu latéral).
2. **Regénérer** un plan vertical de la tour YAWatch à La Défense avec ChatGPT.
3. **Remplacer** par un autre plan d'extérieur déjà en 9:16 si l'on accepte de modifier le storyboard.

---

## 3. EP01 — État détaillé

Fichier de référence : `assets/luna_stories_assets/episodes/EP01_LA_VILLE_DANS_LA_CHAMBRE/EP01_PRODUCTION_PACK.md`.

Les 7 plans du storyboard sont déjà générés en 9:16 dans :

```
assets/luna_stories_assets/episodes/EP01_LA_VILLE_DANS_LA_CHAMBRE/
```

| Plan | Fichier | Dimensions | Format | Statut |
|---|---|---|---|---|
| 01 — Chambre fenêtre nuit | `EP01_PLAN_01_chambre_fenetre_nuit.png` | 941 × 1672 | 9:16 | ✅ OK |
| 02 — Poupée Luna chambre nuit | `EP01_PLAN_02_poupee_luna_chambre_nuit.png` | 941 × 1672 | 9:16 | ✅ OK |
| 03 — Ville miniature illuminée | `EP01_PLAN_03_ville_miniature_illuminee.png` | 941 × 1672 | 9:16 | ✅ OK |
| 04 — Maison porte ouverte | `EP01_PLAN_04_maison_porte_ouverte.png` | 941 × 1672 | 9:16 | ✅ OK |
| 05 — Poupée + ville miniature | `EP01_PLAN_05_poupee_et_ville_miniature.png` | 941 × 1672 | 9:16 | ✅ OK |
| 06 — Ville comme vrai quartier | (référence non canon en paysage) | — | — | ⚠️ Plan 6 flou : peut être obtenu par morphing/dissolve au montage |
| 07 — Jeton Aby observe | `EP01_PLAN_07_jeton_aby_observe.png` | 941 × 1672 | 9:16 | ✅ OK |

**Note sur le plan 6** : le pack mentionne un plan symbolique où la ville miniature semble devenir un vrai quartier. Aucun asset 9:16 dédié n'a été trouvé. Ce plan peut être réalisé au montage par :
- Un fondu/dissolve entre `EP01_PLAN_03_ville_miniature_illuminee.png` et un plan de La Défense/Paris nocturne en 9:16.
- Un effet 2.5D (parallaxe) dans CapCut / DaVinci / After Effects.

EP01 est donc **fonctionnellement prêt** pour Kling, avec une petite réserve sur le plan 6.

---

## 4. Faisabilité Kling — Ce qu'il faut savoir

### Ce que Kling fait bien

- **Image-to-video** : animer une image fixe avec des mouvements de caméra, de la pluie, du vent, des lumières qui respirent.
- **Clips courts** : 5 à 10 secondes par génération selon le mode.
- **Mouvements doux** : parfait pour le ton mélancolique/intime de Luna Stories.

### Ce que Kling ne fait pas

- **Ne génère pas des vidéos longues** (pas de 7 minutes d'un bloc).
- **Ne garantit pas la cohérence personnage** d'un clip à l'autre (visage, lumière, décor peuvent varier).
- **Ne remplace pas le montage** : pas de voix off, pas de musique, pas de structure narrative intégrée.

### Workflow normal avec Kling

1. Uploader une image par plan.
2. Décrire le mouvement souhaité (pan, push-in, zoom, etc.).
3. Générer un clip de 5-10 secondes.
4. Télécharger tous les clips.
5. Assembler dans un logiciel de montage (CapCut, DaVinci Resolve, Premiere Pro).
6. Ajouter voix off, musique, sound design, transitions, texte.

---

## 5. Budget 10 € — Calcul réaliste

Hypothèses de prix Kling (moyenne constatée sur les plans grand public) :

- **1 crédit ≈ 0,01 à 0,03 €** selon le pack acheté.
- **1 clip standard 5 s ≈ 10-20 crédits**.
- **1 clip Pro 5-10 s ≈ 30-60 crédits**.

Avec 10 €, on dispose d'environ **300 à 1 000 crédits**.

### Scénarios

| Scénario | Nb clips | Crédits estimés | Coût estimé | Possible avec 10 € ? |
|---|---|---|---|---|
| Teaser standard (9 clips × 5 s) | 9 | ~90-180 | ~2-4 € | ✅ Oui |
| EP01 standard (7 clips × 5-6 s) | 7 | ~70-140 | ~1,5-3 € | ✅ Oui |
| **Teaser + EP01 standard** | 16 | ~160-320 | **~3-7 €** | ✅ **Oui, recommandé** |
| EP01 Pro haute qualité | 7 | ~210-420 | ~5-10 € | ⚠️ Juste |
| 7 minutes (60 clips standard) | 60 | ~600-1 200 | ~10-25 € | ❌ Non |
| 7 minutes (60 clips Pro) | 60 | ~1 800-3 600 | ~30-80 € | ❌ Non |

**Conclusion budget** : 10 € suffisent pour teaser + EP01 en qualité standard. Ce n'est pas assez pour un épisode de 7 minutes.

---

## 6. Recommandations

### Priorité immédiate

1. **Corriger le plan 1 du teaser** : générer ou recadrer la tour YAWatch en 9:16.
2. **Résoudre le plan 6 d'EP01** : choisir une image de Paris/La Défense nocturne en 9:16 pour le fondu, ou accepter un effet 2.5D.
3. **Produire EP01 d'abord** : c'est le projet le plus abouti et le moins cher.
4. **Puis produire le teaser** si le budget le permet.

### Pour le montage

- Utiliser **CapCut** ou **DaVinci Resolve** (gratuit).
- Exporter en **1080 × 1920**, 30 fps.
- Tester la voix off ElevenLabs avec le script défini avant de générer tous les clips.

### Pour un futur épisode long

- Ne pas viser 7 minutes en un seul Kling.
- Découper l'épisode en **4 à 6 Shorts de 30-45 s**.
- Publier les Shorts séparément, puis proposer une version "longue" assemblée.

---

## 7. Questions pour ChatGPT

L'utilisateur souhaite que ChatGPT analyse cet avis. Voici les questions clés à lui soumettre :

1. Le plan 1 du teaser (`yawatch_tour_la_defense_exterieur_jour_logo_01.png` en 474 × 500) doit-il être recadré ou regénéré en 9:16 ?
2. Le plan 6 d'EP01 peut-il être réalisé par un simple fondu au montage, ou faut-il générer un asset supplémentaire ?
3. Avec 10 €, faut-il privilégier la qualité Pro sur EP01 seul, ou la quantité (EP01 + teaser) en standard ?
4. Kling est-il le bon outil pour cette esthétique, ou Runway Gen-3 / Luma Dream Machine seraient-ils plus adaptés ?
5. Faut-il produire le teaser avant EP01 pour tester l'accueil du public, ou l'inverse ?

---

## Annexes

### Commandes utilisées pour vérifier les formats

```bash
python3 - <<'PY'
from PIL import Image
from pathlib import Path

paths = [
    "assets/luna_stories_assets/09_decors_paris_la_defense/pack_01_yawatch_industries/yawatch_tour_la_defense_exterieur_jour_logo_01.png",
    "assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png",
    "assets/luna_stories_assets/01_luna_adulte/luna_adulte_office_desk_01.png",
    "assets/luna_stories_assets/01_luna_adulte/luna_adulte_looking_at_turned_photo_01.png",
    "assets/luna_stories_assets/02_luna_enfant/luna_enfant_worried_night_01.png",
    "assets/luna_stories_assets/02_luna_enfant/luna_enfant_comforted_with_doll_01.png",
    "assets/luna_stories_assets/05_objets_symboliques_poupees/poupee_luna_gros_plan_yeux_mystere_01.png",
    "assets/luna_stories_assets/03_aby/aby_adulte_observing_luna_01.png",
    "assets/luna_stories_assets/03_aby/aby_enfant_main_jeton_noir_maquette_01.png",
]
for p in paths:
    with Image.open(Path(p)) as im:
        w, h = im.size
        print(f"{Path(p).name}: {w}x{h}")
PY
```

### Total d'assets dans le repo

- **175 fichiers** image au total.
- **43 assets** déjà en 9:16.
- **18 assets** en 16:9.
- Le reste est en formats divers (carrés, portraits non standard, archives de recherche).

---

*Fin de l'analyse.*
