# YAWatch Video Engine API MVP

## Objectif

`yawatch-video-engine` est la premiere architecture API locale destinee a
remplacer progressivement Kling pour les besoins internes de YAWatch-LUNA.

Ce n'est pas un outil "anime une photo". Le but est de produire un plan
cinematique narratif exploitable dans une serie, avec une intention dramatique,
un type de plan, un mouvement camera, un besoin sonore, une revue qualite et un
dossier de production reutilisable.

La philosophie validee reste:

- qualite avant automatisation;
- Paris et La Defense doivent rester realistes;
- Luna, Aby, Malik et les autres personnages doivent rester coherents;
- aucun fallback silencieux;
- validation humaine finale par Ludovic;
- l'architecture doit survivre au remplacement de Wan, FramePack ou tout autre moteur.

## Architecture creee

```text
app/yawatch_video_engine/
  api.py                 FastAPI, endpoint /generate-shot
  schemas.py             contrat JSON entree/sortie
  engine.py              orchestrateur principal
  scene_parser.py        transforme la demande en contexte scene
  shot_planner.py        choisit grammaire de plan et risques
  camera_director.py     planifie mouvement camera
  pose_control.py        prepare corps entier/deplacement/objet
  motion_engine.py       planifie mouvement sujet + cibles techniques
  i2v_adapter.py         adaptateurs mock, Wan, FramePack, pose-to-video futur
  sound_layer.py         silence, ambiance, bruitage, voix off, dialogue
  montage_exporter.py    preview + MP4 mock via FFmpeg si disponible
  quality_review.py      score artistique MVP + limites
  run_manager.py         dossier de run, logs, JSON
  examples/
    generate_shot_kling_like.json
```

Schema JSON:

```text
docs/schemas/generate_shot_request.schema.json
```

## Endpoint

```http
POST /generate-shot
```

### Entree minimale

```json
{
  "shot_id": "plan02_luna_kling_like_local_mvp",
  "character_reference_image": "assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png",
  "decor_description": "bureau YAWatch de nuit a La Defense, ecran Iris Workspace",
  "dramatic_intention": "Luna comprend qu'une verite familiale revient, mais garde le controle.",
  "shot_type": "plan_poitrine",
  "duration_sec": 5,
  "camera_motion": "slow_push_in",
  "emotion": "contained tension",
  "sound_need": {
    "mode": "ambiance",
    "ambience_description": "bureau nocturne calme, ville lointaine"
  },
  "engine_preference": "mock"
}
```

### Sortie

```json
{
  "run_id": "...",
  "status": "mock_generated",
  "run_dir": "...",
  "mp4_final": ".../final.mp4",
  "preview_png": ".../preview.png",
  "metadata_json": ".../metadata.json",
  "quality_review_json": ".../quality_review.json",
  "artistic_score": {},
  "logs_techniques": [".../logs/technical.log"],
  "production_folder_reusable": true
}
```

## Dossier de run

Chaque appel genere:

```text
content/video_engine_runs/<timestamp>_<shot_id>/
  input.json
  scene_parse.json
  shot_plan.json
  camera_plan.json
  pose_plan.json
  motion_plan.json
  sound_plan.json
  render_result.json
  quality_review.json
  metadata.json
  preview.png
  final.mp4
  logs/technical.log
```

Ce dossier est volontairement verbeux. Il doit permettre a Claude, Codex,
DeepSeek ou Ludovic de comprendre exactement ce qui a ete decide avant la
generation.

## Pourquoi ce MVP est different d'une comparaison Wan vs FramePack

La comparaison Wan/FramePack repond a:

> Quel moteur bouge mieux une image?

`yawatch-video-engine` repond a:

> Quel plan narratif veut-on produire, avec quelle intention, quel mouvement,
> quel risque, quel son, quel moteur et quelle revue qualite?

Le moteur I2V n'est qu'un executant. L'API conserve la logique cinema au-dessus
du moteur.

## Criteres artistiques a suivre

Les prochains tests ne doivent pas seulement comparer SSIM, flicker ou optical
flow. Les criteres YAWatch-LUNA prioritaires sont:

1. Presence humaine
   Le personnage doit respirer, avoir un poids, une attention, une hesitation.

2. Intention dramatique
   Le mouvement doit faire sentir une pensee ou une menace interieure.

3. Mouvement corps
   Les yeux seuls ne suffisent pas. Cheveux, epaules, mains, posture et objet
   doivent vivre sans se deformer.

4. Profondeur decor
   Le bureau, La Defense ou Paris doivent avoir des couches spatiales lisibles.

5. Tension cinematographique
   Le mouvement camera doit soutenir le mystere, pas faire "demo IA".

6. Stabilite technique
   Identite, visage, lumiere, mains et objet ne doivent pas deriver.

## Lecon tiree du clip Kling cible

Le clip Kling cible ne gagne pas seulement parce qu'il bouge davantage. Il gagne
parce que le mouvement est distribue:

- visage;
- cheveux;
- epaules;
- mains;
- objet;
- decor;
- camera;
- lumiere.

Objectif local: reproduire cette impression par etapes:

1. Motion pass: Wan, FramePack ou futur modele cree le mouvement global.
2. Identity pass: restauration/ancrage visage et cheveux.
3. Stabilization pass: deflicker, color/luminance consistency.
4. Sound pass: ambiance, bruitage, voix off si necessaire.
5. Quality Gate: metriques + revue artistique humaine.

## Branchement WAN

Dans `app/yawatch_video_engine/i2v_adapter.py`, `WanAdapter` est actuellement
un adaptateur planifie. Pour le rendre productif:

1. connecter l'adaptateur au runner ComfyUI Wan GGUF deja teste;
2. mapper `character_reference_image` vers le noeud `LoadImage`;
3. transformer `motion_plan.target_artistic_axes` en prompt positif;
4. appliquer les regles negatives anti-deformation;
5. verrouiller duree, fps, resolution et seed dans le job;
6. recopier le MP4 dans le dossier de run;
7. appeler `app/i2v_quality_gate.py` apres generation.

WAN est utile pour obtenir plus de vie et de mouvement, mais il doit etre
surveille pour la derive visage.

## Branchement FramePack

`FramePackAdapter` doit etre branche au runner FramePack RunPod ou local.

FramePack est interessant quand la priorite est la stabilite. Sa faiblesse
observee est un rendu parfois trop fige. Dans cette architecture, FramePack
peut etre utilise pour:

- portraits calmes;
- inserts emotionnels;
- plans ou l'identite compte plus que le mouvement;
- generation de base avant ajout d'un mouvement camera/son.

## Branchement pose-to-video

Les plans de corps entier, deplacement ou interaction objet demandent une brique
plus forte que le simple I2V:

- OpenPose / ControlNet;
- depth map;
- sequence de poses;
- reference objet;
- eventuellement un moteur video qui accepte explicitement corps et camera.

`PoseToVideoAdapter` est reserve a cette evolution. Il ne doit pas etre simule
comme reussite tant qu'un vrai workflow pose/depth n'existe pas.

## Commande locale

Installer les dependances:

```powershell
pip install -r requirements.txt
```

Lancer l'API:

```powershell
uvicorn app.yawatch_video_engine.api:app --reload --port 8010
```

Tester l'exemple:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8010/generate-shot `
  -ContentType "application/json" `
  -InFile app/yawatch_video_engine/examples/generate_shot_kling_like.json
```

## Limites honnetes du MVP

- Le mode `mock` ne valide pas une vraie qualite video.
- Le score artistique actuel evalue surtout la preparation du plan.
- Les adaptateurs Wan/FramePack ne generent pas encore depuis cette API.
- Le MP4 mock est une preuve de plomberie, pas une preuve artistique.
- Le Quality Gate I2V complet doit etre appele des qu'un vrai MP4 est produit.

## Prochaine action recommandee

Brancher `WanAdapter` sur le runner existant, puis lancer un seul plan test:

```text
Luna adulte, plan poitrine, 5 secondes, slow_push_in, tension contenue,
decor bureau YAWatch nuit, interaction cadre photo.
```

Le test sera considere utile seulement si le dossier de run contient:

- MP4 reel;
- preview;
- metadata;
- logs;
- metriques I2V;
- score artistique;
- verdict humain de Ludovic.
