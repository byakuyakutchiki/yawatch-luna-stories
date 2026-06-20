# FramePack vs Wan2.1 GGUF — Test Kit 001

Date: 2026-06-20
Decision produit: qualite > vitesse
Machine cible: Windows, RTX 4060 Laptop, 8 Go VRAM

## Objectif

Comparer deux moteurs I2V locaux sur le meme plan YAWatch-LUNA:

- FramePack / HunyuanVideo via ComfyUI-FramePackWrapper
- Wan2.1 I2V 14B 480P GGUF via ComfyUI-GGUF

Le test ne sert pas a produire un teaser. Il sert a choisir le prochain candidat du slot `I2V_ENGINE`.

## Plan de test

Plan unique:

- `PLAN02_LUNA_ADULTE`
- meme image source canonique
- meme prompt realisateur
- meme seed quand le workflow le permet
- duree cible: 5 secondes
- sortie finale attendue: MP4 vertical 9:16

## Regle de gouvernance

Le test peut etre execute hors pipeline episode, mais il doit respecter la logique:

```text
bibliotheques -> MotionDirector -> job verrouille -> moteur I2V -> Quality Gate -> validation Ludovic
```

Tant qu'un moteur n'a pas produit un MP4 regarde et note, il reste `CANDIDATE`, jamais `VALIDATED`.

## Fichiers du kit

- `MODEL_MANIFEST.md`: sources, modeles, chemins ComfyUI, priorites.
- `PROCEDURE_WINDOWS.md`: ordre d'installation et de test.
- `EVALUATION_SHEET.md`: grille de notation Ludovic / QA.
- `GOVERNANCE_RULES.md`: regles bloquantes avant de declarer un resultat exploitable.
- `scripts/install_custom_nodes.ps1`: installe les custom nodes.
- `scripts/download_models.ps1`: telecharge les modeles via `huggingface-cli`.
- `scripts/verify_install.ps1`: verifie fichiers et noeuds attendus.
- `candidate_workflows/`: workflows candidats a valider dans ComfyUI avant usage.

## Important

Les workflows fournis sont des candidats, pas une garantie universelle. Les noms de noeuds ComfyUI changent selon les versions de `ComfyUI-FramePackWrapper` et `ComfyUI-GGUF`.

Regle obligatoire: si un workflow ne charge pas dans ComfyUI ou si `/object_info` ne confirme pas les noeuds attendus, on arrete et on adapte le workflow. On ne declare jamais un MP4 valide sur une execution partiellement degradee.

