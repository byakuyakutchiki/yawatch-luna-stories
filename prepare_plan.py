"""Orchestrateur de gouvernance — prépare un plan de bout en bout (côté Linux).

Concrétise le flux :
    bibliothèques → MotionDirector → VideoJob → (stage image + job JSON) → backend Windows

Ce script NE génère PAS de vidéo. Il prépare tout pour que le backend Windows
exécute, puis affiche la commande à lancer côté Windows.

Usage :
    python3 prepare_plan.py plan06
    python3 prepare_plan.py plan09
"""
import json
import shutil
import sys
from dataclasses import asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

# Pont Linux → Windows (mount vboxsf)
BRIDGE = Path("/media/windows/Users/saint/Desktop/PONT_LINUX_WINDOWS")
BRIDGE_SOURCES = BRIDGE / "sources"
BRIDGE_CLIPS = BRIDGE / "resultats" / "clips_yawatch"
WIN_FACTORY_JOBS = Path("/media/windows/Users/saint/Documents/Codex/ComfyUI/yawatch_factory/jobs")

# Chemins Windows (vus par le backend qui tourne sur Windows)
WIN_SOURCES = r"C:\Users\saint\Desktop\PONT_LINUX_WINDOWS\sources"
WIN_CLIPS = r"C:\Users\saint\Desktop\PONT_LINUX_WINDOWS\resultats\clips_yawatch"
WIN_FACTORY = r"C:\Users\saint\Documents\Codex\ComfyUI\yawatch_factory"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage : python3 prepare_plan.py <plan_id>   (ex: plan06)")
        return 2

    plan_id = sys.argv[1]

    sys.path.insert(0, str(REPO_ROOT))
    from app.motion_director import MotionDirector, TargetPaths

    # 1. La connaissance d'abord — le MotionDirector vérifie les bibliothèques
    director = MotionDirector(strict=True)
    if plan_id not in director.available_plans():
        print(f"Plan inconnu : {plan_id}. Disponibles : {director.available_plans()}")
        return 1

    print("=" * 64)
    print(f"PRÉPARATION GOUVERNÉE — {plan_id}")
    print("=" * 64)
    print(director.describe_plan(plan_id))
    print()

    # 2. Le MotionDirector prépare le VideoJob (pilote par les profils)
    target = TargetPaths(sources_dir=WIN_SOURCES, deposit_dir=WIN_CLIPS)
    job = director.prepare_job(plan_id, target)

    # 3. Staging de l'image canonique vers le pont (Linux → Windows)
    plan_meta = director._plans[plan_id]
    canonical = REPO_ROOT / plan_meta["canonical_image"]
    if not canonical.exists():
        print(f"❌ Image canonique introuvable : {canonical}")
        return 1
    BRIDGE_SOURCES.mkdir(parents=True, exist_ok=True)
    staged = BRIDGE_SOURCES / f"{plan_meta['image_stem']}.png"
    shutil.copy2(canonical, staged)
    print(f"[stage] Image → {staged.name}")

    # 4. Écriture du job JSON côté Windows (factory)
    WIN_FACTORY_JOBS.mkdir(parents=True, exist_ok=True)
    job_file = WIN_FACTORY_JOBS / f"{plan_id}.json"
    job_file.write_text(json.dumps(asdict(job), indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[job]   JSON → {job_file.name}")
    BRIDGE_CLIPS.mkdir(parents=True, exist_ok=True)

    # 5. Commande à exécuter côté Windows (le backend exécute, ne décide rien)
    print()
    print("─" * 64)
    print("PRÊT. Commande à lancer côté WINDOWS (Codex) :")
    print()
    print(f'  C:\\Users\\saint\\Documents\\Codex\\ComfyUI\\.venv\\Scripts\\python.exe ^')
    print(f'    {WIN_FACTORY}\\comfyui_backend.py ^')
    print(f'    --job {WIN_FACTORY}\\jobs\\{plan_id}.json')
    print()
    if job.use_ipadapter:
        print("  ⚠ Ce plan utilise l'IPAdapter — vérifier d'abord que Windows a :")
        print("    - le custom node ComfyUI_IPAdapter_plus installé")
        print("    - ip-adapter_sd15.safetensors dans models/ipadapter/")
        print("    - le CLIP vision dans models/clip_vision/")
        print("    (voir commandes/YAWATCH_INSTALL_IPADAPTER.bat)")
    print("─" * 64)
    print()
    print("Après génération, côté Linux :  python3 run_quality_gate_3plans.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
