# Audit YAWatch-LUNA - WAN -> face-swap -> colormatch

Date: 2026-06-22
Branche auditee: `feat/frontend-queue`
Objectif: identifier pourquoi la qualite artistique baisse apres restauration / face-swap / colormatch.

## Verdict court

Le pipeline actuel ne doit pas etre lance sur les 9 plans.

Le face-swap ameliore legerement l'identite mesuree, mais il abime la matiere cinema du visage: perte de nettete organique, peau plus traitee, visage moins naturellement lie a la scene.

Le colormatch n'est pas valide artistiquement. Il reduit partiellement l'ecart couleur mesure, mais augmente le flicker visage et ne restaure pas la logique lumineuse nocturne. A l'oeil, il donne encore plus l'impression d'un visage corrige puis recolle.

Verdict global: **FAIL pour teaser**, **REVIEW pour R&D**.

## Fichiers produits

- Planche comparative complete: `plan02_wan_faceswap_colormatch_comparison.png`
- Planche crops visage: `plan02_face_crops_comparison.png`
- Mesures detaillees: `metrics.json`
- Tableau mesures: `metrics.md`
- Frames extraites: `frames/`

## Clips audites

| Etape | Clip local | Statut fichier |
| --- | --- | --- |
| WAN original | `C:\Users\saint\Downloads\plan02_luna_WAN.mp4` | present |
| WAN + GFPGAN | `C:\Users\saint\Downloads\plan02_luna_WAN_restored_gfpgan.mp4` | present |
| WAN + face-swap | `C:\Users\saint\Downloads\plan02_luna_WAN_faceswap.mp4` | present |
| WAN + face-swap + colormatch | `C:\Users\saint\Downloads\plan02_luna_WAN_faceswap_colormatch.mp4` | present |
| Kling reference | `C:\Users\saint\Downloads\kling_20260619_VIDEO_Cinematic__4730_0.mp4` | present |

## Mesures principales

| Clip | Luma visage moyenne | Variation noir/clair visage | Flicker visage | Delta LAB visage/scene | Nettete visage | Artefact bord visage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| WAN original | 60.72 | 47.25 % | 1.2409 | 13.13 | 18.66 | 1.02 |
| WAN + GFPGAN | 58.85 | 42.51 % | 0.7266 | 12.96 | 23.38 | 0.97 |
| WAN + face-swap | 61.45 | 42.98 % | 1.6195 | 15.56 | 9.31 | 1.15 |
| WAN + face-swap + colormatch | 58.82 | 45.33 % | 2.0574 | 14.01 | 8.76 | 1.11 |
| Kling reference | 27.52 | 15.17 % | 0.4229 | 16.31 | 14.14 | 0.71 |

Interpretation importante:

- Kling n'est pas plus fort parce que le visage est plus clair. Au contraire, son visage reste sombre, stable, nocturne.
- Le vrai ecart est la stabilite lumineuse: Kling varie a environ 15 %, les sorties WAN restent autour de 42-47 %.
- Le colormatch baisse un peu le delta LAB face/scene par rapport au face-swap, mais augmente le flicker et la variation percue.
- Le face-swap fait chuter la nettete organique du visage: `18.66` sur WAN original, `9.31` apres face-swap, `8.76` apres colormatch.

## Analyse par etape

### 1. WAN original

Verdict: **REVIEW**

Points positifs:

- Le visage appartient encore a la scene.
- La lumiere semble plus naturelle que sur la version face-swappee.
- La correlation lumiere scene/visage reste meilleure que sur les versions traitees.

Problemes:

- Variation noir/clair trop forte.
- Identite Luna insuffisante d'apres les experiences precedentes.
- Le rendu reste trop "portrait anime" et pas assez plan cinema.

Utilisation teaser: possible uniquement comme base de R&D, pas comme plan final.

### 2. WAN + GFPGAN

Verdict: **REVIEW / FAIL comme solution identite**

Points positifs:

- Le flicker visage baisse.
- La nettete mesuree augmente.
- La variation luma baisse legerement.

Problemes:

- Les mesures precedentes montrent une identite plus faible: `0.7747 -> 0.7677`.
- Le visage devient plus lisse, plus restaure, moins naturel.
- GFPGAN ne resout pas le probleme central: Luna doit rester Luna sans effet "beauty restoration".

Utilisation teaser: non retenu comme solution principale.

### 3. WAN + face-swap

Verdict: **REVIEW, limite FAIL artistique**

Points positifs:

- Le face-swap ameliore legerement l'identite mesuree: `0.7747 -> 0.7887`.
- La silhouette globale du visage se rapproche davantage de Luna canonique.

Problemes:

- Gain identite trop faible pour le cout artistique.
- Nettete visage fortement degradee: `18.66 -> 9.31`.
- Artefacts de bord plus forts: `1.02 -> 1.15`.
- Le visage parait parfois pose sur la scene plutot qu'eclaire par elle.
- La peau perd de la micro-texture cinema.

Reponse a la question: oui, le face-swap ameliore l'identite, mais au prix d'une perte cinema visible.

Utilisation teaser: pas encore.

### 4. WAN + face-swap + colormatch

Verdict: **FAIL**

Points positifs:

- Le delta couleur visage/scene baisse par rapport au face-swap: `15.56 -> 14.01`.

Problemes:

- Flicker visage empire: `1.6195 -> 2.0574`.
- Variation noir/clair empire par rapport au face-swap: `42.98 % -> 45.33 %`.
- Nettete visage baisse encore: `9.31 -> 8.76`.
- L'oeil voit une correction locale plutot qu'une lumiere naturelle.
- L'ambiance nocturne est affaiblie; le visage parait parfois trop traite / trop separe.
- La lumiere ne semble pas toujours venir naturellement de la tablette ou de l'ecran.

Reponse a la question: le colormatch corrige une mesure, mais aggrave la perception. Donc **FAIL** selon la regle absolue: si le script dit OK mais que l'oeil voit une regression, verdict FAIL.

Utilisation teaser: non.

### 5. Kling reference

Verdict: **PASS comme reference artistique**

Ce que Kling fait mieux:

- Visage sombre mais lisible.
- Lumiere stable.
- Integration visage/corps/decor naturelle.
- Pas d'effet "visage recollee".
- L'ambiance nocturne reste coherente.

Kling n'est pas seulement une question de mouvement; c'est surtout une coherence globale lumiere + peau + decor + objet.

## Reponses directes

### A quelle etape la qualite se degrade-t-elle ?

La premiere degradation artistique nette arrive au **face-swap**: perte de texture, nettete organique divisee environ par deux, visage plus colle.

La seconde degradation arrive au **colormatch**: il ne repare pas le collage et ajoute plus de flicker / instabilite lumineuse.

### Le face-swap ameliore-t-il l'identite au prix d'une perte cinema ?

Oui. Le gain identite est reel mais trop faible, et le prix artistique est trop visible.

### Le colormatch corrige-t-il vraiment ou aggrave-t-il la perception ?

Il corrige partiellement une statistique couleur, mais aggrave la perception cinema. Verdict: il aggrave.

### Le visage appartient-il encore naturellement a la scene ?

Sur WAN original: plutot oui, mais identite faible.
Sur face-swap: partiellement.
Sur face-swap + colormatch: non, pas assez pour un teaser premium.

### Est-ce utilisable dans un teaser YAWatch-LUNA ?

Non pour la version colormatch actuelle.
Pas encore pour le face-swap actuel.
Le pipeline est utile pour apprendre, pas pour produire les 9 clips.

## Recommandations concretes

### Colormatch

Decision: **ne pas garder en l'etat**.

Modifier avant tout nouvel usage:

1. Ajouter une force de transfert couleur: `strength=0.20` a `0.35`, pas 1.0.
2. Limiter la correction au canal chroma `a/b` et proteger davantage la luminance `L`.
3. Ne jamais transferer la moyenne L globale si la scene est nocturne.
4. Exclure les hautes lumieres du visage et les zones proches des cheveux.
5. Ajouter un seuil anti-regression:
   - si flicker visage augmente de plus de 10 %, rejeter automatiquement;
   - si nettete visage baisse de plus de 10 %, rejeter;
   - si variation luma visage augmente, rejeter.
6. Produire automatiquement un side-by-side avant/apres avant tout commit de validation.

### Face-swap

Decision: **garder pour R&D, pas pour teaser final maintenant**.

A modifier:

1. Tester blending plus doux.
2. Reduire la force de swap ou mixer avec le visage original.
3. Ajouter restoration selective apres swap seulement si elle ne lisse pas la peau.
4. Mesurer la texture visage et le bord du masque, pas seulement SSIM.

### Alternative recommandee

Priorite suivante:

1. WAN comme motion pass.
2. Face identity pass plus doux:
   - InsightFace/ReActor avec blend faible;
   - ou LoRA Luna;
   - ou InstantID/IPAdapter si disponible.
3. Relighting global scene-aware plutot que colormatch local visage.
4. Deflicker / color stabilization temporal apres composition.
5. Quality Gate artistique:
   - luma visage variation;
   - flicker;
   - nettete;
   - artefact bord masque;
   - coherence lumiere source;
   - validation humaine Ludovic.

## Decision de production

Ne pas produire les 9 clips avec ce pipeline.

Prochaine experience utile:

- meme clip WAN;
- face-swap avec 3 forces/blends;
- colormatch faible `0.20`, `0.35`, `0.50`;
- rejet automatique si flicker/nettete/luma regressent;
- comparaison visuelle obligatoire avant toute generation batch.

Conclusion: la baisse de qualite ne vient pas d'un seul bug. Elle vient d'un pipeline qui optimise une statistique locale de visage sans respecter l'ambiance nocturne globale. Pour YAWatch-LUNA, l'image doit rester cinema avant d'etre "corrigee".
