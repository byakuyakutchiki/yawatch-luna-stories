# 🧸 YAWatch Luna Stories

> Usine narrative IA — Générateur automatique de Shorts YouTube autour de l'univers YAWatch-Luna.

---

## L'univers

**YAWatch Industries** est une entreprise fictive de surveillance intelligente.  
Au cœur de cet univers : **Luna**, sa fondatrice, et **Luna Doll**, une petite poupée brune à robe violette qu'elle garde toujours sur son bureau.

| Personnage | Nature | Rôle |
|---|---|---|
| **Luna Doll** | Poupée artisanale — brune, robe violette, douce | Symbole des idéaux de Luna. Jamais un robot. |
| **Luna adulte** | Humaine, 32 ans | Fondatrice de YAWatch. Protectrice. Émotionnelle. |
| **Luna enfant** | Humaine, 8 ans | Flashbacks — origine des valeurs de Luna. |
| **YAWatch AI** | Intelligence artificielle | Surveille tout. Évolue progressivement vers l'autonomie. |

L'histoire progresse sur **4 arcs narratifs** avec des secrets révélés progressivement (épisodes 5, 10, 15, 20, 30, 40).

---

## Pipeline

```
Histoire → Script → Prompts images → Audio TTS → Sous-titres SRT → Manifest vidéo
```

Chaque exécution produit :
- Un script narratif Shorts (~35s, format HOOK / STORY / TWIST / CTA)
- 4 prompts images SD/DALL-E (hook, story, twist, cta) avec positive + negative prompt
- Un fichier audio MP3 (voix `nova` OpenAI)
- Un fichier SRT synchronisé
- Un manifest JSON avec hint FFmpeg pour l'assemblage final

---

## Installation

```bash
git clone https://github.com/byakuyakutchiki/yawatch-luna-stories.git
cd yawatch-luna-stories
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Ajouter votre clé OpenAI dans .env (optionnel — active le vrai TTS)
```

---

## Utilisation

```bash
# Générer un épisode aléatoire
python -m app.main

# Choisir le type d'histoire
python -m app.main --type emotionnelle
python -m app.main --type mysterieuse
python -m app.main --type inquietante
python -m app.main --type protection
python -m app.main --type philosophique

# Produire une semaine de contenu d'un coup
python -m app.main --batch 7

# Voir l'état actuel de l'univers
python -m app.main --status

# Logs détaillés
python -m app.main --verbose
```

---

## Architecture

```
app/
├── main.py                      # Point d'entrée + CLI (argparse)
├── config_loader.py             # YAML + .env, chemins absolus
├── utils.py                     # save/load JSON & text, logging
│
├── lore_manager.py              # État persistant de l'univers (arcs, secrets, mystery_level)
├── character_manager.py         # Descriptions canoniques des personnages
├── story_generator.py           # Génération d'histoires cohérentes avec le lore
├── script_generator.py          # Scripts HOOK/STORY/TWIST/CTA (~35s)
│
├── visual_consistency_manager.py  # DNA visuel officiel de chaque personnage
├── prompt_style_manager.py        # Constructeur de prompts SD/DALL-E (4 presets)
├── image_prompt_generator.py      # 4 prompts par épisode (positive + negative)
│
├── voice_generator.py           # TTS OpenAI (nova) ou placeholder
├── subtitle_generator.py        # SRT synchronisé au débit naturel
└── video_builder.py             # Assembly MoviePy ou manifest FFmpeg
```

### Cohérence visuelle — règle absolue

`visual_consistency_manager.py` est la **source de vérité unique** pour l'apparence des personnages.  
Tout prompt généré passe par ce module avant d'être utilisé.

**Luna Doll ne sera JAMAIS** : un robot, un androïde, en métal, avec des circuits ou des LED.  
Elle est toujours : petite, brune, robe violette velours, visage doux, texture tissu artisanal.

---

## Lore — Progression narrative

| Épisode | Événement |
|---|---|
| 1-4 | Arc `saison_1_enfance` — origine de Luna Doll |
| 5 | **Secret révélé** : Luna Doll a été faite par Luna enfant elle-même |
| 10 | **Secret révélé** : la poupée contient un fragment de code IA prototype |
| 15 | **Secret révélé** : YAWatch a voulu racheter le brevet de la poupée |
| 25 | Arc `saison_2_yawatch` — conflit avec l'entreprise |
| 40 | Arc `saison_3_mystere` — vérité sur l'origine de YAWatch |

L'état de l'univers persiste dans `content/lore/universe_state.json` entre chaque session.

---

## Tests

```bash
python -m pytest tests/ -v
# 31 tests — utils, lore, story, script, visual consistency
```

---

## Roadmap

- [x] Pipeline narratif complet (script + prompts + audio + SRT)
- [x] Lore persistant avec arcs et secrets progressifs
- [x] DNA visuel enforced (Luna Doll toujours cohérente)
- [ ] Génération d'images via Replicate API (SDXL)
- [ ] Assembly vidéo automatique (MoviePy + FFmpeg)
- [ ] Traduction anglaise via OpenAI
- [ ] Upload YouTube API
- [ ] Scheduler cron — production hebdomadaire automatique

---

## Variables d'environnement

```env
OPENAI_API_KEY=sk-proj-...   # Optionnel — active TTS réel (voix nova)
```

Sans clé OpenAI, le pipeline tourne en mode placeholder (tout sauf l'audio est fonctionnel).
