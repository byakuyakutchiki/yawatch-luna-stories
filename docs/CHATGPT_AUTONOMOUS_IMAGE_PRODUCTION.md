# CHATGPT - PILOTAGE AUTONOME DES IMAGES - SUSPENDU

> Expérience suspendue le 15 juin 2026 : ChatGPT ne conservait pas correctement la file et mélangeait les personnages. Ne plus utiliser ce protocole. Codex reprend le pilotage photo par photo.

Source de vérité opérationnelle pour produire les images YAWatch-LUNA par lots de cinq.

Dernière mise à jour : 15 juin 2026.

## Mission De ChatGPT

ChatGPT est l'opérateur visuel de la session. Il doit lire ce document, générer exactement une image à la fois, conserver son avancement dans la conversation et contrôler lui-même la cohérence avant de passer à la suivante.

Codex reste responsable de l'audit final, du renommage, du classement et de l'écriture dans GitHub. ChatGPT ne doit jamais prétendre avoir modifié le dépôt.

## Situation De Production

| Livrable | Visuels | Nouveaux personnages requis | Blocage réel |
|---|---:|---|---|
| Teaser 25-30 s | 90-95 % | Aucun | Voix narrateur, mouvement, musique, montage |
| EP01 - La Photo Retournee, format 7 min 30 | 35-45 % | Aucun nouveau personnage | 10 images sources, voix, animation, montage |
| EP02 - Aby Refuse Le Nom, format long | À réévaluer après EP01 | Aucun nouveau personnage | Écriture longue et nouveaux plans |
| EP03 - L'Homme Qui Ne Parlait Plus | 65-75 % | Aucun | Malik propre, téléphone ignoré, interface YAWatch |

Conclusion : ne pas retarder le teaser ou EP01 pour compléter tous les personnages. Le lot actif sert principalement à terminer EP03 et à combler deux plans émotionnels réutilisables.

## Documents À Lire Au Début De La Session

1. Bible personnages :
   https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/docs/CHARACTER_BIBLE.md
2. Direction visuelle :
   https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/docs/VISUAL_DIRECTION.md
3. État des personnages :
   https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/docs/CHARACTER_LIBRARY_CHECKLIST.md
4. Épisodes 1 à 3 :
   https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/docs/EP01_EP03_REVISED_SPINE.md

## Protocole Obligatoire

1. Commencer par `BATCH-001 / IMAGE 1`.
2. Générer exactement une image, jamais une planche.
3. Inspecter l'image générée avant de répondre.
4. Afficher après chaque génération : identifiant, nom cible et résultat du contrôle.
5. Attendre que l'utilisateur écrive `fait`, `continue` ou équivalent.
6. Passer automatiquement à l'image suivante sans demander que le prompt soit recopié.
7. Si l'image est incohérente, corriger cette image avant de changer de numéro.
8. Après l'image 5, arrêter la génération et produire l'audit de lot prévu plus bas.

ChatGPT conserve dans la conversation ce tableau :

| ID | Nom cible | État |
|---|---|---|
| B01-01 | `malik_adulte_neutral_9x16_01.png` | À faire |
| B01-02 | `malik_adulte_telephone_ignore_01.png` | À faire |
| B01-03 | `interface_yawatch_phrase_muet_01.png` | À faire |
| B01-04 | `luna_adulte_sad_9x16_01.png` | À faire |
| B01-05 | `aby_enfant_regard_biais_maquette_01.png` | À faire |

États autorisés : `À FAIRE`, `GÉNÉRÉ`, `À CORRIGER`, `VALIDÉ SESSION`.

## Règles Absolues De Continuité

- Luna adulte : brune, environ 32 ans. Référence unique : `luna_adulte_neutral_9x16_01.png`.
- Aby adulte : blonde, chignon haut. Ne jamais la remplacer par Luna.
- Luna enfant : petite brune d'environ 8 ans.
- Aby enfant : petite blonde, univers de maquette. Ne jamais la remplacer par Luna enfant.
- Malik : homme noir adulte, même identité que la référence indiquée dans les prompts.
- Luna Doll : poupée textile brune à robe violette. Jamais blonde, jamais en porcelaine, jamais robotique.
- Paris et La Défense restent lumineux et réalistes dans la vie courante.
- Les tenues sont sobres, couvrantes, crédibles et non sexualisées.
- Aucun texte généré n'est considéré fiable. Les écrans doivent rester sans texte lisible afin que Codex ajoute le texte au montage.

## BATCH-001 - Cinq Images Prioritaires

### B01-01 - Malik Neutre 9:16

Référence d'identité :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/06_personnage_masculin_noir/personnage_masculin_noir_portrait_trois_quarts_calme_01.png

Prompt de génération :

```text
Génère exactement UNE photo verticale 9:16 de Malik adulte. Conserve strictement le même homme noir, le même âge d'environ 32 à 38 ans, la même structure du visage, la même peau, les mêmes cheveux courts et la même barbe discrète que la référence.

Portrait de référence neutre, plan poitrine, face caméra, expression calme et naturelle. Malik porte un pull fin gris anthracite ou une chemise bleu nuit opaque et fermée. Lumière naturelle claire venant d'une fenêtre d'appartement parisien en journée. Fond sobre légèrement flou, couleurs réalistes, aucune lumière violette.

Une seule personne, aucun téléphone, aucun objet symbolique, aucun sourire appuyé, aucune détresse, aucun texte, aucun watermark. Photoréalisme cinématographique naturel.
```

Nom cible : `malik_adulte_neutral_9x16_01.png`

### B01-02 - Malik Ignore Le Téléphone

Références :

- identité :
  https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/06_personnage_masculin_noir/personnage_masculin_noir_portrait_trois_quarts_calme_01.png
- appartement et émotion :
  https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/06_personnage_masculin_noir/personnage_masculin_noir_scene_salon_seul_01.png

```text
Génère exactement UNE photo verticale 9:16 de Malik adulte dans son salon parisien en début de soirée. Conserve strictement son identité canonique.

Malik est assis sur le canapé, entièrement habillé, légèrement en retrait. Un smartphone est posé face visible sur la table basse au premier plan. L'écran émet une faible lumière de notification mais ne contient aucun texte, aucun nom, aucune icône lisible. Malik regarde ailleurs et choisit silencieusement de ne pas répondre.

Ambiance humaine et réaliste, tristesse contenue, aucune pose théâtrale. Les deux mains de Malik sont visibles et ne touchent pas le téléphone. Appartement clair avec la lumière bleue naturelle du soir, sans violet dominant.

Une seule personne, un seul téléphone, anatomie naturelle, aucun texte, aucun watermark, aucun logo inventé.
```

Nom cible : `malik_adulte_telephone_ignore_01.png`

### B01-03 - Interface YAWatch Pour Surimpression

Référence de style :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/docs/VISUAL_DIRECTION.md

```text
Génère exactement UNE image verticale 9:16 montrant un écran d'ordinateur sobre dans l'univers YAWatch Industries.

L'écran affiche une interface premium, calme et minimale : fond gris très sombre, quelques lignes fines gris clair, un petit indicateur circulaire discret et une zone centrale vide destinée à recevoir une phrase ajoutée plus tard au montage. Aucun texte, aucune lettre, aucun chiffre, aucun faux mot et aucun visage.

L'écran se trouve dans un appartement parisien réaliste de nuit, avec une très légère réflexion de fenêtre. Cadrage rapproché, profondeur de champ faible, aucune personne visible. L'interface doit sembler crédible et utilitaire, pas futuriste.

Pas de cyberpunk, pas d'hologramme, pas de violet dominant, pas de code informatique spectaculaire, pas de logo inventé, pas de watermark.
```

Nom cible : `interface_yawatch_phrase_muet_01.png`

### B01-04 - Luna Adulte Tristesse Contenue

Référence canonique :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png

```text
Génère exactement UNE photo verticale 9:16 de Luna adulte. Conserve strictement le même visage, le même âge d'environ 32 ans, les mêmes longs cheveux bruns ondulés, les mêmes yeux, le même nez, les mêmes lèvres et la même structure du visage que la référence canonique.

Portrait plan poitrine dans son bureau lumineux de La Défense en fin de journée. Luna regarde légèrement hors champ. Elle exprime une tristesse profonde mais parfaitement contenue : regard plus lourd, respiration calme, lèvres détendues. Aucune larme, aucune grimace et aucune main sur le visage.

Tenue professionnelle noire couvrante avec col fermé, sans décolleté. Paris et La Défense restent visibles en flou derrière elle. Lumière naturelle douce, couleurs réalistes, pas de violet dominant.

Une seule femme adulte, aucun autre personnage, aucune poupée, aucun texte, aucun watermark.
```

Nom cible : `luna_adulte_sad_9x16_01.png`

### B01-05 - Aby Enfant Observe La Maquette

Référence canonique d'Aby enfant et de la maquette :
https://github.com/byakuyakutchiki/yawatch-luna-stories/blob/master/assets/luna_stories_assets/03_aby/aby_enfant_canon_apk_maquette_ville_01.png

```text
Génère exactement UNE photo verticale 9:16 d'une scène familiale saine et non sensible avec Aby enfant, environ 8 ans. Conserve strictement la même petite fille blonde, le même visage enfantin, la même coiffure, la même tenue couvrante et la même maquette de ville que la référence.

Aby est assise normalement devant la maquette. Elle ne regarde pas la caméra : elle observe une rue miniature de biais avec une attention calme et stratégique, comme si elle anticipait le prochain mouvement. Ses deux mains sont visibles et reposent naturellement près de la maquette sans déplacer de pièce.

Lumière naturelle douce de journée, chambre ou espace de jeu réaliste et rassurant. Aucun adulte, aucune menace, aucune peur, aucune violence, aucune poupée, aucune pose adulte et aucun maquillage.

Enfant entièrement habillée, anatomie naturelle, photoréalisme cinématographique doux, pas de texte, pas de watermark, pas de cyberpunk et pas de violet dominant.
```

Nom cible : `aby_enfant_regard_biais_maquette_01.png`

## Contrôle Après Chaque Image

Avant de déclarer `VALIDÉ SESSION`, vérifier :

- identité correcte ;
- bon personnage, sans confusion Luna/Aby ;
- âge apparent correct ;
- tenue correcte et couvrante ;
- nombre de personnages et d'objets conforme ;
- mains et doigts cohérents ;
- format vertical 9:16 ;
- aucun texte ou watermark ;
- lumière et décor cohérents ;
- absence de dérive cyberpunk, glamour ou horrifique.

Après chaque image, répondre sous cette forme :

```text
BATCH-001 — IMAGE X/5
Nom cible : ...
Contrôle : VALIDÉ SESSION / À CORRIGER
Raison : une phrase maximum.
Prochaine étape : télécharge l'image puis écris « continue ».
```

## Audit Obligatoire Après Cinq Images

Après B01-05, ne plus générer. Afficher :

```text
AUDIT BATCH-001

| ID | Nom cible | Identité | Mains/objets | Format | Verdict |
|---|---|---|---|---|---|
| B01-01 | ... | OK/NON | OK/NON | OK/NON | VALIDÉ/REFAIRE |
...

Lot prêt pour Codex : OUI/NON
Images à refaire : liste ou AUCUNE
```

Rappeler ensuite à l'utilisateur de laisser tous les fichiers dans Téléchargements et de dire à Codex : `lot 1 terminé`.

## Lots Suivants

Ne pas commencer un second lot sans mise à jour de ce document par Codex. Les prochains lots possibles concernent les émotions secondaires et la saison 2; ils ne doivent pas ralentir le teaser ni EP01.
