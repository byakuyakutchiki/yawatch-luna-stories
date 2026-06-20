"""Module I2V_ENGINE — backend de génération vidéo (EXPÉRIMENTAL).

Ce module pilote ComfyUI/AnimateDiff pour produire des clips MP4.
Il est l'exécutant du flux de gouvernance YAWatch-LUNA :

    bibliothèques → rôle métier IA → CE BACKEND → Quality Gate → validation humaine

Il ne modifie aucun composant validé du pipeline. Tout clip produit reste un
PROTOTYPE_TECHNIQUE jusqu'à validation explicite via le Quality Gate (VM Linux)
puis approbation humaine de Ludovic.

Ce backend deviendra le cœur de l'application bureau YAWatch Video Factory.
"""
