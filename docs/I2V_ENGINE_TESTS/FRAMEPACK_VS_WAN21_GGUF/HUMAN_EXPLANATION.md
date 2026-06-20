# Explication humaine — Ce que Codex a fait

## Idee generale

On ne cherche pas a faire une demo technique pour faire joli.

On installe une vraie nouvelle piece moteur dans l'atelier video Windows de YAWatch-LUNA.

Avant:

```text
image fixe + AnimateDiff leger = mouvement limite, souvent fragile
```

Objectif:

```text
image canonique Luna + moteur I2V plus moderne = clip plus vivant, plus stable, plus cinematographique
```

## Ce qui a ete installe

Codex a ajoute deux familles d'outils dans ComfyUI:

- FramePack, pour tester un moteur base HunyuanVideo;
- ComfyUI-GGUF, pour charger Wan2.1 en version GGUF.

En langage simple:

```text
ComfyUI etait l'atelier.
Les custom nodes sont les nouvelles machines.
Les modeles sont les gros moteurs.
Les workflows sont les plans de montage.
```

## Pourquoi Wan GGUF

Wan2.1 complet est trop lourd pour une RTX 4060 Laptop 8 Go.

Le fichier GGUF Q5 est une version compressee du modele, plus adaptee a cette machine.

Ce n'est pas magique:

- il peut etre lent;
- il peut manquer de VRAM;
- il peut echouer;
- mais c'est le bon candidat a tester avant de payer un fournisseur externe.

## Ce que Codex a fait concretement

1. Il a verifie que ComfyUI existe.
2. Il a installe les extensions ComfyUI necessaires.
3. Il a installe les dependances Python des extensions.
4. Il a place le modele Wan Q5 dans le bon dossier:

```text
ComfyUI/models/unet/
```

5. Il a redemarre ComfyUI.
6. Il a interroge `/object_info` pour verifier que ComfyUI voit vraiment le modele.

## Pourquoi c'est important

Un fichier pose sur le disque ne suffit pas.

La vraie preuve, c'est:

```text
UnetLoaderGGUF models: wan2.1-i2v-14b-480p-Q5_K_S.gguf
```

Cela veut dire que ComfyUI a charge les extensions et voit le modele Wan.

## Ce qui n'est pas encore valide

Wan n'a pas encore produit de MP4 YAWatch-LUNA.

Donc le statut n'est pas:

```text
Wan valide
```

Le statut correct est:

```text
MODEL_VISIBLE_IN_COMFYUI
```

La prochaine preuve doit etre un MP4.

## Prochaine etape

Construire ou charger un workflow Wan compatible avec les noeuds installes, puis generer:

```text
PLAN02_LUNA_ADULTE — 5 secondes — 9:16
```

Ensuite seulement:

- regarder le MP4;
- remplir la fiche d'evaluation;
- comparer a FramePack et AnimateDiff;
- decider si Wan devient candidat moteur I2V officiel.

