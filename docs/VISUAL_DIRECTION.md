# VISUAL DIRECTION — YAWatch-LUNA

## Identité visuelle

## Vérité visuelle saison 1

- Paris réel est le décor principal.
- Luna est la fausse suspecte : l'image peut la rendre mystérieuse, mais pas coupable explicitement.
- Aby est la manipulatrice cachée : ses indices doivent être subtils, souvent lisibles seulement après coup.
- Le père mafieux est la blessure d'enfance : il apparaît comme présence, phrase, photo, ombre, souvenir.
- YAWatch est la conséquence du traumatisme familial, pas un gadget technologique.
- Le présent doit rester lumineux, crédible, habité.
- Le violet/noir/bleu sombre est réservé aux souvenirs, secrets, bascules psychologiques et traces d'Aby ou du père.

### Luna Doll

- Petite poupée brune
- Robe violette velours
- Éclairage doux, chaleureux
- Symbolisme émotionnel fort
- **Jamais robotique**
- Silhouette simple, immédiatement reconnaissable
- Texture tissu, coutures visibles, artisanal

### Luna adulte

- Sérieuse, humaine, protectrice
- Intelligente, émotionnellement fatiguée parfois
- Énergie de fondatrice
- Tenue professionnelle sombre (gris anthracite / noir)
- Cheveux bruns longs
- Tient ou pose Luna Doll dans les scènes clés

### YAWatch Industries

- Tour / bureaux à La Défense
- Architecture premium, verre, hauteur, lumière parisienne
- Tons clairs et réalistes en journée
- Bascule bleu/violet uniquement quand le secret ou le système reprend le dessus
- Ambiance thriller corporate parisien, pas cyberpunk générique

### Iris Workspace / YAWatch Analytics

- Iris Workspace est une interface analytique contemporaine, crédible en 2026.
- Par défaut, Iris n'affiche pas directement une vieille capture caméra au centre du dashboard.
- Iris montre d'abord cartes, trajectoires, corrélations, chronologies, métadonnées, sources disponibles et niveaux de confiance.
- Une image caméra apparaît seulement quand Luna force ou ouvre la source brute.
- Les flux caméra doivent être HD/4K modernes, pas des images d'archive VHS ou vidéosurveillance années 90.
- Les scènes urbaines surveillées doivent contenir des véhicules européens contemporains 2024-2026, mobilier urbain actuel, marquages récents et signal vidéo propre.
- Les voitures peuvent évoquer SUV compacts modernes, berlines électriques récentes et véhicules urbains français actuels, sans marque ni logo lisible.
- En visio, l'interface peut afficher lisiblement `IRIS WORKSPACE`, avec de vraies vignettes photo de participants adultes si la scène prépare l'application.
- Les textes métier doivent rester illisibles ou symboliques, sauf décision explicite de production.

### Aby

- Femme blonde, élégante, froide, stratégique
- Enfant : petite blonde canon APK avec maquette, regard dur
- Indices visuels : reflet, jeton noir, dossier déjà ouvert, archive modifiée, présence hors champ
- Ne jamais la présenter comme méchante évidente avant le final

### Le père

- Homme élégant, mafieux, sombre, calme
- Bureau, dîner, appel nocturne, photo ancienne, porte entrouverte
- Menace contenue : pas d'action graphique, pas de violence spectaculaire

### Paris réel

- La Défense, Quatre Temps, métro/RER, quais de Seine, Marais, cafés, appartements, rues
- Lieux crédibles et vécus
- Pas de carte postale permanente
- Pas de New York

---

## Règle de contraste

> Présent parisien lumineux et réel
> **VS**
> Souvenirs, secrets et manipulations en bleu/violet sombre

Ce contraste doit être visible dans chaque épisode.

---

## Niveau de qualité minimum obligatoire

Le rendu vidéo ne peut **jamais** ressembler à un diaporama bon marché.

Le niveau minimum visé est :

> **Short YouTube cinématique sérieux**
> avec ambiance émotionnelle + cohérence Luna + identité YAWatch + rendu mobile propre

---

## Quality Gate — Checklist obligatoire avant tout upload

Chaque vidéo générée doit passer cette checklist avant d'être considérée prête :

### Format
- [ ] Format vertical 9:16, résolution 1080x1920
- [ ] Durée 20–60 secondes

### Visuel
- [ ] Cadrage cinématique (pas d'images aléatoires sans lien)
- [ ] Mouvement de caméra ou parallaxe (pas d'images 100% statiques)
- [ ] Palette de couleurs cohérente avec le lore
- [ ] Séquence de scènes logique (hook → story → twist → cta)
- [ ] Éclairage directionnel (pas de lumière plate générique)
- [ ] Luna Doll reconnaissable (brune, robe violette, douce, non-robotique)
- [ ] Identité visuelle YAWatch présente
- [ ] Paris réel ou La Défense crédible si scène au présent
- [ ] Luna peut être suspecte, mais pas révélée coupable
- [ ] Aby ne doit pas être révélée manipulatrice avant le final
- [ ] Le père reste une blessure/ombre, pas un méchant caricatural

### Audio
- [ ] Voix claire et cohérente
- [ ] Ambiance sonore présente

### Sous-titres
- [ ] Sous-titres synchronisés
- [ ] Police lisible sur mobile
- [ ] Contraste suffisant

### Lore
- [ ] Luna Doll n'est jamais décrite comme robot, androïde, métal ou circuits
- [ ] Cohérence narrative avec les épisodes précédents
- [ ] Arc narratif respecté
- [ ] Vérité saison 1 respectée : Luna fausse suspecte, Aby cachée, père blessure d'enfance

---

## Instruction développeur — RÈGLE ABSOLUE

> Si le pipeline ne peut pas encore générer des visuels de haute qualité,
> il ne doit **pas** prétendre que le résultat est prêt pour la production.

Le fichier de sortie doit être marqué comme :

```
STATUS: prototype
STATUS: visual_test
STATUS: placeholder
STATUS: not_ready_for_upload
```

**Ne jamais marquer une vidéo comme `production_ready` si elle ne passe pas le Quality Gate complet.**

---

## Éléments visuels interdits

- Images aléatoires sans lien avec le lore
- Images statiques sans aucun mouvement
- Visuels IA génériques sans direction artistique
- Apparence incohérente de Luna Doll entre les scènes
- Visage/style incohérent de Luna adulte
- Absence de direction lumineuse
- Absence de mouvement de caméra
- Absence de style de sous-titres
- Absence de rythme cinématique
- Visuels cyberpunk génériques déconnectés du lore
- Paris remplacé par New York ou ville générique américaine
- Interface 2026 mélangée à des flux caméra ou véhicules visuellement datés années 80/90
- Vieux look VHS/archive quand la scène est censée être une source urbaine actuelle
- Présent constamment violet/noir sans raison narrative
- Aby rendue coupable trop tôt
- Père traité comme gangster cartoon
