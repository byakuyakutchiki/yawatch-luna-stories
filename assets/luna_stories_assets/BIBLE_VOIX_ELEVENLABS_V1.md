# Bible Voix ElevenLabs - YAWatch Luna Stories V1

## Objectif

Garder des voix coherentes episode apres episode, sans perdre du temps a refaire les memes tests.

Regle principale : on choisit peu de voix, on les documente, puis on ne change plus sauf probleme evident.

## Organisation Des Fichiers Audio

Creer cette structure quand les voix seront generees :

```text
audio/
  00_tests_voix/
  01_voix_canon/
  episodes/
    EP01_LA_VILLE_DANS_LA_CHAMBRE/
    EP02_ABY_AVAIT_DEJA_COMPRIS/
    EP03_L_HOMME_QUI_NE_PARLAIT_PLUS/
```

Convention de nommage :

```text
EP01_NARRATEUR_v01.wav
EP01_LUNA_ENFANT_phrase01_v01.wav
EP01_ABY_ENFANT_phrase01_v01.wav
EP02_ABY_ADULTE_phrase01_v01.wav
EP03_MALIK_phrase01_v01.wav
```

Quand une voix est validee :

```text
CANON_NARRATEUR_voix_nom-elevenlabs_reglages.txt
CANON_LUNA_ADULTE_voix_nom-elevenlabs_reglages.txt
CANON_ABY_ADULTE_voix_nom-elevenlabs_reglages.txt
```

## Voix Prioritaires

Pour les 3 premiers episodes, ne pas tout faire tout de suite. Priorite :

1. Narrateur principal
2. Luna enfant
3. Aby enfant
4. Aby adulte
5. Malik adulte

Les autres voix peuvent attendre :

- Luna adulte
- Pere de Luna
- Mere de Luna
- Mere de Malik
- Pere de Malik

## Direction Generale

La serie doit sonner comme un secret raconte a voix basse.

Eviter :

- voix de bande-annonce trop grave
- voix de dessin anime
- voix trop theatrale
- enfants qui parlent trop longtemps
- cris ou melodrame

Chercher :

- intimite
- retenue
- mystere
- emotion contenue
- phrases courtes
- silences

## Reglages De Depart ElevenLabs

Pour tester :

- Stability : 60 a 75
- Similarity : 70 a 85
- Style exaggeration : 10 a 25
- Speaker boost : active si la voix manque de presence

Si la voix est trop plate :

- baisser un peu Stability
- monter legerement Style

Si la voix est trop dramatique :

- monter Stability
- baisser Style

## Personnages

### Narrateur Principal

Role : porter la serie, raconter le mystere et l emotion.

Voix :

- adulte
- calme
- grave douce
- intime
- pas trop masculine agressive
- pas trop publicitaire

Phrase test :

```text
Avant de creer Luna, il y avait une petite fille qui construisait une ville pour ne plus se sentir seule.
```

Consigne ElevenLabs :

```text
Voix off cinematographique intime, douce et grave, emotion contenue, rythme lent, mystere discret, comme si une verite importante etait racontee a voix basse. Pas de ton publicitaire.
```

### Luna Enfant

Role : origine emotionnelle, solitude, refuge.

Voix :

- enfantine mais naturelle
- douce
- fragile
- reveuse
- pas cartoon
- phrases tres courtes

Phrase test :

```text
Dans ma ville, personne ne dort avec le coeur lourd.
```

Consigne ElevenLabs :

```text
Petite voix douce et naturelle, fragile mais pas triste de facon exageree, enfant reveuse, phrase dite lentement comme un secret. Pas de voix de dessin anime.
```

### Aby Enfant

Role : enfant strategique, lucide trop tot.

Canon visuel : petite blonde APK avec la maquette.

Voix :

- enfantine
- calme
- intelligente
- presque trop posee pour son age
- pas mechante, mais troublante

Phrase test :

```text
Et qui decide qui a le droit d entrer ?
```

Consigne ElevenLabs :

```text
Petite voix d enfant tres calme, intelligente, froide sans etre mechante, phrase courte, regard strategique, emotion retenue. Elle doit sembler comprendre quelque chose que les adultes ne voient pas.
```

### Aby Adulte

Role : pouvoir, strategie, tension morale.

Voix :

- feminine adulte
- basse
- elegante
- froide mais seduisante
- controle total

Phrase test :

```text
Le monde ne protege pas les doux. Il obeit a ceux qui savent lire les regles.
```

Consigne ElevenLabs :

```text
Voix feminine adulte elegante, calme, froide, strategique, tres controlee. Elle ne crie jamais. Elle parle comme quelqu un qui a deja trois coups d avance.
```

### Malik Adulte

Role : silence, blessure, humanite.

Voix :

- masculine adulte
- grave
- fatiguee
- retenue
- peu de mots

Phrase test :

```text
Ca va. Je suis juste fatigue.
```

Consigne ElevenLabs :

```text
Voix masculine adulte grave, fatiguee, emotion retenue, parle peu, comme quelqu un qui cache sa douleur depuis longtemps. Ton realiste, pas dramatique.
```

### Luna Adulte

Role : promesse, presence, fondatrice.

Voix :

- feminine adulte
- rassurante
- douce
- profonde
- therapeutique sans etre robotique

Phrase test :

```text
Je n ai pas cree Luna pour repondre. Je l ai creee pour rester.
```

Consigne ElevenLabs :

```text
Voix feminine adulte calme, douce, rassurante, profonde, presence presque therapeutique. Emotion contenue, intelligence, chaleur humaine.
```

### Pere De Luna

Role : pouvoir, peur, controle.

Voix :

- masculine adulte
- grave
- calme
- nerveuse sous la surface
- menace controlee

Phrase test :

```text
Dans cette famille, on ne laisse jamais une faiblesse devenir publique.
```

Consigne ElevenLabs :

```text
Voix masculine grave, controlee, autoritaire, menace calme, tension nerveuse sous la surface. Il ne crie pas. Il fait peur parce qu il garde le controle.
```

### Mere De Luna

Role : elegance, silence, inquietude.

Voix :

- feminine adulte
- douce
- elegante
- fatiguee
- inquietude cachee

Phrase test :

```text
Luna, parfois il vaut mieux ne pas poser certaines questions.
```

Consigne ElevenLabs :

```text
Voix feminine adulte elegante, douce, inquiete sous la surface, parle avec retenue comme quelqu un qui protege un secret depuis longtemps.
```

## Methode De Test

Pour chaque voix :

1. Generer 3 versions de la phrase test.
2. Garder seulement la meilleure.
3. Noter le nom exact de la voix ElevenLabs.
4. Noter les reglages.
5. Mettre le fichier valide dans `audio/01_voix_canon/`.
6. Ne plus changer pour les episodes suivants.

## Plan Pour Les 3 Premiers Episodes

### EP01

Voix necessaires :

- Narrateur
- Luna enfant, une phrase courte
- Aby enfant, phrase finale ou souffle inquietant

### EP02

Voix necessaires :

- Narrateur
- Aby enfant
- Aby adulte, phrase finale possible

### EP03

Voix necessaires :

- Narrateur
- Malik adulte, une ou deux phrases maximum

## Regle D Or

Le narrateur raconte.
Les personnages ne parlent que quand leur voix doit marquer le spectateur.

Moins ils parlent, plus chaque phrase compte.
