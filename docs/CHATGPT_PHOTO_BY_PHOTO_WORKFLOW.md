# ChatGPT Photo-By-Photo Workflow — YAWatch-LUNA

## Principe

Une demande ChatGPT = une seule photo finale.

On travaille personnage par personnage et case par case :

1. ChatGPT consulte les références canoniques sur GitHub.
2. Il produit une seule image correspondant à une case de checklist.
3. Ludovic télécharge l'image.
4. Codex la contrôle, la renomme et la classe.
5. Codex met à jour les checklists et GitHub.
6. On passe seulement ensuite à la photo suivante.

## Sources De Vérité GitHub

- Repo : https://github.com/byakuyakutchiki/yawatch-luna-stories
- Bible personnages : https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/docs/CHARACTER_BIBLE.md
- Direction visuelle : https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/docs/VISUAL_DIRECTION.md
- Checklist émotions : https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/docs/CHARACTER_LIBRARY_CHECKLIST.md
- Checklist poses : https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/docs/POSE_LIBRARY_CHECKLIST.md
- Assets classés : https://github.com/byakuyakutchiki/yawatch-luna-stories/tree/master/assets/luna_stories_assets

## Règles Pour ChatGPT

- Produire exactement une image, jamais une planche.
- Utiliser les fichiers GitHub indiqués comme références d'identité.
- Conserver le même visage, âge, cheveux, carnation et silhouette.
- Modifier seulement l'émotion, la pose, le cadrage ou le décor demandé.
- Format vertical 9:16, sauf indication contraire.
- Réalisme cinématographique premium.
- Présent parisien lumineux et crédible.
- Pas de cyberpunk générique, pas de New York.
- Pas de texte lisible, pas de watermark, pas de logo inventé.
- Émotions subtiles, jamais théâtrales.

## File De Production — Luna Adulte

### LUNA-A-001 — Neutral 9:16

Statut : `[x]` validé par la direction artistique le 13 juin 2026. Cette image devient la nouvelle référence canonique de Luna adulte pour toutes les générations suivantes.

Références :

- https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/01_luna_adulte/luna_adulte_reference_realiste_01.jpg
- https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/01_luna_adulte/luna_adulte_ceo_01.png
- https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/01_luna_adulte/luna_adulte_ceo_03_portrait.png

Prompt :

```text
Consulte d'abord ces trois références GitHub de Luna adulte :

1. https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/01_luna_adulte/luna_adulte_reference_realiste_01.jpg
2. https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/01_luna_adulte/luna_adulte_ceo_01.png
3. https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/01_luna_adulte/luna_adulte_ceo_03_portrait.png

Génère exactement UNE nouvelle photo de Luna adulte.

Objectif checklist : LUNA ADULTE — émotion NEUTRAL, portrait vertical propre 9:16.

Conserve strictement son identité visuelle : même femme méditerranéenne de 30 à 35 ans, mêmes traits du visage, mêmes longs cheveux bruns légèrement ondulés, mêmes yeux bruns profonds, silhouette élégante et crédible.

Scène : portrait vertical, Luna face caméra dans un bureau premium lumineux de YAWatch Industries à La Défense. Lumière naturelle parisienne, verre et architecture de bureau réaliste en arrière-plan. Blazer noir ou anthracite, chemisier sobre. Expression neutre, calme, intelligente, légèrement fatiguée mais sans inquiétude visible.

Important : Luna est la fausse suspecte de la saison 1, mais cette photo est sa référence neutre. Elle ne doit sembler ni méchante, ni glamour, ni théâtrale.

Contraintes : une seule image, 9:16, réalisme cinématographique premium, pas de violet dominant, pas de cyberpunk, pas de New York, pas de texte lisible, pas de watermark, pas de logo inventé.
```

Nom cible après téléchargement :

```text
luna_adulte_neutral_9x16_01.png
```

Premier candidat, ensuite promu comme référence canonique :

```text
assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png
```

Décision artistique : le visage diffère des anciennes références, mais son naturel, sa crédibilité et sa présence ont été préférés. Il remplace les anciennes images comme référence d'identité prioritaire.

### LUNA-A-001-R1 — Correction d'identité

Statut : annulé après validation artistique de `LUNA-A-001`. Ne pas générer.

```text
Tu dois CORRIGER la photo verticale que tu viens de générer, pas inventer une nouvelle femme.

Consulte cette référence d'identité principale de Luna adulte :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/01_luna_adulte/luna_adulte_reference_realiste_01.jpg

Génère exactement UNE image corrigée.

Conserve de la photo actuelle : le cadrage vertical 9:16, le bureau lumineux à La Défense, la lumière naturelle, le blazer noir, les longs cheveux bruns et l'expression neutre.

Corrige uniquement l'identité du personnage pour reproduire fidèlement le visage de la référence principale : même âge apparent, même forme douce et légèrement ovale du visage, mêmes grands yeux bruns, mêmes sourcils, même nez, mêmes lèvres et mêmes proportions. La nouvelle image ne doit pas paraître plus âgée, plus anguleuse ou plus sévère que la référence.

Luna doit rester naturelle, calme et légèrement fatiguée. Ne l'embellis pas et ne la transforme pas en mannequin. Aucun changement de décor ou de tenue.

Contraintes : une seule image, photoréalisme cinématographique, 9:16, pas de texte, pas de watermark, pas de logo inventé, pas de cyberpunk.
```

### LUNA-A-002 — Worried / Insomniaque

Statut : `[x]` validé le 13 juin 2026.

Prompt :

```text
Utilise comme unique référence d'identité canonique cette photo de Luna adulte :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png

Génère exactement UNE nouvelle photo du même personnage.

Objectif checklist : LUNA ADULTE — émotion WORRIED.

Luna se trouve dans son bureau YAWatch à La Défense, de nuit. Paris est flou derrière les grandes vitres. Elle porte le même style de blazer sobre. Son visage montre une inquiétude contenue et une fatigue insomniaque : regard légèrement fuyant, mâchoire détendue, respiration calme. Pas de larmes, pas de panique, pas de grimace.

La scène doit faire soupçonner qu'elle cache quelque chose sans la rendre mauvaise.

Contraintes : une seule image verticale 9:16, même visage que la référence canon, lumière nocturne réaliste, reflets discrets, pas de violet excessif, pas de cyberpunk, pas de texte, pas de watermark.
```

Nom cible : `luna_adulte_worried_9x16_01.png`

### LUNA-A-003 — Protective Avec Luna Doll

Statut : `[x]` validé le 13 juin 2026.

Référence poupée :

- https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/05_objets_symboliques_poupees/poupee_luna_violette_01.jpg

Prompt :

```text
Utilise comme unique référence d'identité canonique cette photo de Luna adulte :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png

Consulte la référence officielle de Luna Doll :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/05_objets_symboliques_poupees/poupee_luna_violette_01.jpg

Génère exactement UNE photo.

Objectif checklist : LUNA ADULTE — émotion PROTECTIVE, Luna Doll tenue dans les mains.

Luna tient délicatement contre elle une petite poupée artisanale en tissu d'environ 20 cm, cheveux bruns, robe violette légèrement usée. La poupée doit clairement rester un objet textile de petite taille : ce n'est ni un robot, ni une enfant miniature. Aucun métal, circuit, LED ou visage numérique.

Luna est dans un bureau parisien lumineux. Son geste est protecteur, son émotion retenue, son regard doux mais grave. Cadrage poitrine ou plan américain vertical.

Contraintes : une seule image 9:16, même visage de Luna, poupée fidèle à la référence, réalisme premium, pas de texte, pas de watermark, pas de logo inventé.
```

Nom cible : `luna_adulte_protective_luna_doll_01.png`

### LUNA-A-004 — Looking Out Window

Statut : `[x]` validé le 13 juin 2026.

Prompt :

```text
Utilise comme unique référence d'identité canonique cette photo de Luna adulte :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png

Génère exactement UNE photo.

Objectif checklist pose : LUNA ADULTE — LOOKING_OUT_WINDOW.

Luna est vue de profil, suffisamment tournée pour que son visage canonique reste identifiable, dans son bureau YAWatch à La Défense. Elle regarde Paris de nuit à travers une grande baie vitrée. Son reflet subtil reste visible dans le verre. Posture immobile, élégante, solitude contenue. Architecture réaliste de La Défense, pas de skyline américaine.

Contraintes : vertical 9:16, même visage et mêmes cheveux, lumière nocturne réaliste, pas de cyberpunk, pas de violet dominant, pas de texte, pas de watermark.
```

Nom cible : `luna_adulte_looking_out_window_01.png`

### LUNA-A-005 — Office Desk

Statut : `[x]` validé le 13 juin 2026.

Prompt :

```text
Utilise comme unique référence d'identité canonique cette photo de Luna adulte :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png

Utilise cette image uniquement comme référence de Luna Doll :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/05_objets_symboliques_poupees/poupee_luna_violette_01.jpg

Génère exactement UNE photo.

Objectif checklist pose : LUNA ADULTE — OFFICE_DESK.

Luna est assise à son bureau YAWatch à La Défense. Bureau premium mais sobre : ordinateur portable discret, dossier fermé sans texte lisible, Luna Doll posée sur un côté du bureau. Lumière parisienne de fin de journée. Luna travaille en silence, expression concentrée et calme. Son visage, ses deux mains et la poupée doivent être visibles sans se chevaucher.

La technologie doit rester crédible et secondaire. YAWatch est la conséquence de son traumatisme familial, pas un décor de science-fiction spectaculaire.

Contraintes : vertical 9:16, même identité, pas de cyberpunk, pas de faux texte, pas de logo inventé, pas de watermark.
```

Nom cible : `luna_adulte_office_desk_01.png`

### LUNA-A-006 — Looking At Turned Photo

Statut : `[x]` validé le 13 juin 2026. Le cadre est vertical, dos visible; son contenu reste entièrement caché.

Prompt :

```text
Utilise comme unique référence d'identité canonique cette photo de Luna adulte :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png

Génère exactement UNE photo.

Objectif checklist pose et teaser : LUNA ADULTE — LOOKING_AT_PHOTO.

Luna est assise devant son bureau YAWatch. Elle regarde une photo familiale encadrée posée face contre le bureau. Le contenu de la photo ne doit absolument pas être visible. Son expression est troublée mais contenue. Une main hésite près du cadre sans le retourner, l'autre repose naturellement sur le bureau. Elle ne regarde pas la caméra.

Décor lumineux et réaliste de La Défense, avec une bascule psychologique très subtile dans les reflets. Aucun père visible directement.

Contraintes : une seule image verticale 9:16, même visage de Luna, émotion subtile, pas de texte, pas de watermark, pas de violence, pas de cyberpunk.
```

Nom cible : `luna_adulte_looking_at_turned_photo_01.png`

## File De Production — Luna Enfant

### LUNA-E-001 — Neutral 9:16

Statut : à générer maintenant.

Références d'identité autorisées :

- https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/00_assets_deja_dans_app/app_luna_enfant_current.png
- https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/02_luna_enfant/luna_enfant_chambre_poupee_01.png

Références interdites pour cette génération : `app_aby_enfant_current.png` et `luna_enfant_maquette_ville_01.png`, qui représentent une enfant blonde et risquent de mélanger Luna avec Aby.

```text
Consulte uniquement ces deux références canoniques de Luna enfant :

1. https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/00_assets_deja_dans_app/app_luna_enfant_current.png
2. https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/02_luna_enfant/luna_enfant_chambre_poupee_01.png

Génère exactement UNE nouvelle photo de Luna enfant.

Objectif checklist : LUNA ENFANT — portrait NEUTRAL propre, vertical 9:16.

Conserve strictement l'identité visible sur les deux références : petite fille méditerranéenne d'environ 8 ans, longs cheveux bruns foncés, grands yeux bruns, visage doux et légèrement ovale, peau naturelle. Elle doit pouvoir être reconnue comme la version enfant de Luna adulte.

Attention : Luna enfant est brune. Ne consulte pas et ne reproduis pas `app_aby_enfant_current.png` ni `luna_enfant_maquette_ville_01.png`. Ne la transforme surtout pas en petite fille blonde : ce serait Aby ou une identité incohérente.

Scène : portrait vertical simple dans sa chambre parisienne, en journée, avec une lumière naturelle douce. Fond réaliste et discret, légèrement flou. Luna est debout ou assise face caméra, vêtue d'un haut bleu nuit ou violet très sombre, sans costume fantastique. Expression neutre, attentive et calme, avec une fragilité subtile; pas de sourire appuyé, pas de tristesse théâtrale.

Aucune poupée dans ses mains pour ce portrait de référence. Aucun autre enfant ni adulte visible.

Contraintes : exactement une image 9:16, photoréalisme cinématographique naturel, âge clairement enfantin et non adolescent, pas de glamour, pas de maquillage, pas de pose adulte, pas de cyberpunk, pas de texte, pas de watermark et pas de logo.
```

Nom cible : `luna_enfant_neutral_9x16_01.png`

## Validation Après Chaque Photo

Codex contrôle :

- identité du visage ;
- format et cadrage ;
- émotion demandée ;
- cohérence Paris / YAWatch ;
- absence d'artefacts ;
- absence de texte ou faux logo ;
- conformité à la checklist.

Si la photo est bonne : elle est classée et la case passe à `[x]`.

Si elle est presque bonne : elle est classée comme variante `[~]` et Codex écrit un prompt correctif unique.

Si elle est incohérente : elle n'entre pas dans le canon et la même case est régénérée.
