# ChatGPT Character Panel Prompts — YAWatch-LUNA

> ARCHIVE : la production utilise maintenant le workflow photo par photo décrit dans `docs/CHATGPT_PHOTO_BY_PHOTO_WORKFLOW.md`. Ce document reste disponible comme réserve de prompts groupés.

Objectif : remplir progressivement `CHARACTER_LIBRARY_CHECKLIST.md` et `POSE_LIBRARY_CHECKLIST.md` sans gaspiller les générations.

Workflow :

1. Codex prépare un prompt de panel.
2. Ludovic colle le prompt dans ChatGPT.
3. Ludovic télécharge les images générées.
4. Codex récupère dans `Downloads`, découpe, renomme, classe.
5. Codex met à jour les checklists et pousse sur GitHub.

Règle générale : demander des planches/panels cohérents, mais garder des cellules séparables. Si ChatGPT donne une planche non découpée, Codex la découpera.

---

## Prompt Global A Coller Avant Chaque Panel

```text
Tu dois générer une planche de références personnage pour YAWatch-LUNA.

Style général :
- thriller émotionnel psychologique premium
- réalisme cinématographique
- Paris contemporain, La Défense, bureaux, appartements
- lumière naturelle pour le présent
- violet/bleu sombre seulement pour les souvenirs, secrets ou bascules
- pas de cyberpunk générique
- pas de New York
- pas de texte lisible
- pas de logo inventé
- pas de watermark
- chaque image doit être exploitable comme photo de production

Format souhaité :
- planche propre avec plusieurs vignettes séparées
- chaque vignette doit cadrer le personnage clairement
- cohérence forte du visage, âge, cheveux, vêtements et style
- les émotions doivent être subtiles, pas théâtrales
- pas d’expression caricaturale
```

---

## Bloc 1 — Luna Adulte / Teaser S01E00

Priorité : critique.

Checklist ciblée :

- `neutral` propre 9:16
- `worried`
- `protective` avec Luna Doll
- `looking_out_window`
- `office_desk`
- `looking_at_photo`

### Prompt ChatGPT

```text
Génère une planche de 6 images cinématographiques cohérentes du même personnage : Luna adulte, fondatrice de YAWatch Industries.

Important : Luna est la fausse suspecte de la saison 1. Elle doit sembler mystérieuse, fatiguée, peut-être coupable, mais jamais mauvaise.

Description personnage :
- femme humaine de 30 à 35 ans
- cheveux bruns longs légèrement ondulés
- peau méditerranéenne légèrement hâlée
- regard brun profond, empathique mais insomniaque
- tenue professionnelle sobre : blazer noir ou anthracite, chemisier simple, élégance discrète
- pas de style super-héroïne
- pas d’arme
- pas de pose glamour
- pas de sourire publicitaire

Décor :
- Paris réel / La Défense
- bureaux premium YAWatch
- verre, lumière parisienne, skyline de La Défense ou Paris en fond
- présent lumineux ou nuit réaliste
- pas de cyberpunk
- pas de New York

Créer 6 vignettes séparées :

1. NEUTRAL 9:16
Portrait vertical propre de Luna face caméra, expression neutre, fond bureau clair à La Défense, lumière naturelle, regard calme.

2. WORRIED
Luna adulte inquiète, regard qui fuit légèrement, fatigue insomniaque, bureau YAWatch de nuit, Paris flou derrière les vitres.

3. PROTECTIVE WITH LUNA DOLL
Luna tient une petite poupée artisanale brune à robe violette dans ses mains, geste protecteur, émotion contenue, lumière douce.

4. LOOKING OUT WINDOW
Luna de profil ou de dos, regardant Paris / La Défense par une grande fenêtre, solitude, nuit réaliste, reflets sur la vitre.

5. OFFICE DESK
Luna assise à son bureau, dossier fermé, ordinateur sobre, Luna Doll visible sur le bureau, atmosphère de contrôle et secret.

6. LOOKING AT PHOTO
Luna regarde une photo familiale retournée ou presque retournée sur son bureau. On ne voit pas clairement la photo. Elle semble troublée.

Contraintes :
- même visage sur toutes les vignettes
- même style vestimentaire
- émotions subtiles
- format réaliste premium
- pas de texte lisible
- pas de watermark
- pas de logo inventé
```

---

## Bloc 2 — Luna Doll / États Manquants

Checklist ciblée :

- gros plan yeux mystère
- tenue dans les mains de Luna

### Prompt ChatGPT

```text
Génère une planche de 4 images cinématographiques de Luna Doll, petite poupée artisanale brune à robe violette.

Règle absolue :
- ce n’est PAS un robot
- pas de métal
- pas de circuits
- pas de LED
- pas de visage numérique
- pas d’horreur

Description :
- petite poupée en tissu d’environ 20 cm
- cheveux bruns courts
- robe violette velours légèrement usée
- yeux sombres brodés ou boutons doux
- présence émotionnelle, mélancolique, mystérieuse

Créer 4 vignettes :

1. Gros plan sur les yeux de la poupée, lumière douce, mystère.
2. Luna Doll tenue dans les mains d’une femme adulte, cadrage mains + poupée uniquement.
3. Luna Doll posée sur bureau YAWatch, Paris flou derrière, contraste douceur / entreprise.
4. Luna Doll près d’une photo familiale retournée, ambiance de secret.

Style réaliste cinématographique premium, pas de texte, pas de watermark.
```

---

## Bloc 3 — Aby Adulte / EP02

Checklist ciblée :

- portrait face 9:16 neutral froid
- suspicious
- determined
- vulnerable
- standing
- office_desk

### Prompt ChatGPT

```text
Génère une planche de 6 images cinématographiques cohérentes du même personnage : Aby adulte.

Important : Aby est la manipulatrice cachée de la saison 1, mais elle ne doit jamais ressembler à une méchante évidente. Elle doit être froide, élégante, intelligente, moralement ambiguë.

Description personnage :
- femme humaine de 28 à 32 ans
- blonde, cheveux coiffés avec précision ou attachés élégamment
- regard sombre, stratégique, calme
- tailleur noir ou anthracite
- bijoux discrets mais coûteux
- présence dominante mais contenue
- pas de sourire maléfique
- pas de posture de méchante cartoon

Décor :
- bureaux YAWatch à La Défense
- vitres, reflets, dossiers, lumière froide mais réaliste
- Paris réel, pas cyberpunk

Créer 6 vignettes :

1. NEUTRAL COLD 9:16
Portrait vertical face caméra, expression froide et neutre, bureau YAWatch clair mais tendu.

2. SUSPICIOUS
Aby regarde légèrement de côté, comme si elle savait quelque chose, reflet dans une vitre.

3. DETERMINED
Aby debout, bras croisés, posture contrôlée, décision froide.

4. VULNERABLE
Aby seule, expression très légèrement blessée, émotion retenue, pas de larmes dramatiques.

5. OFFICE DESK
Aby assise à un bureau avec un dossier fermé, main proche d’un jeton noir, aucun texte lisible.

6. LOOKING THROUGH GLASS
Aby vue à travers une vitre/reflet, présence ambiguë, indice qu’elle observe sans être vue.

Contraintes :
- même visage sur toutes les images
- réalisme premium
- émotions subtiles
- pas de texte
- pas de watermark
```

---

## Bloc 4 — Aby Enfant / Maquette Et Jeton Noir

Note sécurité : enfant entièrement habillée, contexte non sexualisé, pas de violence graphique.

Checklist ciblée :

- main posant le jeton noir
- regard de biais vers maquette
- sitting contrôle maquette angle alternatif

### Prompt ChatGPT

```text
Génère une planche de 4 images cinématographiques cohérentes d’Aby enfant.

Important canon :
- Aby enfant est une petite fille blonde
- elle est associée à une maquette de ville
- elle est calme, intelligente, stratégique
- elle n’est pas Luna enfant
- elle ne doit pas être effrayante comme un film d’horreur

Contexte sûr :
- enfant entièrement habillée
- chambre d’enfant réaliste
- aucune violence
- aucune sexualisation
- émotion subtile

Créer 4 vignettes :

1. Aby enfant assise devant une maquette de ville miniature, regard concentré et stratégique.
2. Gros plan sur une petite main posant un jeton noir brillant près des maisons miniatures, visage hors champ.
3. Aby enfant regarde de biais vers la maquette, expression calme, presque trop lucide pour son âge.
4. Maquette miniature avec lumières chaudes, jeton noir au premier plan, Aby enfant floue en arrière-plan.

Style réaliste premium, lumière de chambre douce, tension psychologique subtile, pas de texte, pas de watermark.
```

---

## Bloc 5 — Mère De Luna / Personnage Manquant

Checklist ciblée :

- worried
- protective
- vulnerable
- looking_out_window
- seule en appartement lumineux mais froid

### Prompt ChatGPT

```text
Génère une planche de 6 images cinématographiques cohérentes du même personnage : la mère de Luna et Aby.

Description personnage :
- femme adulte élégante, 40 à 50 ans
- brune ou châtain foncé
- regard doux, inquiet, fatigué
- élégance parisienne discrète
- vêtements sobres : beige, noir, crème, manteau ou chemisier
- elle semble porter un secret familial

Décor :
- appartement parisien lumineux mais froid
- cuisine ou salon élégant
- fenêtres sur Paris
- pas de luxe ostentatoire
- pas de New York

Créer 6 vignettes :

1. NEUTRAL
Portrait vertical sobre, regard calme mais triste.

2. WORRIED
Elle regarde hors champ, inquiétude contenue.

3. PROTECTIVE
Main sur un dossier ou une photo familiale, comme si elle voulait protéger quelqu’un.

4. VULNERABLE
Assise seule dans un appartement lumineux, silence lourd.

5. LOOKING OUT WINDOW
De profil, regarde Paris par la fenêtre.

6. HIDDEN SECRET
Elle tient une photo ou une enveloppe fermée, sans texte lisible.

Style réaliste premium, émotion retenue, pas de texte, pas de watermark.
```

---

## Bloc 6 — Malik Complément EP03

Checklist ciblée :

- neutral propre 9:16 sans violet dominant
- phone_call / téléphone ignoré
- walking rue parisienne

### Prompt ChatGPT

```text
Génère une planche de 5 images cinématographiques cohérentes du même personnage : Malik adulte.

Description personnage :
- homme noir adulte, 30 à 45 ans
- regard fatigué, retenu, humain
- vêtements sobres, veste ou pull sombre
- émotion contenue, pas de colère spectaculaire
- personnage blessé mais digne

Décor :
- appartement parisien réaliste
- rue parisienne calme
- fenêtre de nuit
- lumière naturelle ou nocturne réaliste
- éviter violet dominant

Créer 5 vignettes :

1. NEUTRAL 9:16
Portrait vertical propre, visage calme, lumière naturelle, pas de dominante violette.

2. PHONE IGNORED
Malik assis dans son appartement, téléphone posé sur la table, notification ignorée, regard absent.

3. PHONE CALL
Malik téléphone à l’oreille ou tient son téléphone sans parler, tension intérieure.

4. WALKING PARIS STREET
Malik marche seul dans une rue parisienne, fin de journée, solitude.

5. VULNERABLE WINDOW
Malik près d’une fenêtre de nuit, regard fatigué, silence.

Style réaliste premium, émotion retenue, pas de texte, pas de watermark.
```

---

## Ordre Recommandé

1. Bloc 1 — Luna adulte
2. Bloc 3 — Aby adulte
3. Bloc 5 — Mère
4. Bloc 4 — Aby enfant
5. Bloc 2 — Luna Doll
6. Bloc 6 — Malik complément

Après chaque téléchargement, Codex classe les images et met à jour :

- `docs/CHARACTER_LIBRARY_CHECKLIST.md`
- `docs/POSE_LIBRARY_CHECKLIST.md`
- `assets/luna_stories_assets/catalogue_assets_luna_stories.csv`
- GitHub
