# QUALITY GATE ENGINE — YAWatch-LUNA

## Métier correspondant
Responsable Qualité · Ingénieur pipeline · (Enforcement automatique + validation humaine)

## Sources expertes utilisées
- VISUAL_DIRECTION.md (Quality Gate existant, à automatiser)
- "The Checklist Manifesto" — Atul Gawande (application des checklists à la production créative)
- Pixar's "Dailies" process (validation quotidienne par le directeur artistique)
- TEASER_S01E00_PRODUCTION_PACK.md (référence absolue pour le teaser)
- CHARACTER_BIBLE.md (critères personnage)
- FFMPEG_PROFESSIONAL_VIDEO_PIPELINE.md (critères techniques)
- IMAGE_TO_VIDEO_ENGINE_RULES.md (critères mouvement)

## Problème empêché
La défaillance exacte de la Phase 14 : un fichier MP4 (prototype avec images placeholder,
sans animation réelle, sans son canon) déclaré "utilisable" sans Quality Gate.
Sans ce document, n'importe quel agent peut marquer n'importe quoi comme production_ready.

## Code repo qui doit respecter ce document
- `app/video_builder.py` (INTERDIT de déclarer STATUS=production_ready sans Gate)
- `app/quality_gate.py` (à créer — ce document en est la spec complète)
- `app/export_manager.py` (ne peut exporter un fichier final sans Gate passé)

## Règles bloquantes (inviolables)
1. STATUS=production_ready ne peut être assigné que par un humain (Ludovic) après visionnage.
2. Le pipeline peut assigner STATUS=prototype ou STATUS=gate_passed_technical uniquement.
3. Aucun fichier dont les checks techniques échouent ne peut passer en validation humaine.
4. Un fichier qui utilise des images placeholder est AUTOMATIQUEMENT STATUS=prototype.

---

## Architecture du Quality Gate

```
NIVEAU 1 — Gate technique automatique (code)
    Résolution, codec, fps, durée, audio sync, format
    → RÉSULTAT : PASS ou FAIL_TECHNIQUE
    → Si FAIL : retour au pipeline avec message d'erreur précis

NIVEAU 2 — Gate contenu automatique (code + heuristiques)
    Assets canon vs placeholder, personnages détectés, durée conforme
    → RÉSULTAT : PASS ou FAIL_CONTENU
    → Si FAIL : retour au pipeline avec message d'erreur précis

NIVEAU 3 — Gate artistique humain (Ludovic)
    Visionnage sur mobile, casque, plein écran
    Vérification lore, cohérence personnage, rythme, émotion
    → RÉSULTAT : APPROVED ou REWORK(motif)
    → Si APPROVED : STATUS=production_ready assigné manuellement

NIVEAU 4 — Gate distribution (avant upload YouTube)
    Métadonnées, titre, description, thumbnail, hashtags
    → Seulement quand Level 3 = APPROVED
```

---

## NIVEAU 1 — Gate technique (automatisable)

### Checks obligatoires
```python
import subprocess
import json
from pathlib import Path

def gate_technique(filepath: str) -> dict:
    """
    Quality Gate Niveau 1 — Validation technique automatique.
    Returns : {"pass": bool, "errors": list[str], "warnings": list[str]}
    """
    errors = []
    warnings = []
    path = Path(filepath)

    # Vérification existence
    if not path.exists():
        return {"pass": False, "errors": [f"Fichier introuvable : {filepath}"], "warnings": []}

    # Inspection FFprobe
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_streams", "-show_format", filepath
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"pass": False, "errors": ["FFprobe ne peut pas lire le fichier"], "warnings": []}

    data = json.loads(result.stdout)
    streams = {s["codec_type"]: s for s in data.get("streams", [])}

    # Check vidéo
    if "video" not in streams:
        errors.append("Aucun flux vidéo détecté")
    else:
        v = streams["video"]

        # Résolution
        w, h = v.get("width", 0), v.get("height", 0)
        if w != 1080 or h != 1920:
            errors.append(f"Résolution incorrecte : {w}×{h} (attendu 1080×1920)")

        # Codec
        codec = v.get("codec_name", "")
        if codec != "h264":
            errors.append(f"Codec vidéo : {codec} (attendu h264)")

        # FPS
        fps_str = v.get("r_frame_rate", "0/1")
        num, den = map(int, fps_str.split("/"))
        fps = num / den if den != 0 else 0
        if abs(fps - 25.0) > 0.5:
            warnings.append(f"FPS : {fps:.2f} (attendu 25.0)")

        # Pixel format
        pix_fmt = v.get("pix_fmt", "")
        if pix_fmt != "yuv420p":
            errors.append(f"Pixel format : {pix_fmt} (attendu yuv420p)")

    # Check audio
    if "audio" not in streams:
        errors.append("Aucun flux audio détecté")
    else:
        a = streams["audio"]
        if a.get("codec_name") != "aac":
            warnings.append(f"Codec audio : {a.get('codec_name')} (attendu aac)")
        if int(a.get("sample_rate", 0)) != 44100:
            warnings.append(f"Sample rate audio : {a.get('sample_rate')} (attendu 44100)")

    # Check durée
    duration = float(data.get("format", {}).get("duration", 0))
    if duration < 5.0:
        errors.append(f"Durée trop courte : {duration:.1f}s (minimum 5s)")
    if duration > 180.0:
        warnings.append(f"Durée inhabituellement longue : {duration:.1f}s")

    # Check faststart (moov atom en début de fichier)
    # Heuristique : le fichier doit être lisible dès les premières secondes
    # (vérification complète nécessite un test de streaming — simplifié ici)
    size_kb = path.stat().st_size / 1024
    if size_kb < 50:
        errors.append(f"Fichier suspect : seulement {size_kb:.0f} KB — probablement vide ou corrompu")

    return {
        "pass": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "duration": duration,
        "resolution": f"{w}×{h}" if "video" in streams else "N/A"
    }
```

---

## NIVEAU 2 — Gate contenu (automatisable)

### Checks obligatoires
```python
from pathlib import Path
import subprocess

PLACEHOLDER_PATTERNS = [
    "scene_hook", "scene_story", "scene_climax", "scene_resolution",
    "episode_test", "placeholder", "test_image", "demo_"
]

TEASER_PLANS_REQUIS = [
    "TEASER_PLAN_01", "TEASER_PLAN_02", "TEASER_PLAN_03",
    "TEASER_PLAN_04", "TEASER_PLAN_05", "TEASER_PLAN_06",
    "TEASER_PLAN_07", "TEASER_PLAN_08", "TEASER_PLAN_09"
]

def gate_contenu(filepath: str, manifest_path: str = None) -> dict:
    """
    Quality Gate Niveau 2 — Validation contenu.
    """
    errors = []
    warnings = []
    path = Path(filepath)

    # Check 1 : nom du fichier ne contient pas de patterns placeholder
    filename = path.name.lower()
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern in filename:
            errors.append(f"Fichier utilise un pattern placeholder : '{pattern}' dans '{filename}'")

    # Check 2 : présence d'un manifest
    if manifest_path:
        manifest = Path(manifest_path)
        if not manifest.exists():
            warnings.append("Manifest JSON absent — pas de traçabilité")
        else:
            import json
            with open(manifest) as f:
                m = json.load(f)
            status = m.get("status", "unknown")
            if status == "prototype":
                errors.append(
                    "Le manifest indique STATUS=prototype. "
                    "Ce fichier ne peut pas passer le Quality Gate."
                )
            source_images = m.get("source_images", [])
            for img in source_images:
                for pattern in PLACEHOLDER_PATTERNS:
                    if pattern in str(img).lower():
                        errors.append(
                            f"Image source placeholder détectée dans le manifest : {img}"
                        )

    # Check 3 : vérification de la durée conformément au PRODUCTION_PACK
    # (Pour le teaser : 26-30 secondes)
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", filepath],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        duration = float(result.stdout.strip())
        if filepath and "teaser" in filepath.lower():
            if not (24.0 <= duration <= 32.0):
                warnings.append(
                    f"Durée teaser : {duration:.1f}s (attendu 26-30s selon PRODUCTION_PACK)"
                )

    return {
        "pass": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }
```

---

## NIVEAU 3 — Gate artistique humain

Ce niveau NE PEUT PAS être automatisé. Il requiert le visionnage par Ludovic.

### Protocole de visionnage
```
CONDITIONS REQUISES :
□ Support : smartphone (mobile, 6 pouces minimum), plein écran
□ Audio   : casque ou écouteurs (pas les haut-parleurs intégrés)
□ Ambiance: lumière normale (pas plein soleil, pas noir complet)
□ Durée   : regarder l'intégralité au moins 2 fois

PREMIER VISIONNAGE — Ressenti global
□ L'émotion passe-t-elle dans les 3 premières secondes ?
□ Le rythme tient-il jusqu'à la fin sans décrochage ?
□ La musique et la voix s'intègrent-elles naturellement ?

DEUXIÈME VISIONNAGE — Vérifications lore
□ Luna est reconnaissable (cheveux, teint, expression, vêtements)
□ La poupée est en tissu/velours violet (jamais robotique)
□ Aby n'est pas identifiée comme antagoniste explicite avant S1E06+
□ Le logo YAWatch est lisible si présent
□ Les sous-titres sont lisibles sur mobile
□ La grammaire présent/souvenir est respectée (froid vs chaud)
□ Aucun artefact IA visible (déformation, corruption)
□ Le mouvement est cinématique (pas de slideshow, pas de jitter)
```

### Résultats possibles
```
APPROVED → Ludovic signe le fichier comme production_ready
           → Renommer le fichier : ajouter _APPROVED à la fin
           → Mettre à jour le manifest : "status": "production_ready", "approved_by": "Ludovic"

REWORK(motif) → Le fichier est retourné au pipeline avec motif précis
                Motifs valides :
                - REWORK(couleur_incoh) : dérive chromatique entre plans
                - REWORK(luna_doll_robot) : poupée non conforme au canon
                - REWORK(slideshow) : mouvement insuffisant
                - REWORK(audio_sync) : désynchronisation perceptible
                - REWORK(rhythm) : rythme cassé, montage non fluide
                - REWORK(lore_breach) : violation d'une règle narrative
```

---

## NIVEAU 4 — Gate distribution (avant upload)

```python
DISTRIBUTION_CHECKLIST = {
    "titre": {
        "check": "Titre entre 30-60 caractères, contient 'LUNA' ou 'YAWatch'",
        "example": "LUNA — Tout a commencé par un secret | Teaser S01"
    },
    "description": {
        "check": "Description ≥ 100 mots, lien vers la prochaine vidéo si disponible",
        "example": "Luna pensait que sa vie était normale..."
    },
    "thumbnail": {
        "check": "1080×1920, visage Luna visible, texte lisible à 10cm",
        "example": "thumbnail_TEASER_S01E00_v1.jpg"
    },
    "hashtags": {
        "check": "3-5 hashtags pertinents",
        "example": "#Luna #YAWatch #ThrilllerPsychologique #YouTubeShorts"
    },
    "premiere": {
        "check": "Heure de publication prévue selon CONTENT_STRATEGY.md",
        "example": "Jeudi 19h00 Paris"
    }
}
```

---

## Codes de statut du pipeline

```python
class VideoStatus:
    PROTOTYPE = "prototype"
    # Généré par le pipeline local FFmpeg
    # Utilise peut-être des images placeholder
    # NE PEUT PAS être publié

    GATE_TECHNICAL_PASS = "gate_technical_pass"
    # A passé le Niveau 1 automatique
    # En attente de Gate Niveau 2

    GATE_CONTENT_PASS = "gate_content_pass"
    # A passé les Niveaux 1 et 2 automatiques
    # En attente de validation humaine (Niveau 3)

    REWORK = "rework"
    # Retourné après Gate humain avec motif
    # Inclut le motif dans le manifest

    PRODUCTION_READY = "production_ready"
    # A passé les 3 Niveaux
    # Approuvé par Ludovic
    # Prêt pour l'upload YouTube
    # SEUL STATUT PUBLIÉ

    PUBLISHED = "published"
    # Uploadé sur YouTube
    # Lien URL dans le manifest
```

---

## Rapport de Gate — template

```json
{
  "filename": "TEASER_S01E00_v1.mp4",
  "gate_run_date": "2026-XX-XX",
  "gate_niveau_1": {
    "pass": true,
    "errors": [],
    "warnings": ["FPS: 24.97 (attendu 25.0)"],
    "resolution": "1080×1920",
    "duration": 28.4
  },
  "gate_niveau_2": {
    "pass": true,
    "errors": [],
    "warnings": []
  },
  "gate_niveau_3": {
    "status": "pending",
    "approved_by": null,
    "approved_date": null,
    "rework_reason": null
  },
  "final_status": "gate_content_pass"
}
```

---

## Anti-patterns absolument interdits

```
✗ Un agent IA assigne STATUS=production_ready sans validation humaine
✗ Le pipeline continue si gate_niveau_1.pass == False
✗ Un fichier avec "placeholder" dans son nom ou ses sources passe le Gate Niveau 2
✗ Le manifest est absent lors de l'export final
✗ Le Gate est bypassé "pour aller vite" ou "pour tester"
✗ Le Gate est appliqué après l'upload (trop tard)
✗ Un REWORK sans motif précis (le motif guide la régénération)
```

---

## Règle fondamentale (à lire avant tout déploiement)

> **Le Quality Gate n'est pas une formalité. C'est la seule frontière
> entre un prototype interne et une vidéo publique portant le nom YAWatch-LUNA.**
>
> La Phase 14 a produit un diaporama de 34 secondes avec des images test
> et un zoom tremblant. Ce fichier a existé. Il aurait pu être publié.
> Il ne l'a pas été parce que Ludovic l'a vu avant.
>
> Ce document garantit que la vérification de Ludovic est toujours la
> dernière étape avant la publication — pas une option.
