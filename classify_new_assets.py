"""Classe les nouvelles images validées dans le repo."""

from pathlib import Path
import shutil

DOWNLOADS_DIR = Path("/media/windows/Users/saint/Downloads")
REPO_DIR = Path("/home/ludo/PROJETS/YAWATCH_LUNA_STORIES")

# Mapping : (timestamp_partiel_fichier_source, destination_dans_repo)
VALIDATED = [
    # 23:53:19 — Hall YAWatch vivant
    ("11_53_19 PM.png", "assets/luna_stories_assets/09_decors_paris_la_defense/pack_01_yawatch_industries/yawatch_hall_vivant_9x16_01.png"),
    # 23:53:09 — Mère inquiète discrète
    ("11_53_09 PM.png", "assets/luna_stories_assets/10_famille_luna/mere_luna_aby_inquietude_discrete_9x16_01.png"),
    # 23:53:03 — Mère inquiète variante
    ("11_53_03 PM.png", "assets/luna_stories_assets/10_famille_luna/mere_luna_aby_inquietude_discrete_variante_01.png"),
    # 23:52:52 — Luna détermination
    ("11_52_52 PM.png", "assets/luna_stories_assets/01_luna_adulte/luna_adulte_determination_9x16_01.png"),
    # 23:52:39 — Luna + Malik café
    ("11_52_39 PM.png", "assets/luna_stories_assets/08_visuels_cles/luna_malik_cafe_la_defense_9x16_01.png"),
    # 23:52:11 — Malik portrait appartement
    ("11_52_11 PM.png", "assets/luna_stories_assets/06_personnage_masculin_noir/malik_adulte_portrait_appartement_9x16_01.png"),
    # 23:52:02 — Aby stratégique froide
    ("11_52_02 PM.png", "assets/luna_stories_assets/03_aby/aby_adulte_strategique_froide_9x16_01.png"),
    # 23:51:57 — Luna Doll canon tissu
    ("11_51_57 PM.png", "assets/luna_stories_assets/05_objets_symboliques_poupees/poupee_luna_canon_tissu_propre_9x16_01.png"),
]

for partial_name, dest_rel in VALIDATED:
    # Trouver le fichier source exact
    matches = [f for f in DOWNLOADS_DIR.iterdir() if partial_name in f.name and f.suffix.lower() in (".png", ".jpg", ".jpeg")]
    if not matches:
        print(f"[ERREUR] Source non trouvée pour : {partial_name}")
        continue
    if len(matches) > 1:
        print(f"[ATTENTION] Plusieurs correspondances pour {partial_name}: {[m.name for m in matches]}")
        continue

    src = matches[0]
    dest = REPO_DIR / dest_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"[COPIE] {src.name} -> {dest}")

print("\nClassification terminée.")
