"""Validation niveau CLIP — 3 plans tests YAWatch-LUNA.

IMPORTANT — distinction de niveau :
  Le Quality Gate à 6 verdicts (app/quality_gate.py) vise le SHORT FINAL ASSEMBLÉ
  (9 plans + audio + sous-titres). Un clip I2V BRUT n'a pas encore de son ni de
  montage — ils arrivent à l'étape d'assemblage (étape 11 du master plan).

  Ce script valide donc ce qui est pertinent pour un CLIP BRUT :
    1. Technique vidéo (résolution, codec, pix_fmt, fps) — sans exiger l'audio
    2. Mouvement (vient d'un vrai outil I2V, ratio Ken Burns)
    3. Cohérence personnage (pas de placeholder, asset canon)

  Les verdicts "son" et "montage" sont marqués N/A — ils s'appliquent au Short
  assemblé, pas au clip. Ils seront évalués par QualityGate.run() après assemblage.

Lancer depuis la VM Linux après dépôt des clips.
Usage :
    python3 run_quality_gate_3plans.py
"""
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent

CLIPS_DIRS = [
    Path("/media/windows/Users/saint/Desktop/PONT_LINUX_WINDOWS/resultats/clips_yawatch"),
    Path("/media/windows/Users/saint/Documents/Codex/ComfyUI/output"),
]

# Critères techniques niveau CLIP (audio non requis — il vient à l'assemblage)
REQUIRED_WIDTH = 1080
REQUIRED_HEIGHT = 1920
REQUIRED_VIDEO_CODEC = "h264"
REQUIRED_PIX_FMT = "yuv420p"
REQUIRED_FPS = 25
FPS_TOLERANCE = 0.5

PLANS = [
    {
        "name": "Plan 02 — Luna adulte portrait",
        "file": "plan02_luna_adulte_portrait.mp4",
        "source_image": "yawatch_plan02_luna_adulte_portrait",
        "i2v_tool": "animatediff",
        "challenge": "Stabilité visage adulte portrait serré",
    },
    {
        "name": "Plan 06 — Luna enfant + poupée",
        "file": "plan06_luna_enfant_poupee.mp4",
        "source_image": "luna_enfant_comforted_with_doll_01",
        "i2v_tool": "animatediff",
        "challenge": "Visage enfant + texture tissu poupée",
    },
    {
        "name": "Plan 09 — Aby enfant + jeton noir",
        "file": "plan09_aby_jeton_noir.mp4",
        "source_image": "aby_enfant_main_jeton_noir_maquette_01",
        "i2v_tool": "animatediff",
        "challenge": "Mains + objet + focus pull",
    },
]


def find_clip(filename: str):
    for base in CLIPS_DIRS:
        candidate = base / filename
        if candidate.exists():
            return candidate
    return None


def probe_clip(clip_path: Path) -> dict:
    """ffprobe minimal — flux vidéo + durée. Audio non requis au niveau clip."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json",
         "-show_streams", "-show_format", str(clip_path)],
        capture_output=True, text=True, timeout=20,
    )
    if result.returncode != 0:
        return {}
    return json.loads(result.stdout)


def check_technique_clip(clip_path: Path) -> tuple[str, list]:
    """Vérifie les specs vidéo d'un clip brut (sans exiger l'audio)."""
    errors = []
    probe = probe_clip(clip_path)
    if not probe:
        return "FAIL", ["FFprobe ne peut pas lire le fichier."]

    video = next((s for s in probe.get("streams", []) if s.get("codec_type") == "video"), None)
    if not video:
        return "FAIL", ["Aucun flux vidéo détecté."]

    w, h = video.get("width", 0), video.get("height", 0)
    if (w, h) != (REQUIRED_WIDTH, REQUIRED_HEIGHT):
        errors.append(f"Résolution {w}×{h} (requis {REQUIRED_WIDTH}×{REQUIRED_HEIGHT}).")

    if video.get("codec_name") != REQUIRED_VIDEO_CODEC:
        errors.append(f"Codec {video.get('codec_name')} (requis {REQUIRED_VIDEO_CODEC}).")

    if video.get("pix_fmt") != REQUIRED_PIX_FMT:
        errors.append(f"Pix_fmt {video.get('pix_fmt')} (requis {REQUIRED_PIX_FMT}).")

    num, den = (video.get("r_frame_rate", "0/1").split("/") + ["1"])[:2]
    fps = float(num) / float(den) if float(den) else 0
    if abs(fps - REQUIRED_FPS) > FPS_TOLERANCE:
        errors.append(f"FPS {fps:.2f} (requis {REQUIRED_FPS}±{FPS_TOLERANCE}).")

    return ("FAIL" if errors else "PASS"), errors


def main():
    sys.path.insert(0, str(REPO_ROOT))
    from app.production_gatekeeper import ProductionGatekeeper

    gk = ProductionGatekeeper.load(strict=False)
    results = []

    print("\n" + "=" * 64)
    print("VALIDATION NIVEAU CLIP — 3 PLANS TESTS YAWATCH-LUNA")
    print("=" * 64)

    for plan in PLANS:
        clip_path = find_clip(plan["file"])

        if clip_path is None:
            print(f"\n⏳ {plan['name']} → PAS ENCORE GÉNÉRÉ ({plan['file']})")
            results.append({"plan": plan["name"], "status": "MISSING"})
            continue

        size_kb = clip_path.stat().st_size // 1024
        print(f"\n▶  {plan['name']}")
        print(f"   Fichier   : {clip_path.name} ({size_kb} KB)")
        print(f"   Challenge : {plan['challenge']}")

        # 1. Technique vidéo (niveau clip)
        tech_status, tech_errors = check_technique_clip(clip_path)
        print(f"   [1] Technique vidéo   : {tech_status}")
        for e in tech_errors:
            print(f"        ⚠ {e}")

        # 2. Mouvement (rôle MotionEngineer)
        motion = gk.motion_engineer.validate({
            "clips": [str(clip_path)],
            "ken_burns_count": 0,
            "total_plans": 1,
            "i2v_tool": plan["i2v_tool"],
        })
        print(f"   [2] Mouvement         : {motion.status}")
        for e in motion.errors:
            print(f"        ⚠ {e}")

        # 3. Cohérence personnage (rôle VideoGenerationEngineer)
        coherence = gk.video_generation_engineer.validate({
            "clips": [str(clip_path)],
            "source_images": [plan["source_image"]],
            "i2v_tool": plan["i2v_tool"],
        })
        print(f"   [3] Cohérence         : {coherence.status}")
        for e in coherence.errors:
            print(f"        ⚠ {e}")

        # Son + montage : niveau assemblage, non applicable à un clip brut
        print(f"   [—] Son / Montage     : N/A (étape assemblage du Short final)")

        clip_ok = (tech_status == "PASS"
                   and motion.status == "PASS"
                   and coherence.status == "PASS")
        results.append({
            "plan": plan["name"],
            "status": "CLIP_VALIDE" if clip_ok else "CLIP_REJETE",
        })

    print("\n" + "=" * 64)
    print("RÉSUMÉ")
    print("=" * 64)
    for r in results:
        icon = {"CLIP_VALIDE": "✅", "CLIP_REJETE": "❌", "MISSING": "⏳"}[r["status"]]
        print(f"  {icon}  {r['plan']} → {r['status']}")

    generated = [r for r in results if r["status"] != "MISSING"]
    valid = [r for r in results if r["status"] == "CLIP_VALIDE"]

    print()
    if generated and len(valid) == len(generated):
        print(f"✅ {len(valid)}/{len(generated)} clip(s) généré(s) valide(s) au niveau CLIP.")
        print("   Le moteur local produit des clips techniquement conformes.")
        print("   Prochaine étape : visionnage humain (Ludovic) pour juger l'ART")
        print("   (stabilité visage, émotion) — le code ne juge pas ça.")
    elif generated:
        print(f"❌ {len(valid)}/{len(generated)} clip(s) valide(s). Voir les ⚠ ci-dessus.")
    else:
        print("⏳ Aucun clip généré pour l'instant.")
    print("=" * 64 + "\n")


if __name__ == "__main__":
    main()
