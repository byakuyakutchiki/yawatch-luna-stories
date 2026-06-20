"""Quality Gate — 3 plans tests YAWatch-LUNA.

Lancer depuis la VM Linux après que Codex a déposé les clips dans :
/media/windows/Users/saint/Desktop/PONT_LINUX_WINDOWS/resultats/clips_yawatch/

Usage :
    python3 run_quality_gate_3plans.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent

# Deux emplacements possibles pour les clips, dans l'ordre de priorité :
#   1. Dossier de dépôt du pont (si Codex copie les MP4 avec les noms exacts)
#   2. Dossier output natif de ComfyUI (chemin réel découvert sur Windows)
CLIPS_DIRS = [
    Path("/media/windows/Users/saint/Desktop/PONT_LINUX_WINDOWS/resultats/clips_yawatch"),
    Path("/media/windows/Users/saint/Documents/Codex/ComfyUI/output"),
]


def find_clip(filename: str) -> Path | None:
    """Cherche un clip par nom exact dans les deux emplacements connus."""
    for base in CLIPS_DIRS:
        candidate = base / filename
        if candidate.exists():
            return candidate
    return None

PLANS = [
    {
        "name": "Plan 02 — Luna adulte portrait",
        "file": "plan02_luna_adulte_portrait.mp4",
        "i2v_tool": "animatediff_sd15",
        "duration": 5.0,
        "challenge": "Stabilité visage adulte portrait serré",
    },
    {
        "name": "Plan 06 — Luna enfant + poupée",
        "file": "plan06_luna_enfant_poupee.mp4",
        "i2v_tool": "animatediff_sd15",
        "duration": 4.0,
        "challenge": "Visage enfant + texture tissu poupée",
    },
    {
        "name": "Plan 09 — Aby enfant + jeton noir",
        "file": "plan09_aby_jeton_noir.mp4",
        "i2v_tool": "animatediff_sd15",
        "duration": 4.0,
        "challenge": "Mains + objet + focus pull",
    },
]

def main():
    sys.path.insert(0, str(REPO_ROOT))
    from app.production_gatekeeper import ProductionGatekeeper
    from app.quality_gate import QualityGate

    gatekeeper = ProductionGatekeeper.load(strict=False)
    gate = QualityGate(gatekeeper)
    results = []

    print("\n" + "="*60)
    print("QUALITY GATE — 3 PLANS TESTS YAWATCH-LUNA")
    print("="*60)

    for plan in PLANS:
        clip_path = find_clip(plan["file"])

        if clip_path is None:
            print(f"\n❌ {plan['name']}")
            print(f"   FICHIER MANQUANT : {plan['file']}")
            print(f"   Cherché dans :")
            for base in CLIPS_DIRS:
                print(f"     - {base}")
            results.append({"plan": plan["name"], "status": "MISSING"})
            continue

        print(f"\n▶  {plan['name']}")
        print(f"   Fichier : {clip_path.name} ({clip_path.stat().st_size // 1024} KB)")
        print(f"   Challenge : {plan['challenge']}")

        context = {
            "i2v_tool": plan["i2v_tool"],
            "image_paths": [str(clip_path)],
            "plan_count": 1,
            "duration": plan["duration"],
            "audio_present": False,
        }

        try:
            report = gate.run(video_context=context)
            print(f"   Technique       : {report.verdict_technique.status}")
            print(f"   Mouvement       : {report.verdict_mouvement.status}")
            print(f"   Son             : {report.verdict_son.status}")
            print(f"   Cohérence       : {report.verdict_coherence_personnage.status}")
            print(f"   Statut actuel   : {report.current_status.value}")

            if report.verdict_technique.errors:
                for e in report.verdict_technique.errors:
                    print(f"   ⚠  {e}")

            passed = report.automatic_verdicts_pass
            results.append({
                "plan": plan["name"],
                "status": "AUTO_PASS" if passed else "AUTO_FAIL",
                "current_status": report.current_status.value,
            })
        except Exception as exc:
            print(f"   ERREUR quality gate : {exc}")
            results.append({"plan": plan["name"], "status": "ERROR", "error": str(exc)})

    print("\n" + "="*60)
    print("RÉSUMÉ")
    print("="*60)
    for r in results:
        icon = "✅" if r["status"] == "AUTO_PASS" else ("❌" if r["status"] == "AUTO_FAIL" else "⚠")
        print(f"  {icon}  {r['plan']} → {r['status']}")

    all_pass = all(r["status"] == "AUTO_PASS" for r in results)
    if all_pass:
        print("\n✅ Les 3 plans passent les verdicts automatiques.")
        print("   Prochaine étape : visionnage humain (Ludovic) → verdict storytelling.")
        print("   Puis : advance_to_candidat() si validé artistiquement.")
    else:
        print("\n❌ Un ou plusieurs plans ont échoué.")
        print("   Analyser les erreurs ci-dessus avant de relancer.")

    print("="*60 + "\n")


if __name__ == "__main__":
    main()
