# Production Stack - Roles Des Outils

## Decision

Le stack actuel suffit pour produire un teaser premium.

Il ne faut pas ajouter 20 API. Il faut clarifier les roles et ajouter une seule brique manquante : **image-to-video cinematographique**.

## Roles

### ChatGPT

Role :

- direction artistique ;
- structure emotionnelle ;
- prompts ;
- coherence ;
- analyse des retours ;
- decisions narratives rapides.

Utilisation :

- poser la question centrale ;
- challenger les episodes ;
- transformer une idee vague en sequence exploitable.

### Claude

Role :

- ecriture longue ;
- scenes dramatiques ;
- dialogues plus litteraires ;
- variations de voix off ;
- tension psychologique.

Utilisation :

- versions longues des scenes ;
- monologues ;
- dialogues Luna / Aby / pere.

### Codex

Role :

- organisation du repo ;
- pipeline ;
- nomenclature fichiers ;
- integration des assets ;
- generation de docs de production ;
- automatisation video/audio/sous-titres ;
- controle qualite.

Utilisation :

- transformer les decisions creatives en fichiers ;
- maintenir GitHub comme source de verite ;
- preparer les manifests de production.

### ElevenLabs

Role :

- narrateur ;
- voix personnage ;
- voix enfant courte ;
- phrases cultes ;
- emotion audio.

Utilisation :

- voix longues uniquement pour narrateur ;
- personnages en phrases courtes ;
- garder les reglages canon.

### Simli

Role :

- avatar parlant ;
- visage anime court ;
- plan dialogue ponctuel.

Utilisation :

- uniquement pour une phrase forte ou un plan de personnage face camera ;
- ne pas l'utiliser pour tout, sinon le rendu deviendra artificiel.

### Images IA Deja Produites

Role :

- base visuelle ;
- personnages canon ;
- decors ;
- reference de style ;
- support image-to-video.

Utilisation :

- ne pas regénérer sans raison ;
- partir des images classees dans `assets/luna_stories_assets/`.

## Brique Manquante

### Image-To-Video Cinematique

Besoin :

- camera push-in ;
- travelling lent ;
- micro-expression ;
- respiration ;
- regard ;
- pluie / lumiere / reflet ;
- cheveux ou vetements subtilement animes.

Objectif :

Transformer les images fixes en plans de 3 a 5 secondes.

Regle :

Une seule bonne solution image-to-video suffit pour commencer.

## Workflow Cible

```text
Scenario / teaser
  -> selection assets fixes
  -> voix ElevenLabs
  -> generation clips image-to-video 3-5s
  -> montage Codex / FFmpeg / MoviePy
  -> sous-titres
  -> sound design
  -> export Shorts 1080x1920
```

## Priorite

1. Produire S01E00 teaser.
2. Tester 5 plans image-to-video.
3. Garder l'outil qui respecte le mieux les visages et l'ambiance.
4. Ne pas chercher le lipsync sauf phrase culte.

## Regle Anti-Dispersion

Si un nouvel outil n'aide pas directement le teaser S01E00, on l'ignore pour l'instant.
