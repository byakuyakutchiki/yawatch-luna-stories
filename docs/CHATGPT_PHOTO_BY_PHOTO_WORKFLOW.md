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
- Tenues cohérentes avec la fonction, le lieu et l'heure de la scène.
- Pour Luna et Aby au travail : silhouettes professionnelles parisiennes, élégantes et couvrantes; aucun décolleté plongeant, tissu transparent, tenue moulante ou look de femme fatale.
- Conserver la continuité vestimentaire entre deux plans appartenant à la même scène.

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

Statut : `[x]` validé le 13 juin 2026. Cette image devient la référence d'identité prioritaire de Luna enfant.

Références d'identité autorisées :

- https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/00_assets_deja_dans_app/app_luna_enfant_current.png
- https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/02_luna_enfant/luna_enfant_chambre_poupee_01.png

Références interdites pour cette génération : `app_aby_enfant_current.png` et `aby_enfant_canon_apk_maquette_ville_01.png`, qui représentent toutes les deux Aby enfant, la petite blonde.

```text
Consulte uniquement ces deux références canoniques de Luna enfant :

1. https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/00_assets_deja_dans_app/app_luna_enfant_current.png
2. https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/02_luna_enfant/luna_enfant_chambre_poupee_01.png

Génère exactement UNE nouvelle photo de Luna enfant.

Objectif checklist : LUNA ENFANT — portrait NEUTRAL propre, vertical 9:16.

Conserve strictement l'identité visible sur les deux références : petite fille méditerranéenne d'environ 8 ans, longs cheveux bruns foncés, grands yeux bruns, visage doux et légèrement ovale, peau naturelle. Elle doit pouvoir être reconnue comme la version enfant de Luna adulte.

Attention : Luna enfant est brune. Ne consulte pas et ne reproduis pas `app_aby_enfant_current.png` ni `aby_enfant_canon_apk_maquette_ville_01.png`. La petite fille blonde est officiellement Aby enfant.

Scène : portrait vertical simple dans sa chambre parisienne, en journée, avec une lumière naturelle douce. Fond réaliste et discret, légèrement flou. Luna est debout ou assise face caméra, vêtue d'un haut bleu nuit ou violet très sombre, sans costume fantastique. Expression neutre, attentive et calme, avec une fragilité subtile; pas de sourire appuyé, pas de tristesse théâtrale.

Aucune poupée dans ses mains pour ce portrait de référence. Aucun autre enfant ni adulte visible.

Contraintes : exactement une image 9:16, photoréalisme cinématographique naturel, âge clairement enfantin et non adolescent, pas de glamour, pas de maquillage, pas de pose adulte, pas de cyberpunk, pas de texte, pas de watermark et pas de logo.
```

Nom cible : `luna_enfant_neutral_9x16_01.png`

### LUNA-E-002 — Worried At Night

Statut : `[x]` validé le 13 juin 2026.

```text
Utilise comme unique référence d'identité canonique cette photo de Luna enfant :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/02_luna_enfant/luna_enfant_neutral_9x16_01.png

Génère exactement UNE nouvelle photo du même personnage.

Objectif checklist : LUNA ENFANT — émotion WORRIED, inquiétude nocturne contenue.

Conserve strictement son identité : même petite fille méditerranéenne d'environ 8 ans, même visage, mêmes grands yeux bruns, mêmes longs cheveux bruns foncés, même âge apparent et mêmes proportions enfantines.

Scène : Luna est assise sur le bord de son lit dans sa chambre parisienne, la nuit. Elle vient d'entendre un bruit inquiétant hors champ dans l'appartement. Elle regarde légèrement vers la porte fermée, jamais vers la caméra. Son expression montre une peur silencieuse et contenue : yeux attentifs, lèvres légèrement serrées, épaules un peu rentrées. Pas de larmes, pas de cri et pas de grimace.

La chambre est réaliste et rassurante en apparence : lampe de chevet chaude, faible lumière bleue venant de la fenêtre, quelques jouets discrets. Luna Doll peut être visible posée près d'elle sur le lit, mais Luna ne la tient pas encore. Aucun adulte, aucune silhouette, aucune violence et aucune menace visible.

Cadrage vertical 9:16, plan mi-corps ou plan américain. Luna doit paraître clairement enfantine, vulnérable et naturelle, jamais glamourisée.

Contraintes : exactement une image, photoréalisme cinématographique naturel, même identité que la référence, pas de maquillage, pas de pose adulte, pas de contenu violent, pas de texte, pas de watermark, pas de cyberpunk et pas de violet dominant.
```

Nom cible : `luna_enfant_worried_night_01.png`

### LUNA-E-003 — Comforted With Luna Doll

Statut : `[x]` validé le 13 juin 2026.

```text
Utilise comme unique référence d'identité canonique cette photo de Luna enfant :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/02_luna_enfant/luna_enfant_neutral_9x16_01.png

Utilise cette image comme référence de continuité pour la chambre, la tenue et la lumière :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/02_luna_enfant/luna_enfant_worried_night_01.png

Utilise cette image uniquement comme référence de Luna Doll :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/05_objets_symboliques_poupees/poupee_luna_violette_01.jpg

Génère exactement UNE nouvelle photo.

Crée une scène familiale douce et entièrement innocente : Luna enfant se rassure avec son jouet préféré.

Conserve strictement le même visage, le même âge d'environ 8 ans, les mêmes cheveux bruns, la même tenue de pyjama bleu nuit couvrante, la même chambre et le même éclairage chaud et bleu que la référence de continuité.

Luna est assise normalement sur son lit, entièrement habillée. Luna Doll repose sur ses genoux et Luna la tient doucement avec ses deux mains. La poupée est un petit jouet artisanal en tissu d'environ 20 cm, avec cheveux bruns et robe violette usée; ce n'est ni un robot ni une personne réelle.

Luna baisse légèrement les yeux vers son jouet avec une expression calme, pensive et rassurée. L'atmosphère est paisible et protectrice. Aucun danger, aucune peur intense, aucune détresse et aucune autre personne dans la pièce.

Ses deux mains doivent être visibles et tenir naturellement le jouet sur ses genoux, sans doigts fusionnés. La poupée doit être visible en entier ou presque, sans masquer le visage de Luna.

Cadrage vertical 9:16, plan mi-corps. La scène doit pouvoir être montée juste après `luna_enfant_worried_night_01.png` avec une continuité évidente.

Contraintes : exactement une image, scène familiale saine et non sensible, photoréalisme cinématographique naturel, enfant clairement âgée d'environ 8 ans et entièrement habillée, aucune violence, aucun adulte, pas de maquillage, pas de pose adulte, pas de texte, pas de watermark, pas de cyberpunk et pas de violet dominant.
```

Nom cible : `luna_enfant_vulnerable_with_doll_01.png`

Fichier finalement classé : `luna_enfant_comforted_with_doll_01.png`.

## File De Production — Aby Adulte

### ABY-A-001 — Neutral 9:16

Statut : `[x]` validé le 13 juin 2026. Cette image devient la référence d'identité prioritaire d'Aby adulte.

Référence adulte autorisée :

- https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/03_aby/aby_character_sheet_01.png

Ne pas utiliser `aby_character_sheet_02.png` : cette planche représente Aby adolescente, pas Aby adulte.

```text
Consulte cette planche GitHub uniquement pour identifier l'apparence d'Aby adulte :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/03_aby/aby_character_sheet_01.png

Génère exactement UNE nouvelle photo d'Aby adulte, jamais une planche ni un collage.

Objectif checklist : ABY ADULTE — portrait NEUTRAL propre, vertical 9:16.

Reproduis fidèlement l'identité adulte montrée dans la planche : femme française d'environ 28 ans, cheveux blond foncé avec racines légèrement plus sombres, coiffés en chignon haut volontairement imparfait avec quelques mèches libres, yeux très foncés, traits fins et anguleux, silhouette élégante. Elle porte un tailleur noir sobre et quelques bijoux discrets.

Aby est la manipulatrice cachée de la saison 1, mais ce portrait ne doit pas la présenter comme une méchante évidente. Son expression est neutre, intelligente, calme et professionnelle. Son regard direct laisse seulement deviner qu'elle observe beaucoup.

Scène : portrait vertical dans un bureau contemporain lumineux de YAWatch Industries à La Défense, en journée. Architecture de verre réaliste, lumière naturelle parisienne, arrière-plan légèrement flou. Aucun écran futuriste et aucun décor nocturne violet.

Attention : ne reproduis aucun texte, aucune citation, aucun logo ni aucune mise en page de la planche. Ne génère pas Aby adolescente. Une seule femme adulte doit apparaître.

Contraintes : exactement une image 9:16, photoréalisme cinématographique premium, apparence adulte d'environ 28 ans, pas de glamour excessif, pas de regard menaçant, pas de cyberpunk, pas de New York, pas de texte, pas de watermark et pas de logo inventé.
```

Nom cible : `aby_adulte_neutral_9x16_01.png`

### ABY-A-002 — Observing Luna

Statut : `[x]` validé le 13 juin 2026.

```text
Utilise comme unique référence d'identité canonique cette photo d'Aby adulte :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/03_aby/aby_adulte_neutral_9x16_01.png

Génère exactement UNE nouvelle photo du même personnage.

Objectif checklist : ABY ADULTE — émotion SUSPICIOUS subtile, sans révéler qu'elle est la manipulatrice cachée.

Conserve strictement son visage, son âge apparent d'environ 28 ans, son chignon blond imparfait aux racines sombres et ses yeux foncés.

Tenue obligatoire : tailleur pantalon noir ou anthracite parfaitement ajusté, blazer structuré fermé ou porté sur un chemisier noir couvrant à col simple, sans décolleté plongeant. Bijoux très discrets, chaussures professionnelles sobres, aucune tenue moulante, transparente, glamour ou sexualisée. Aby doit évoquer une directrice stratégique parisienne haut de gamme, pas un mannequin ni une femme fatale.

Scène : réunion professionnelle en journée dans une salle vitrée de YAWatch Industries à La Défense. Aby est assise de trois quarts à une table de réunion. Elle regarde légèrement hors champ vers Luna, qui ne doit pas apparaître dans l'image. Un dossier fermé et un stylo sont posés devant elle, sans texte lisible.

Son expression reste calme, courtoise et professionnelle. Un très léger sourire contenu et un regard attentif suggèrent qu'elle comprend davantage que les autres. Elle ne doit jamais sembler menaçante, cruelle ou caricaturale. Cette image doit paraître normale au premier visionnage et ambiguë seulement après la révélation de fin de saison.

Lumière naturelle parisienne, verre et architecture contemporaine crédible de La Défense. Arrière-plan légèrement flou avec quelques collègues indistincts, sans visage détaillé.

Cadrage vertical 9:16, plan poitrine ou plan américain. Ses mains doivent être visibles et naturelles, l'une près du dossier ou tenant doucement le stylo.

Contraintes : exactement une image, photoréalisme cinématographique premium, même identité que la référence, tenue professionnelle couvrante, pas de lumière violette dominante, pas de cyberpunk, pas de texte, pas de watermark, pas de logo inventé, pas de regard de méchante et pas de sexualisation.
```

Nom cible : `aby_adulte_observing_luna_01.png`

### ABY-A-003 — Vulnerable After Meeting

Statut : `[x]` validé le 14 juin 2026.

```text
Utilise comme unique référence d'identité canonique cette photo d'Aby adulte :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/03_aby/aby_adulte_neutral_9x16_01.png

Utilise cette image comme référence de continuité pour sa tenue professionnelle :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/03_aby/aby_adulte_observing_luna_01.png

Génère exactement UNE nouvelle photo du même personnage.

Objectif checklist : ABY ADULTE — émotion VULNERABLE, blessure cachée brièvement visible.

Conserve strictement son visage, son âge apparent d'environ 28 ans, son chignon blond imparfait aux racines sombres, ses yeux foncés et la même tenue professionnelle couvrante : tailleur noir structuré, chemisier noir fermé, bijoux très discrets. Aucun décolleté plongeant, aucune tenue glamour ou sexualisée.

Scène : quelques minutes après la réunion, Aby est seule dans une petite salle vitrée de YAWatch Industries à La Défense. Elle est assise près de la table, légèrement tournée vers la fenêtre. Le dossier fermé de la réunion est posé devant elle. Elle ne regarde pas la caméra.

Pour un instant, son contrôle se fissure : regard baissé ou perdu vers Paris, mâchoire détendue, fatigue contenue. Elle semble blessée et isolée, mais ne pleure pas. Aucun geste spectaculaire, aucune main sur le visage et aucune posture théâtrale.

Une main repose naturellement sur le dossier fermé; l'autre tient doucement son poignet ou repose sur la table. Les mains doivent être entièrement visibles et anatomiquement correctes.

Lumière parisienne douce de fin d'après-midi, décor clair et réaliste. La scène doit donner envie de comprendre Aby, pas de la condamner.

Cadrage vertical 9:16, plan poitrine ou plan américain. Une seule femme adulte apparaît.

Contraintes : exactement une image, photoréalisme cinématographique premium, tenue professionnelle couvrante, émotion subtile, pas de larmes, pas de sexualisation, pas de cyberpunk, pas de violet dominant, pas de texte, pas de watermark et pas de logo inventé.
```

Nom cible : `aby_adulte_vulnerable_after_meeting_01.png`

### ABY-A-004 — Controlled Anger

Statut : `[x]` validé le 14 juin 2026. Pack initial Aby adulte complet.

```text
Utilise comme unique référence d'identité canonique cette photo d'Aby adulte :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/03_aby/aby_adulte_neutral_9x16_01.png

Utilise cette image comme référence stricte de tenue professionnelle :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/03_aby/aby_adulte_observing_luna_01.png

Génère exactement UNE nouvelle photo du même personnage.

Objectif checklist : ABY ADULTE — émotion CONTROLLED_ANGER, colère entièrement maîtrisée.

Conserve strictement son visage, son âge apparent d'environ 28 ans, son chignon blond imparfait aux racines sombres, ses yeux foncés et sa tenue professionnelle couvrante : tailleur noir structuré et chemisier noir fermé, bijoux très discrets. Aucun décolleté plongeant, aucune tenue moulante, glamour ou sexualisée.

Scène : Aby est debout au bout d'une table de réunion dans une salle vitrée de YAWatch Industries à La Défense. Une discussion difficile vient de se terminer. Elle regarde une personne hors champ, jamais la caméra. Aucun autre personnage identifiable ne doit apparaître.

Sa colère reste presque invisible : mâchoire légèrement tendue, regard fixe et calme, lèvres fermées, respiration maîtrisée. Une main est posée fermement mais naturellement sur un dossier fermé; l'autre reste détendue le long du corps ou près de la table. Aucun poing serré, aucun cri, aucun geste agressif.

La scène doit montrer une femme qui transforme immédiatement son émotion en stratégie. Elle ne doit ressembler ni à une méchante caricaturale ni à une femme fatale.

Lumière naturelle parisienne de fin de journée, architecture claire et crédible de La Défense. Cadrage vertical 9:16, plan américain permettant de voir son visage, sa posture et ses mains.

Contraintes : exactement une image, photoréalisme cinématographique premium, tenue professionnelle couvrante, même identité que la référence, colère subtile, pas de violence, pas de sexualisation, pas de cyberpunk, pas de violet dominant, pas de texte, pas de watermark et pas de logo inventé.
```

Nom cible : `aby_adulte_controlled_anger_01.png`

## File De Production — Mère De Luna Et Aby

### MERE-001 — Neutral 9:16

Statut : `[x]` validé le 14 juin 2026. Cette image devient la référence d'identité prioritaire de la mère.

Références d'identité :

- https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/10_famille_luna/luna_parents_portrait_officiel_yawatch_01.png
- https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/10_famille_luna/luna_parents_cuisine_matin_01.png

```text
Consulte ces deux références GitHub pour identifier uniquement la mère de Luna et Aby :

1. https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/10_famille_luna/luna_parents_portrait_officiel_yawatch_01.png
2. https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/10_famille_luna/luna_parents_cuisine_matin_01.png

Génère exactement UNE nouvelle photo de la mère seule. Le père ne doit pas apparaître.

Objectif checklist : MÈRE DE LUNA ET ABY — portrait NEUTRAL propre, vertical 9:16.

Reproduis fidèlement la femme visible sur les références : femme méditerranéenne française d'environ 48 à 52 ans, cheveux bruns foncés mi-courts et ondulés, yeux bruns, traits fins et élégants, visage mature naturel. Elle doit être clairement plus âgée que Luna adulte, sans être vieillie artificiellement.

Scène : portrait vertical dans le salon lumineux d'un appartement parisien contemporain. Lumière naturelle de journée, immeubles haussmanniens discrètement visibles derrière une fenêtre, fond réaliste légèrement flou. Expression neutre, douce, attentive et légèrement fatiguée.

Tenue obligatoire : pantalon sombre et chemisier ou pull fin couvrant, élégant mais quotidien, col simple, manches longues ou trois-quarts. Bijoux familiaux très discrets. Aucun décolleté plongeant, aucune tenue moulante, glamour ou sexualisée.

La mère doit sembler humaine et protectrice, pas riche et froide, pas menaçante et pas coupable. Ce portrait sert uniquement à verrouiller son identité avant les émotions narratives.

Attention : ne reproduis pas le père, le logo, le bureau nocturne ou la composition des références. Une seule femme adulte doit apparaître.

Contraintes : exactement une image 9:16, photoréalisme cinématographique naturel, âge visible 48–52 ans, tenue couvrante, Paris crédible, pas de cyberpunk, pas de violet dominant, pas de texte, pas de watermark et pas de logo inventé.
```

Nom cible : `mere_luna_aby_neutral_9x16_01.png`

### MERE-002 — Worried In Bright Apartment

Statut : `[x]` validé le 15 juin 2026.

```text
Utilise comme unique référence d'identité canonique cette photo de la mère de Luna et Aby :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/10_famille_luna/mere_luna_aby_neutral_9x16_01.png

Génère exactement UNE nouvelle photo du même personnage.

Objectif checklist : MÈRE DE LUNA ET ABY — émotion WORRIED, inquiétude contenue dans un appartement lumineux.

Conserve strictement son visage mature d'environ 48 à 52 ans, ses cheveux bruns mi-courts ondulés, ses yeux bruns et ses proportions naturelles.

Tenue obligatoire : pantalon sombre et chemisier opaque à col rond ou boutonné jusqu'en haut, manches longues, coupe quotidienne élégante et couvrante. Bijoux très discrets. Aucun décolleté, tissu transparent, tenue moulante, glamour ou sexualisée.

Scène : elle est debout près de la fenêtre du salon de son appartement parisien, en pleine journée. Les façades haussmanniennes sont visibles mais floues derrière elle. Elle vient de recevoir une information inquiétante par téléphone, mais le téléphone est maintenant posé sur une table, écran invisible et sans texte.

Elle regarde légèrement hors champ vers le couloir. Son inquiétude reste contenue : sourcils très légèrement rapprochés, regard attentif, lèvres au repos, une main posée naturellement sur le dossier d'une chaise. Pas de larmes, pas de panique, pas de geste théâtral.

L'appartement demeure clair, chaleureux et réaliste. La tension vient uniquement de son visage et d'un silence inhabituel, jamais d'une lumière violette ou d'un décor horrifique. Aucun autre personnage ne doit apparaître.

Cadrage vertical 9:16, plan américain permettant de voir son visage, sa posture et ses deux mains.

Contraintes : exactement une image, photoréalisme cinématographique naturel, même identité que la référence, âge mature préservé, tenue couvrante, Paris crédible, pas de violence, pas de cyberpunk, pas de texte, pas de watermark et pas de logo inventé.
```

Nom cible : `mere_luna_aby_worried_apartment_01.png`

### MERE-003 — Protective Memory Box

Statut : `[x]` validé le 15 juin 2026.

```text
Utilise comme unique référence d'identité canonique cette photo de la mère de Luna et Aby :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/10_famille_luna/mere_luna_aby_neutral_9x16_01.png

Utilise cette image comme référence de continuité pour l'appartement et sa tenue :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/10_famille_luna/mere_luna_aby_worried_apartment_01.png

Utilise cette image uniquement comme référence de Luna Doll :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/05_objets_symboliques_poupees/poupee_luna_violette_01.jpg

Génère exactement UNE nouvelle photo du même personnage.

Objectif checklist : MÈRE DE LUNA ET ABY — émotion PROTECTIVE, préservation d'un souvenir familial.

Conserve strictement son visage mature d'environ 48 à 52 ans, ses cheveux bruns mi-courts ondulés, ses yeux bruns et ses proportions naturelles.

Tenue obligatoire : même pantalon sombre et même chemisier ivoire opaque à manches longues que dans la scène précédente, mais boutonné plus haut avec une encolure fermée et couvrante. Bijoux très discrets. Aucune tenue glamour, moulante, transparente ou sexualisée.

Scène : dans le salon lumineux de son appartement parisien, la mère est assise à une table. Devant elle se trouve une boîte à souvenirs en bois ouverte. Elle dépose délicatement Luna Doll dans la boîte ou la tient juste au-dessus, comme si elle voulait préserver un objet précieux de l'enfance de ses filles.

Luna Doll reste une petite poupée artisanale en tissu d'environ 20 cm, cheveux bruns et robe violette légèrement usée. Ce n'est ni un robot ni une personne réelle.

L'expression de la mère est protectrice, douce et grave. Elle regarde la poupée, jamais la caméra. Aucun enfant, aucun père et aucun autre personnage ne doit apparaître. Aucun contenu de photo familiale ne doit être visible dans la boîte.

Ses deux mains doivent être entièrement visibles et tenir naturellement la poupée, sans doigts fusionnés. La poupée ne doit pas masquer son visage.

Lumière naturelle de journée, appartement clair et réaliste, façades parisiennes discrètes derrière la fenêtre. Cadrage vertical 9:16, plan américain montrant son visage, ses mains, la poupée et la boîte.

Contraintes : exactement une image, photoréalisme cinématographique naturel, même identité et même âge que la référence, tenue couvrante, scène familiale saine, pas de violence, pas de cyberpunk, pas de violet dominant, pas de texte, pas de watermark et pas de logo inventé.
```

Nom cible : `mere_luna_aby_protective_memory_box_01.png`

### MERE-004 — Vulnerable With Closed Memory Box

Statut : `[x]` validé le 15 juin 2026. Pack initial de la mère complet.

```text
Utilise comme unique référence d'identité canonique cette photo de la mère de Luna et Aby :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/10_famille_luna/mere_luna_aby_neutral_9x16_01.png

Utilise cette image comme référence stricte de continuité pour la tenue, la table, la boîte et l'appartement :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/10_famille_luna/mere_luna_aby_protective_memory_box_01.png

Génère exactement UNE nouvelle photo du même personnage.

Objectif checklist : MÈRE DE LUNA ET ABY — émotion VULNERABLE, secret familial porté en silence.

Conserve strictement son visage mature d'environ 48 à 52 ans, ses cheveux bruns mi-courts ondulés, ses yeux bruns, ses proportions naturelles et exactement la même tenue couvrante : pantalon sombre, chemisier ivoire opaque à manches longues et encolure fermée, bijoux très discrets.

Scène : quelques instants après avoir rangé Luna Doll, la mère est toujours assise à la même table dans le salon lumineux. La boîte à souvenirs en bois est maintenant fermée devant elle. Aucun contenu de la boîte n'est visible.

Elle pose doucement ses deux mains sur le couvercle fermé et regarde vers la fenêtre, jamais la caméra. Son visage exprime une fatigue émotionnelle contenue et le poids d'un secret ancien. Elle reste digne et calme : aucune larme, aucune grimace, aucune main sur le visage et aucun geste théâtral.

Aucun enfant, aucun père, aucune poupée visible et aucun autre personnage ne doit apparaître. La vulnérabilité vient uniquement du regard, de la posture légèrement relâchée et du silence.

Lumière naturelle parisienne de fin d'après-midi, appartement toujours clair, façades haussmanniennes légèrement floues derrière la fenêtre. Cadrage vertical 9:16, plan américain montrant son visage, ses deux mains et la boîte fermée.

Contraintes : exactement une image, photoréalisme cinématographique naturel, même identité et même âge, continuité parfaite de tenue et de décor, tenue couvrante, pas de larmes, pas de violence, pas de sexualisation, pas de cyberpunk, pas de violet dominant, pas de texte, pas de watermark et pas de logo inventé.
```

Nom cible : `mere_luna_aby_vulnerable_closed_box_01.png`

## File De Production — Aby Enfant, Plans Symboliques

### ABY-E-001 — Main Et Jeton Noir

Statut : `[x]` validé le 15 juin 2026. La version téléchargée à 17:10 est retenue; la version antérieure, plus plate, n'entre pas dans le canon.

Référence de la maquette et de l'univers d'Aby enfant :

- https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/03_aby/aby_enfant_canon_apk_maquette_ville_01.png

```text
Consulte cette référence GitHub uniquement pour reproduire la ville miniature et l'univers visuel d'Aby enfant :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/03_aby/aby_enfant_canon_apk_maquette_ville_01.png

Génère exactement UNE image symbolique, sans visage et sans personnage identifiable.

Objectif checklist : ABY ENFANT — une petite main pose un jeton noir sur une ville miniature.

Scène familiale entièrement innocente : gros plan cinématographique sur une maquette de quartier parisien construite comme un jeu de stratégie. Une petite main d'enfant, visible seulement du poignet jusqu'aux doigts et couverte par la manche longue d'un pull noir, pose délicatement un jeton rond noir sur le toit d'un bâtiment miniature.

Aucun visage, aucune tête, aucun corps, aucune peau autre que la main et aucun autre enfant ne doivent apparaître. La main accomplit simplement un geste de jeu calme, sans danger ni violence.

La ville miniature doit être détaillée et réaliste : petites maisons parisiennes, rues éclairées, quelques éléments violets très discrets. Le jeton noir est simple, mat, sans symbole, sans texte et sans logo. Il doit être clairement distinct des bâtiments.

Éclairage chaleureux de chambre en fin d'après-midi, avec une légère lumière froide venant d'une fenêtre hors champ. L'image suggère la stratégie et le contrôle, jamais la peur ou la menace.

Cadrage vertical 9:16, mise au point sur les doigts, le jeton et la zone de la maquette où il est posé. Anatomie de la main naturelle, cinq doigts cohérents, aucun doigt fusionné.

Contraintes : exactement une image, scène saine et non sensible, photoréalisme cinématographique premium, aucun visage, aucun personnage complet, aucune violence, aucun texte, aucun watermark, aucun logo inventé et pas de cyberpunk.
```

Nom cible : `aby_enfant_main_jeton_noir_maquette_01.png`

## File De Production — Transmission De Luna Doll

### DOLL-T-001 — La Mère Remet La Boîte À Luna

Statut : `[x]` validé le 15 juin 2026 après correction ciblée du visage de Luna.

Usage : plan narratif large approuvé pour le montage. Cette image ne remplace pas les portraits canoniques individuels de Luna ou de sa mère comme références d'identité.

Cette scène est le raccord canonique entre les états `CHEZ_LA_MERE` et `BUREAU_LUNA`.

```text
Utilise comme référence d'identité canonique de la mère :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/10_famille_luna/mere_luna_aby_neutral_9x16_01.png

Utilise comme référence d'identité canonique de Luna adulte :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png

Utilise comme référence stricte de la boîte à souvenirs et de la tenue de la mère :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/10_famille_luna/mere_luna_aby_vulnerable_closed_box_01.png

Génère exactement UNE nouvelle photo avec uniquement ces deux femmes adultes.

Objectif narratif : LA TRANSMISSION — la mère remet à Luna adulte la boîte fermée qui contient Luna Doll. C'est la scène qui explique pourquoi la poupée quitte l'appartement de la mère et apparaît ensuite dans le bureau de Luna.

Scène : dans le salon lumineux de l'appartement parisien de la mère, les deux femmes sont debout ou assises face à face près de la table en bois. La mère tend la boîte à souvenirs fermée à Luna. Luna la reçoit avec ses deux mains. La poupée ne doit absolument pas être visible; la boîte reste fermée et aucun contenu n'apparaît.

Conserve strictement les deux identités et leurs âges : la mère a environ 48 à 52 ans, cheveux bruns mi-courts ondulés; Luna a environ 32 ans, longs cheveux bruns ondulés. Elles doivent être clairement distinctes, mère et fille, sans fusion de leurs traits.

Tenues : la mère porte exactement son chemisier ivoire opaque à manches longues et encolure fermée avec pantalon sombre. Luna porte un pantalon anthracite et un pull fin noir à col rond ou un chemisier noir fermé sous un blazer sobre. Les deux tenues sont élégantes, couvrantes et quotidiennes; aucun décolleté, vêtement transparent, moulant, glamour ou sexualisé.

Émotion : la mère est grave mais soulagée; Luna est surprise et émue, sans larmes. Elles regardent la boîte ou brièvement l'une vers l'autre, jamais la caméra. Le geste doit être intime et retenu, pas cérémoniel.

Les quatre mains doivent être visibles, anatomiquement correctes et tenir naturellement la même boîte, sans doigts fusionnés. Une seule boîte existe. Aucun père, aucune Aby, aucun enfant et aucun autre personnage ne doivent apparaître.

Lumière naturelle parisienne de fin d'après-midi, façades haussmanniennes légèrement floues derrière la fenêtre. Cadrage vertical 9:16, plan américain suffisamment large pour montrer les deux visages, les mains et la boîte.

Contraintes : exactement une image, photoréalisme cinématographique naturel, deux femmes adultes seulement, une seule boîte fermée, Luna Doll invisible, tenues couvrantes, pas de violence, pas de cyberpunk, pas de violet dominant, pas de texte, pas de watermark et pas de logo inventé.
```

Nom cible : `mere_transmet_boite_luna_adulte_01.png`

## File De Production — Luna Doll, Plan Mystère

### DOLL-M-001 — Gros Plan Sur Les Yeux

Statut : à générer maintenant.

Ce plan complète le dernier état manquant de Luna Doll et sert de ponctuation mystérieuse dans EP01.

```text
Utilise cette image uniquement comme référence canonique stricte de Luna Doll :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/05_objets_symboliques_poupees/poupee_luna_violette_01.jpg

Génère exactement UNE nouvelle photo de Luna Doll, sans aucun personnage humain.

Objectif : créer un très gros plan cinématographique mystérieux sur le visage et surtout les deux yeux de la poupée.

Luna Doll reste exactement la même petite poupée artisanale en tissu : mêmes cheveux bruns en laine, même peau textile cousue, mêmes deux petits yeux sombres, mêmes proportions et même fabrication légèrement usée. Elle reste clairement un jouet inanimé. Ce n'est ni une enfant réelle, ni un robot, ni une poupée de porcelaine.

Cadrage vertical 9:16, macro très rapprochée. Les deux yeux doivent être entièrement visibles, nets et symétriques; une partie des cheveux bruns et du haut du visage reste dans le cadre. La robe violette peut apparaître très légèrement en bas, sans dominer l'image.

Éclairage réaliste de fin de journée venant d'une fenêtre du bureau de Luna. Dans les yeux sombres, ajoute uniquement un minuscule reflet naturel rectangulaire de fenêtre, suffisamment ambigu pour créer un doute au montage. Les yeux ne brillent pas par eux-mêmes et ne changent pas de forme.

Ambiance premium, silencieuse et psychologique. Faible profondeur de champ, texture du tissu visible, fond de bureau YAWatch complètement flou et sans texte lisible. Aucun effet horrifique, aucune expression menaçante, aucun sourire ajouté, aucune larme, aucun mouvement surnaturel.

Contraintes : exactement une image, photoréalisme cinématographique naturel, une seule poupée, aucun humain, aucun visage humain dans un reflet, yeux non lumineux, pas de LED, pas de métal, pas de circuits, pas de cyberpunk, pas de violet dominant, pas de texte, pas de watermark et pas de logo inventé.
```

Nom cible : `poupee_luna_gros_plan_yeux_mystere_01.png`

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
