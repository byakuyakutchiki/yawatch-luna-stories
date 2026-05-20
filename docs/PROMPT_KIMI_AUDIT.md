# Prompt optimisé pour Kimi — Audit critique final

Copier-coller exactement ce prompt dans Kimi :

---

Tu es un expert en audit de code Python et en architecture logicielle.

Je travaille sur **YAWatch Luna Stories**, un pipeline Python de génération automatique de Shorts YouTube autour d'un univers fictionnel (YAWatch Industries, Luna adulte, Luna Doll — petite poupée brune robe violette, non-robotique).

## Contexte du projet

- **VM Linux**, RAM limitée, Python 3.11
- Pipeline : génération narrative → script → prompts images → TTS → sous-titres → vidéo
- Modules principaux : `lore_manager.py`, `story_generator.py`, `script_generator.py`, `visual_consistency_manager.py`, `prompt_style_manager.py`, `image_prompt_generator.py`, `voice_generator.py`, `subtitle_generator.py`, `video_builder.py`

## Ce que j'ai déjà corrigé

1. Ajout de `load_json()` dans `utils.py` (absent du code original)
2. Suppression de l'import circulaire dans `script_generator.py`
3. Ancrage des chemins absolus via `PROJECT_ROOT`
4. Refactorisation de `lore_manager.py` avec arcs narratifs progressifs
5. Création de `visual_consistency_manager.py` et `prompt_style_manager.py`

## Ta mission

Audite le code fourni et identifie :

### 1. Erreurs critiques restantes
Pour chaque erreur : `fichier:ligne`, impact (🔴 Critique / 🟡 Moyen / 🟢 Bas), correction avec exemple de code.

### 2. Risques VM Linux
- Fuites mémoire lors de traitements batch (--batch N)
- Opérations I/O bloquantes sur disque lent
- Gestion des signaux (Ctrl+C propre ?)
- Fichier de log qui grossit sans rotation

### 3. Cohérence narrative
- Est-ce que `mystery_level` peut dépasser les secrets révélés ?
- Les arcs progressent-ils de façon cohérente avec le lore ?
- Y a-t-il des cas où Luna Doll pourrait être décrite comme un robot ?

### 4. Qualité des prompts images
- Les prompts générés par `prompt_style_manager.py` sont-ils exploitables tel quel dans Stable Diffusion XL ?
- Manque-t-il des éléments clés (seeds, samplers, CFG) ?
- Les prompts négatifs sont-ils suffisamment défensifs ?

### 5. 5 améliorations prioritaires
Propose les 5 améliorations les plus impactantes pour transformer ce pipeline en vraie production.

### Format de ta réponse
1. Résumé exécutif (5 lignes max)
2. Tableau des problèmes trouvés
3. Code corrigé pour les 3 problèmes les plus critiques
4. Recommandations priorisées (P1/P2/P3)

---

## Code source à auditer

[Coller ici le contenu des fichiers suivants :]
- `app/lore_manager.py`
- `app/visual_consistency_manager.py`
- `app/prompt_style_manager.py`
- `app/story_generator.py`
- `app/main.py`
- `app/utils.py`
