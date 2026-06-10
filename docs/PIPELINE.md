# PIPELINE — YAWatch-LUNA

## Pipeline narratif

```
Lore
  → Génération d'histoires
    → Génération de scripts
      → Traduction (Phase 4)
        → Génération de prompts images
          → Génération de voix (TTS)
            → Animation image-to-video courte
            → Génération de sous-titres
              → Rendu vidéo
                → Thumbnail
                  → Upload YouTube (Phase 4)
```

---

## Pipeline technique

```
lore_manager.py          ← état persistant de l'univers
  → story_generator.py   ← histoire cohérente avec le lore
    → script_generator.py ← script HOOK/STORY/TWIST/CTA
      → image_prompt_generator.py ← 4 prompts SD par épisode
        → voice_generator.py      ← TTS OpenAI (nova)
          → subtitle_generator.py ← SRT synchronisé
            → video_builder.py    ← assembly MoviePy ou manifest FFmpeg
```

---

## Commandes

```bash
# Un épisode aléatoire
python -m app.main

# Type spécifique
python -m app.main --type emotionnelle
python -m app.main --type mysterieuse
python -m app.main --type inquietante
python -m app.main --type protection
python -m app.main --type philosophique

# Batch hebdomadaire
python -m app.main --batch 7

# État de l'univers
python -m app.main --status

# Logs détaillés
python -m app.main --verbose
```

---

## Ce que produit chaque épisode

| Fichier | Format | Description |
|---|---|---|
| `content/stories/story_*.json` | JSON | Histoire structurée avec lore |
| `content/scripts/luna_script_*.txt` | TXT | Script HOOK/STORY/TWIST/CTA |
| `content/images/prompts_*.json` | JSON | 4 prompts SD (positive + negative) |
| `content/audio/luna_*.mp3` | MP3 | Audio TTS voix nova |
| `content/subtitles/subs_*.srt` | SRT | Sous-titres synchronisés |
| `content/videos/luna_*_manifest.json` | JSON | Manifest FFmpeg pour assembly |
| `content/lore/universe_state.json` | JSON | État persistant de l'univers |

---

## Statuts de sortie vidéo

```
STATUS: prototype           ← pipeline fonctionnel, visuels non générés
STATUS: visual_test         ← images placeholder, audio réel
STATUS: production_ready    ← passe le Quality Gate complet (voir VISUAL_DIRECTION.md)
```

**Règle : ne jamais marquer `production_ready` sans passer le Quality Gate.**

---

## Phases d'évolution

| Phase | Objectif | Statut |
|---|---|---|
| 1 | Scripts + prompts + audio + SRT | ✅ Fait |
| 2 | Génération images réelles (SDXL/Replicate) | 🔜 |
| 3 | Animation image-to-video premium | 🔜 |
| 4 | Assembly vidéo automatique (MoviePy/FFmpeg) | 🔜 |
| 5 | Traduction multilingue (OpenAI) | 🔜 |
| 6 | Upload YouTube automatique | 🔜 |
| 7 | Batch hebdomadaire + scheduler cron | 🔜 |
| 8 | Intégration application Luna | 🔜 |
