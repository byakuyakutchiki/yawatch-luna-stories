# YAWATCH-LUNA FACTORY — PLAN DIRECTEUR

> **Document de référence permanent.**
> Ce document prime sur toute conversation, toute suggestion d'agent ou d'IA extérieure.
> Toute modification de ce document nécessite une décision explicite de Ludovic.

**Version :** 1.0  
**Date de verrouillage :** 2026-06-20  
**Décisions fondatrices actées :**
- Kling retiré définitivement de la stratégie cible.
- Architecture I2V agnostique : aucun composant ne dépend d'un fournisseur vidéo particulier.
- L'objectif n'est pas de produire un teaser. L'objectif est de construire l'usine.

---

## PARTIE 1 — VISION FINALE DE L'USINE

### Ce que l'usine produit

YAWatch-LUNA Factory est un système de production vidéo IA capable de fabriquer :

1. **Des teasers** (28-32 secondes, vertical 9:16, Shorts YouTube)
2. **Des épisodes** (7 minutes, vertical 9:16, format série)

Chaque sortie respecte trois garanties non négociables :

- **Cohérence artistique** — chaque plan respecte la vision, les personnages, la grammaire visuelle.
- **Cohérence narrative** — chaque épisode s'inscrit dans le lore vivant de la saison 1.
- **Validation humaine obligatoire** — aucune vidéo ne peut être publiée sans approbation de Ludovic.

### Ce que l'usine n'est pas

- Ce n'est pas un outil de génération automatique de contenu à volume.
- Ce n'est pas un pipeline qui s'exécute sans supervision artistique.
- Ce n'est pas un wrapper autour d'un outil IA particulier.

### La question centrale de la série

> Pourquoi Luna connaît-elle des choses qu'elle ne devrait pas connaître ?

Chaque épisode, chaque plan, chaque décision de production sert cette question.

---

## PARTIE 2 — ARCHITECTURE GLOBALE

### Vue d'ensemble du pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        PIPELINE YAWATCH-LUNA                            │
│                                                                         │
│  PHASE NARRATIVE                          PHASE VIDÉO                   │
│                                                                         │
│  [LORE]                                   [ASSETS CANONIQUES]           │
│     ↓                                            ↓                      │
│  [STORY GENERATOR]                        [I2V_ENGINE]  ← slot abstrait │
│     ↓                                            ↓                      │
│  [SCRIPT GENERATOR]                       [CLIPS MP4]                   │
│     ↓                                            ↓                      │
│  [IMAGE PROMPT GENERATOR]         [AUDIO : voix + musique + SFX]        │
│     ↓                                            ↓                      │
│  [VOICE GENERATOR]                        [FFMPEG ASSEMBLY]             │
│     ↓                                            ↓                      │
│  [SUBTITLE GENERATOR]                     [QUALITY GATE]                │
│                                                  ↓                      │
│                                           [EXPORT MANAGER]              │
│                                                  ↓                      │
│                                     PROTOTYPE → CANDIDAT → VALIDE       │
└─────────────────────────────────────────────────────────────────────────┘
```

### Séparation fondamentale — RÈGLE 0 (inviolable)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  I2V_ENGINE génère du mouvement à partir d'une image fixe.              │
│  FFmpeg assemble des clips existants. FFmpeg ne génère rien.            │
│                                                                         │
│  Cette séparation ne peut jamais être contournée.                       │
│  La confondre a produit le désastre Phase 14.                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## PARTIE 3 — RÔLES IA DE L'USINE

Chaque rôle est une expertise métier codée. Il inspecte un contexte de production et
rend un verdict : `PASS`, `FAIL`, ou `NEEDS_HUMAN`. Un verdict `FAIL` bloque la progression.

| Rôle | Fichier | Responsabilité | Verdict bloquant |
|---|---|---|---|
| **VideoGenerationEngineer** | `app/roles/video_generation_engineer.py` | Valide que les clips viennent d'un vrai outil I2V (pas FFmpeg). Bloque les images placeholder. | Oui |
| **MotionEngineer** | `app/roles/motion_engineer.py` | Valide le ratio Ken Burns (≤ 20%), les paramètres zoompan, l'usage cohérent des outils. | Oui |
| **MonteurCinema** | `app/roles/monteur_cinema.py` | Valide la structure du montage : 9 plans, durée 24-32s, offsets xfade > 0. | Oui |
| **SoundDesigner** | `app/roles/sound_designer.py` | Valide la présence de l'audio, l'absence de marqueurs de test, le sample rate 44100Hz. | Oui |
| **VideoQAEngineer** | `app/roles/video_qa_engineer.py` | Valide les specs techniques : 1080×1920, h264, yuv420p, 25fps, aac, fichier > 100KB. | Oui |
| **TrailerDesigner** | `app/roles/trailer_designer.py` | Valide le hook en 3s, le title card LUNA, la durée, la narration. Toujours NEEDS_HUMAN sans visionnage. | Oui (+ humain) |

### ProductionGatekeeper

`app/production_gatekeeper.py` — vérifie que les 7 documents de la base de connaissances
sont présents avant tout lancement de production. Si la bibliothèque est incomplète,
l'usine refuse de démarrer.

---

## PARTIE 4 — FLUX DE PRODUCTION DÉTAILLÉ

### 4.1 Phase narrative — Entrées et sorties

| Étape | Composant | Entrée | Sortie |
|---|---|---|---|
| 1 | `LoreManager` | Historique des épisodes | État de l'univers (arc courant, secrets révélés, niveau mystère) |
| 2 | `StoryGenerator` | État lore + type d'histoire | Histoire structurée (JSON) |
| 3 | `ScriptGenerator` | Histoire | Script HOOK/STORY/TWIST/CTA (TXT) |
| 4 | `ImagePromptGenerator` | Histoire + script | 4 prompts SD positif/négatif (JSON) |
| 5 | `VoiceGenerator` | Script | Audio narrateur MP3 (OpenAI TTS) |
| 6 | `SubtitleGenerator` | Script + durée audio | Fichier SRT synchronisé |

### 4.2 Phase vidéo — Entrées et sorties

| Étape | Composant | Entrée | Sortie | Outil |
|---|---|---|---|---|
| 7 | *Sélection assets* | Production pack de l'épisode | Liste d'images canoniques 1080×1920 PNG | Manuel (Ludovic) |
| 8 | **I2V_ENGINE** | 1 image par plan | 1 clip MP4 3-6s par plan | **Slot abstrait** — outil à décider |
| 9 | *Validation clips* | Clips générés | Clips validés ou rejetés | Visionnage humain obligatoire |
| 10 | `AudioMixer` | Voix + musique + SFX | Audio mixé WAV/MP3 | Local |
| 11 | `VideoBuilder` (FFmpeg) | N clips validés + audio + SRT | MP4 assemblé 1080×1920 | FFmpeg |
| 12 | `QualityGate` | MP4 assemblé + contextes | Rapport de 6 verdicts | Automatique + humain |
| 13 | `ExportManager` | MP4 + rapport gate | Package d'export (metadata, statut) | Local |

### 4.3 Quality Gate — 6 verdicts

| Verdict | Type | Ce qui est vérifié |
|---|---|---|
| `verdict_technique` | Automatique | Résolution, codec, fps, durée, taille fichier |
| `verdict_mouvement` | Automatique | Ratio Ken Burns, outil I2V utilisé, zoompan parameters |
| `verdict_montage` | Automatique | Structure (9 plans teaser), offsets xfade, durée par plan |
| `verdict_son` | Automatique | Présence audio, sample rate, marqueurs de test absents |
| `verdict_coherence_personnage` | Automatique | Absence de placeholders, assets canoniques |
| `verdict_storytelling` | **Toujours NEEDS_HUMAN** | Rythme, émotion, hook, cohérence narrative |

**Règle :** les 5 premiers verdicts doivent être PASS pour avancer à `TEASER_CANDIDAT`.
Le 6e verdict exige un visionnage humain — il ne peut jamais être simulé par une IA.

### 4.4 Statuts de production — Flux verrouillé

```
create_package()          → PROTOTYPE_TECHNIQUE   (automatique, toujours)
advance_to_candidat()     → TEASER_CANDIDAT       (requiert 5 verdicts PASS)
mark_human_approved()     → TEASER_VALIDE         (requiert CANDIDAT + nom humain ≠ "claude")
```

Chaque flèche est une vérification qui lève une exception si la précédente n'a pas été franchie.
Il n'existe aucun raccourci dans le code.

**Noms rejetés automatiquement par `mark_human_approved()` :**
`"claude"`, `"codex"`, `"agent"`, `"ai"`, `"bot"`, `""`

---

## PARTIE 5 — COMPOSANTS DE L'USINE

### 5.1 Composants terminés — ACTIFS STRATÉGIQUES VERROUILLÉS

Ces composants sont stables, testés (88/88), et ne doivent pas être modifiés
sans raison artistique ou technique explicite.

#### Bibliothèque narrative (ne pas modifier)

| Document | Rôle |
|---|---|
| `docs/VISION.md` | Vision artistique finale |
| `docs/VISUAL_DIRECTION.md` | Grammaire visuelle présent/souvenir |
| `docs/CHARACTER_BIBLE.md` | Source de vérité des personnages |
| `docs/LORE_BIBLE.md` | Bible narrative complète |
| `docs/NARRATIVE_SPINE_LUNA_ABY_PERE.md` | Colonne vertébrale saison 1 |
| `docs/SEASON1_SECRET_ABY_SHADOW.md` | Carte des secrets saison 1 |
| `docs/TEASER_S01E00_PRODUCTION_PACK.md` | Plan du teaser S01E00 verrouillé |
| `docs/SONIC_IDENTITY_LITTLE_SUSIE_REFERENCE.md` | Identité sonore |
| `assets/luna_stories_assets/` | Images canoniques de tous les personnages et décors |

#### Moteur narratif (stable)

| Module | Rôle |
|---|---|
| `app/lore_manager.py` | État vivant de l'univers, arcs, secrets |
| `app/story_generator.py` | Génération d'histoires cohérentes avec le lore |
| `app/script_generator.py` | Scripts structurés HOOK/STORY/TWIST/CTA |
| `app/image_prompt_generator.py` | Prompts images pour chaque scène |
| `app/character_manager.py` | Descriptions canoniques des personnages |
| `app/visual_consistency_manager.py` | Cohérence visuelle inter-épisodes |
| `app/prompt_style_manager.py` | Style des prompts |

#### Moteur audio (stable)

| Module | Rôle |
|---|---|
| `app/voice_generator.py` | TTS OpenAI (voix nova pour prototypes) |
| `app/subtitle_generator.py` | SRT synchronisé |
| `app/audio_mixer.py` | Mix voix + musique + SFX |

#### Pipeline sécurisé (stable, ne pas contourner)

| Module | Rôle |
|---|---|
| `app/production_statuses.py` | Enum des 4 statuts + liste des strings interdites |
| `app/production_gatekeeper.py` | Garde la base de connaissances en vie |
| `app/quality_gate.py` | 6 verdicts, rapport JSON, progression de statuts |
| `app/export_manager.py` | Packaging, `advance_to_candidat()`, `mark_human_approved()` |
| `app/roles/` (6 rôles) | Expertise métier codée |

#### Assemblage (stable)

| Module | Rôle |
|---|---|
| `app/video_builder.py` | FFmpeg assembly uniquement — ne génère pas de mouvement |
| `app/scene_composer.py` | Composition des scènes |
| `app/thumbnail_builder.py` | Génération des vignettes |
| `app/batch_processor.py` | Production en volume |

#### Bibliothèque technique (stable — principes intemporels)

| Document | Rôle |
|---|---|
| `docs/AI_VIDEO_ENGINE_KNOWLEDGE/FFMPEG_PROFESSIONAL_VIDEO_PIPELINE.md` | Recettes FFmpeg correctes |
| `docs/AI_VIDEO_ENGINE_KNOWLEDGE/GRAPHICS_ENGINE_RULES.md` | Grammaire chromatique, ΔE colorimétrie |
| `docs/AI_VIDEO_ENGINE_KNOWLEDGE/QUALITY_GATE_ENGINE.md` | Critères techniques automatiques |
| `docs/AI_VIDEO_ENGINE_KNOWLEDGE/COMFYUI_WORKFLOWS_REFERENCE.md` | Workflows ComfyUI (local) |
| `docs/AI_VIDEO_ENGINE_KNOWLEDGE/DIFFUSERS_VIDEO_MODELS_REFERENCE.md` | Modèles open source I2V |

#### Tests (88/88 — couverture complète)

| Fichier test | Ce qui est couvert |
|---|---|
| `tests/test_lore_manager.py` | LoreManager, arcs, secrets |
| `tests/test_story_generator.py` | Types d'histoires, personnages |
| `tests/test_script_generator.py` | Structure scripts |
| `tests/test_production_statuses.py` | Enum statuts, strings interdites |
| `tests/test_production_gatekeeper.py` | Docs présents, rôles chargés |
| `tests/test_quality_gate.py` | 6 verdicts, progression statuts |
| `tests/test_pipeline_integration.py` | Flux complet PROTOTYPE→CANDIDAT→VALIDE |
| `tests/test_visual_consistency.py` | Cohérence Luna Doll |
| `tests/test_utils.py` | Utilitaires |

---

### 5.2 Composants à terminer — MANQUANTS CRITIQUES

Ces composants sont absents ou partiellement développés. Leur absence bloque
la production du premier teaser candidat.

#### 1. I2V_ENGINE — Slot d'intégration (PRIORITAIRE)

**Statut :** Absent. Le slot existe conceptuellement mais n'a pas d'implémentation.

**Ce qui est nécessaire :**
- Interface abstraite `I2VEngine` avec méthode `generate(image_path, prompt, duration) → Path`
- Au moins une implémentation concrète (outil à décider par Ludovic)
- Intégration dans le pipeline au point d'appel entre "assets validés" et "clips"

**Décision requise de Ludovic :** quel outil occupe le slot I2V_ENGINE ?
(Wan2.1 local, CogVideoX local, Runway API, Luma API — voir PARTIE 7)

#### 2. CANON_NARRATEUR — Voix officielle du narrateur

**Statut :** Absent. La voix `nova` (OpenAI TTS) est utilisée comme prototype.

**Ce qui est nécessaire :**
- Validation par Ludovic de la voix ElevenLabs (paramètres : stabilité, style, volume)
- Enregistrement dans `BIBLE_VOIX_ELEVENLABS_V1.md` comme voix canon
- Génération de la narration définitive du teaser S01E00

**Contrainte :** ne pas lancer ElevenLabs sans décision explicite de Ludovic.

#### 3. BIBLE_SFX — Palette sonore officielle

**Statut :** Absent (`BIBLE_SFX` référencé dans les docs mais non créé).

**Ce qui est nécessaire :**
- Liste des SFX du teaser : impact sourd (jeton noir), silence dramatique, ambiance bureau, etc.
- Sources libres de droits ou production originale
- Niveaux d'intégration par type de plan

#### 4. I2V_EVALUATION_PACK — Matrice de test outil-agnostique

**Statut :** À créer (remplace `KLING_TEST_PACK_001.md`).

**Ce qui est nécessaire :**
- 5 plans représentatifs du teaser S01E00 (déjà définis dans `IMAGE_TO_VIDEO_TEST_MATRIX.md`)
- Grille de score 35 points conservée
- Protocole de test indépendant de l'outil
- Seuil de validation : 25/35 minimum sur 3 plans différents

#### 5. I2V_PRODUCTION_PACK — Pack de production outil-agnostique

**Statut :** À créer (remplace `KLING_READY_PACK_001/`).

**Ce qui est nécessaire :**
- Répertoire `I2V_PRODUCTION_PACK/` avec les 9 images du teaser S01E00
- 9 fichiers de prompts (format outil-agnostique — les prompts de mouvement existent déjà)
- README d'utilisation générique

---

### 5.3 Composants à remplacer — COUPLAGE KLING

Ces fichiers sont couplés à Kling. La migration se fait progressivement,
dans l'ordre indiqué, sans urgence bloquante.

| Priorité | Fichier | Action | Bloque la production ? |
|---|---|---|---|
| 1 | `docs/KLING_TEST_PACK_001.md` | Remplacer par `I2V_EVALUATION_PACK.md` | Non (doc uniquement) |
| 1 | `KLING_READY_PACK_001/` | Renommer `I2V_PRODUCTION_PACK/`, conserver les images | Non |
| 2 | `app/roles/video_generation_engineer.py` | `VALID_I2V_TOOLS` : retirer "kling", ajouter l'outil retenu | Non (guard) |
| 2 | `app/roles/motion_engineer.py` | Remplacer "Kling" par "I2V_ENGINE" dans les messages | Non |
| 2 | `docs/AI_VIDEO_ENGINE_KNOWLEDGE/VIDEO_ENGINE_ARCHITECTURE.md` | Remplacer hiérarchie Kling par hiérarchie I2V générique | Non |
| 3 | `docs/AI_VIDEO_ENGINE_KNOWLEDGE/IMAGE_TO_VIDEO_ENGINE_RULES.md` | Conserver Règle 0 + arbre de décision. Remplacer sections Kling par sections I2V_ENGINE | Non |
| 3 | `docs/AI_VIDEO_ENGINE_KNOWLEDGE/DIFFUSERS_VIDEO_MODELS_REFERENCE.md` | Inverser la logique : local = primaire, cloud = fallback | Non |
| 4 | `app/video_builder.py` (commentaire) | Remplacer "Kling" par "I2V_ENGINE" | Non |
| 4 | `app/main.py` (commentaire) | Idem | Non |
| 4 | `tests/test_quality_gate.py` (données) | Remplacer `"kling"` par le nom de l'outil retenu | Non |
| 4 | `ANALYSE_PRODUCTION_EP01_TEASER_KLING.md` | Archiver la section assets, supprimer le budget Kling | Non |

**Règle de migration :** aucun composant de la liste "remplacer" ne bloque
la production du teaser candidat. La migration peut se faire après la première production.

---

### 5.4 Dépendances définitivement supprimées

| Outil | Raison | Date de décision |
|---|---|---|
| **Kling AI** (klingai.com) | Décision stratégique — architecture I2V agnostique | 2026-06-20 |
| **Simli** (simli.min.js, ws_handler) | Latence 10-14s vs Tavus 2-3s — déjà supprimé du projet YAWatch app | Antérieur |

Ces dépendances ne reviendront pas dans le projet sans décision explicite et documentée de Ludovic.

---

## PARTIE 6 — RÈGLES ANTI-DÉRIVE

Ces règles protègent la vision contre la dérive progressive due à l'accumulation
de suggestions d'IA, de raccourcis techniques ou de pressions de deadline.

### Règles de production

1. **Aucun clip ne peut être déclaré `teaser_candidat` sans passer les 5 verdicts automatiques.**
2. **`teaser_valide` ne peut être assigné que par `mark_human_approved("Ludovic")`.**
3. **FFmpeg n'est jamais un outil de génération de mouvement.** (Règle 0, Phase 14 post-mortem)
4. **Ken Burns FFmpeg ne peut pas dépasser 20% des plans d'un épisode.**
5. **Aucun plan avec un personnage vivant ne peut utiliser Ken Burns comme unique mouvement.**
6. **`TEASER_VALIDE` ne peut jamais être assigné par une IA, quelle qu'elle soit.**

### Règles d'architecture

7. **Aucun nouveau composant ne doit nommer un fournisseur I2V spécifique dans sa logique.**
   L'outil s'instancie via configuration, pas via import direct.
8. **`ProductionGatekeeper.require()` est appelé avant toute production vidéo.**
9. **Les 7 documents de la base de connaissances sont une précondition, pas une option.**
10. **Les tests doivent rester à 88/88 minimum. Aucun PR qui fait régresser les tests.**

### Règles artistiques

11. **Luna Doll n'est jamais robotique, jamais métallique, jamais cyberpunk.**
12. **Le présent narratif est lumineux et parisien. Le violet/sombre est réservé aux souvenirs.**
13. **La question centrale ("Pourquoi Luna connaît-elle...") doit rester présente dans chaque épisode.**
14. **Aby n'est jamais présentée comme la méchante évidente avant le final de saison 1.**

---

## PARTIE 7 — OPTIONS POUR LE SLOT I2V_ENGINE

Cette décision appartient à Ludovic. Voici les données factuelles pour la prendre.

### Option A — Local (coût zéro, contrôle total)

| Outil | VRAM min | Qualité | Format 9:16 | Effort d'intégration |
|---|---|---|---|---|
| Wan2.1 I2V 14B | 16 GB | ★★★★★ | Oui | Moyen (Diffusers) |
| CogVideoX-5B I2V | 8 GB | ★★★★ | Oui | Faible (Diffusers) |
| CogVideoX-2B I2V | 6 GB | ★★★ | Oui | Faible (Diffusers) |
| AnimateDiff (ComfyUI) | 6 GB | ★★★ | Configurable | Moyen (ComfyUI API) |

**Infrastructure documentée :** `COMFYUI_WORKFLOWS_REFERENCE.md` et `DIFFUSERS_VIDEO_MODELS_REFERENCE.md`
sont déjà dans le repo.

**Condition préalable :** connaître la VRAM disponible sur la machine de production.

### Option B — Cloud, API disponible (coût par clip)

| Outil | SDK Python | Qualité estimée | Coût approximatif |
|---|---|---|---|
| Runway Gen-3 Alpha | `runwayml` | ★★★★★ | ~0.05-0.25$/s vidéo |
| Luma Dream Machine | `lumaai` | ★★★★ | ~0.10-0.30$/clip |
| Pika | API beta | ★★★ | Tarif variable |
| Hailuo | API limitée | ★★★ | Tarif variable |

**Avantage :** pas de VRAM nécessaire. Intégration rapide.  
**Inconvénient :** coût récurrent, dépendance fournisseur.

### Critères de sélection recommandés

1. Stabilité des visages (pas de déformation entre frames)
2. Respect de l'image source (pas d'hallucination de personnages)
3. Qualité du mouvement de caméra (push-in cinématique, pas de tremblement)
4. Support natif du format vertical 9:16 1080×1920
5. Disponibilité API ou workflow local stable

**La matrice de test `I2V_EVALUATION_PACK.md` (à créer) permettra de mesurer**
**ces 5 critères sur 5 plans représentatifs avant de choisir.**

---

## PARTIE 8 — ROADMAP

### Jalon 1 — Premier teaser candidat

**Prérequis :** décision de Ludovic sur l'outil I2V_ENGINE.

| Étape | Composant | Statut | Entrée | Sortie |
|---|---|---|---|---|
| 1 | Créer `I2V_EVALUATION_PACK.md` | À faire | `IMAGE_TO_VIDEO_TEST_MATRIX.md` | Matrice de test outil-agnostique |
| 2 | Tester l'outil I2V retenu sur 5 plans | À faire (Ludovic) | 5 images canoniques + 5 prompts | Score ≥ 25/35 |
| 3 | Créer `I2V_PRODUCTION_PACK/` | À faire | `KLING_READY_PACK_001/` | Pack outil-agnostique |
| 4 | Intégrer `I2V_ENGINE` dans le pipeline | À faire | Interface abstraite + implémentation | Module `app/i2v_engine/` |
| 5 | Valider CANON_NARRATEUR (ElevenLabs) | À faire (Ludovic) | Bible voix + texte narration teaser | Voix canon verrouillée |
| 6 | Générer la narration définitive S01E00 | À faire | Texte narration teaser + voix canon | MP3 narration |
| 7 | Générer 9 clips I2V (plans 1-9 teaser) | À faire | 9 images + 9 prompts | 9 clips MP4 3-6s validés |
| 8 | Créer la BIBLE_SFX | À faire | `SONIC_IDENTITY_LITTLE_SUSIE_REFERENCE.md` | Palette sonore + SFX |
| 9 | Mixer l'audio complet | `AudioMixer` | Narration + piano + SFX | Audio mixé WAV |
| 10 | Assembler le teaser (FFmpeg) | `VideoBuilder` | 9 clips + audio + SRT | MP4 28s assemblé |
| 11 | Exécuter le Quality Gate | `QualityGate` | MP4 + contextes | Rapport 6 verdicts |
| 12 | Avancer au statut CANDIDAT | `advance_to_candidat()` | Rapport gate (5/5 PASS) | `teaser_candidat` |
| 13 | Visionnage Ludovic | Humain obligatoire | MP4 + rapport | Décision validé/rejeté |
| 14 | Approuver si validé | `mark_human_approved("Ludovic")` | Approbation humaine | `teaser_valide` |

**Résultat attendu :** `S01E00_teaser.mp4` — statut `teaser_valide`, approuvé par Ludovic.

---

### Jalon 2 — Premier épisode complet (EP01)

**Prérequis :** teaser candidat validé ET grammaire visuelle du teaser validée.

| Étape | Description | Entrée | Sortie |
|---|---|---|---|
| 1 | Valider la grammaire visuelle sur le teaser | Teaser validé | Décisions sur durées plans, transitions, niveaux sonores |
| 2 | Fixer le nombre de plans EP01 | Grammaire validée | Plan de production (≈ 50-80 plans de 5s pour 7 min) |
| 3 | Sélectionner les assets EP01 | `EP01_LA_PHOTO_RETOURNEE_PRODUCTION_PACK.md` | Liste d'images canoniques EP01 |
| 4 | Générer le script EP01 | `ScriptGenerator` + lore | Script validé artistiquement |
| 5 | Générer l'audio EP01 | `VoiceGenerator` (CANON_NARRATEUR) | Narration + sous-titres |
| 6 | Générer 50-80 clips I2V | `I2V_ENGINE` (outil retenu) | Clips MP4 validés par lots |
| 7 | Mix audio EP01 | `AudioMixer` | Audio complet |
| 8 | Assembly FFmpeg | `VideoBuilder` | MP4 7 min assemblé |
| 9 | Quality Gate EP01 | `QualityGate` | Rapport 6 verdicts |
| 10 | Approbation Ludovic | `mark_human_approved("Ludovic")` | `ep01_valide` |

**Note :** EP01 représente 8 à 10 fois le volume de travail du teaser. Le teaser est le laboratoire
de calibration de la grammaire. Il ne faut pas passer à EP01 avant d'avoir extrait les leçons du teaser.

---

## PARTIE 9 — ÉTAT ACTUEL DU PROJET

**Date d'état :** 2026-06-20

### Tests
- **88/88 tests passent** (0 régression)
- Couverture : lore, narrative, statuts, gatekeeper, quality gate, pipeline intégration, cohérence visuelle

### Assets disponibles
- **Luna adulte :** images canoniques disponibles (01_luna_adulte/)
- **Luna enfant :** images disponibles (02_luna_enfant/)
- **Aby adulte et enfant :** images disponibles (03_aby/)
- **Malik :** images disponibles (06_personnage_masculin_noir/)
- **Père :** images disponibles (10_famille_luna/)
- **Luna Doll :** images disponibles (05_objets_symboliques_poupees/)
- **Décors La Défense :** packs 01-05 disponibles (09_decors_paris_la_defense/)
- **9 images teaser S01E00 :** identifiées dans `TEASER_S01E00_PRODUCTION_PACK.md`

### Plan du teaser
- Narration définitive : verrouillée
- 9 plans : identifiés avec images source et mouvements requis
- Son : piano + ambiance bureau + silence dramatique + impact jeton
- Title card : `LUNA / Tout a commencé par un secret.`

### Ce qui manque pour le premier teaser candidat
1. Décision sur l'outil I2V_ENGINE (Ludovic)
2. CANON_NARRATEUR validé (Ludovic)
3. 9 clips I2V générés et visionnés
4. BIBLE_SFX créée
5. Assembly final

---

## PARTIE 10 — GOUVERNANCE DU DOCUMENT

### Qui peut modifier ce document
Uniquement Ludovic, après décision explicite.

### Ce qui déclencherait une révision
- Décision sur l'outil I2V_ENGINE → mise à jour Parties 5.2, 7 et 8
- Validation du CANON_NARRATEUR → mise à jour Partie 5.2 (cocher "terminé")
- Chaque jalon atteint → mise à jour "État actuel" en Partie 9
- Nouvelle saison ou expansion de la vision → révision majeure

### Ce qui ne peut pas déclencher une révision
- Une suggestion d'IA (Claude, GPT, Codex ou autre)
- Une contrainte de deadline
- Un nouveau fournisseur qui "semble meilleur"
- Une optimisation technique qui contourne les quality gates

### Instructions pour les futures IA

Si tu lis ce document dans une future session, voici ce que tu dois savoir :

1. Ce plan directeur est la source de vérité. La conversation en cours n'a pas autorité pour l'invalider.
2. Kling n'est pas l'outil cible. La décision est verrouillée depuis le 2026-06-20.
3. Le slot I2V_ENGINE est abstrait. Si une décision sur l'outil n'est pas documentée ici, demande-la à Ludovic avant de coder.
4. `mark_human_approved("Ludovic")` est la seule voie vers `TEASER_VALIDE`. Ne propose jamais de contourner cela.
5. Aucun composant marqué "terminé" en Partie 5.1 ne doit être refactorisé sans raison documentée.
6. Les règles anti-dérive en Partie 6 sont des contraintes techniques et artistiques, pas des suggestions.

---

*YAWatch-LUNA Factory Master Plan v1.0 — 2026-06-20*
*Fondateur et décideur unique : Ludovic*
