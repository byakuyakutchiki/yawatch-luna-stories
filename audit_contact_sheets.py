"""Génère des planches de contact pour auditer les assets visuels."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ASSETS_DIR = Path("assets/luna_stories_assets")
OUTPUT_DIR = Path("audit_contact_sheets")

GROUPS = {
    "luna_adulte": [
        "01_luna_adulte/luna_adulte_reference_realiste_01.jpg",
        "01_luna_adulte/luna_adulte_neutral_9x16_01.png",
        "01_luna_adulte/luna_adulte_worried_9x16_01.png",
        "01_luna_adulte/luna_adulte_protective_luna_doll_01.png",
        "01_luna_adulte/luna_adulte_looking_out_window_01.png",
        "01_luna_adulte/luna_adulte_office_desk_01.png",
        "01_luna_adulte/luna_adulte_looking_at_turned_photo_01.png",
        "01_luna_adulte/luna_adulte_ceo_01.png",
        "01_luna_adulte/luna_adulte_ceo_03_portrait.png",
    ],
    "luna_enfant": [
        "00_assets_deja_dans_app/app_luna_enfant_current.png",
        "02_luna_enfant/luna_enfant_neutral_9x16_01.png",
        "02_luna_enfant/luna_enfant_worried_night_01.png",
        "02_luna_enfant/luna_enfant_comforted_with_doll_01.png",
        "02_luna_enfant/luna_enfant_chambre_poupee_01.png",
    ],
    "aby_adulte": [
        "03_aby/aby_character_sheet_01.png",
        "03_aby/aby_adulte_neutral_9x16_01.png",
        "03_aby/aby_adulte_observing_luna_01.png",
        "03_aby/aby_adulte_vulnerable_after_meeting_01.png",
        "03_aby/aby_adulte_controlled_anger_01.png",
        "03_aby/aby_adulte_bureau_public_realiste_01.png",
        "03_aby/aby_adulte_reunion_publique_collaborateurs_01.png",
        "03_aby/aby_adulte_privee_baie_vitree_dossier_01.png",
        "03_aby/aby_adulte_mains_referme_dossier_01.png",
    ],
    "aby_enfant": [
        "00_assets_deja_dans_app/app_aby_enfant_current.png",
        "03_aby/aby_enfant_canon_apk_maquette_ville_01.png",
        "03_aby/aby_enfant_main_jeton_noir_maquette_01.png",
    ],
    "malik": [
        "06_personnage_masculin_noir/personnage_masculin_noir_planche_reference_01.png",
        "06_personnage_masculin_noir/malik_adulte_neutral_canon_realiste_01.png",
        "06_personnage_masculin_noir/malik_adulte_travail_couloir_jour_01.png",
        "06_personnage_masculin_noir/personnage_masculin_noir_portrait_face_stresse_01.png",
        "06_personnage_masculin_noir/personnage_masculin_noir_portrait_trois_quarts_calme_01.png",
        "06_personnage_masculin_noir/personnage_masculin_noir_portrait_profil_01.png",
        "06_personnage_masculin_noir/personnage_masculin_noir_portrait_intense_02.png",
        "06_personnage_masculin_noir/personnage_masculin_noir_scene_salon_seul_01.png",
        "06_personnage_masculin_noir/personnage_masculin_noir_scene_fenetre_nuit_01.png",
        "06_personnage_masculin_noir/personnage_masculin_noir_photo_famille_floue_01.png",
        "06_personnage_masculin_noir/personnage_masculin_noir_avec_mere_01.png",
        "06_personnage_masculin_noir/personnage_masculin_noir_avec_pere_01.png",
        "06_personnage_masculin_noir/personnage_masculin_noir_avec_parents_01.png",
    ],
    "mere": [
        "10_famille_luna/luna_parents_portrait_officiel_yawatch_01.png",
        "10_famille_luna/luna_parents_cuisine_matin_01.png",
        "10_famille_luna/mere_luna_aby_neutral_9x16_01.png",
        "10_famille_luna/mere_luna_aby_worried_apartment_01.png",
        "10_famille_luna/mere_luna_aby_protective_memory_box_01.png",
        "10_famille_luna/mere_luna_aby_vulnerable_closed_box_01.png",
        "10_famille_luna/mere_transmet_boite_luna_adulte_01.png",
    ],
    "pere": [
        "10_famille_luna/luna_parents_portrait_officiel_yawatch_01.png",
        "10_famille_luna/luna_parents_cuisine_matin_01.png",
        "10_famille_luna/luna_pere_portrait_clan_01.png",
        "10_famille_luna/luna_pere_bureau_face_dossier_01.png",
        "10_famille_luna/luna_pere_bureau_verre_silence_01.png",
        "10_famille_luna/luna_pere_diner_tension_01.png",
        "10_famille_luna/luna_pere_intimidation_contact_01.png",
        "10_famille_luna/luna_pere_parking_lunettes_01.png",
        "10_famille_luna/luna_pere_appel_nuit_tour_eiffel_01.png",
    ],
    "secondaires": [
        "06_personnages_secondaires_a_valider/sophie_drh_yawatch_neutral_canon_01.png",
        "06_personnages_secondaires_a_valider/thomas_assistant_yawatch_neutral_canon_01.png",
        "06_personnages_secondaires_a_valider/personnage_stress_palette_01.jpg",
    ],
    "luna_doll": [
        "05_objets_symboliques_poupees/poupee_luna_violette_01.jpg",
        "05_objets_symboliques_poupees/poupee_luna_portrait_02.jpg",
        "05_objets_symboliques_poupees/poupee_luna_portrait_03.jpg",
        "05_objets_symboliques_poupees/poupee_luna_allongee_04.jpg",
        "05_objets_symboliques_poupees/poupee_luna_gros_plan_yeux_mystere_01.png",
        "06_personnage_masculin_noir/malik_jouet_symbolique_enfance_01.png",
    ],
    "visuels_cles_ep01": [
        "08_visuels_cles/ep01_aby_entre_bureau_luna_01.png",
        "08_visuels_cles/ep01_dialogue_luna_aby_cadre_retourne_01.png",
        "08_visuels_cles/ep01_mains_luna_arrete_aby_cadre_01.png",
        "08_visuels_cles/ep01_reflet_aby_observe_luna_vitre_01.png",
        "08_visuels_cles/ep01_luna_consulte_historique_yawatch_01.png",
        "08_visuels_cles/ep01_luna_seule_bureau_nuit_cadre_en_main_01.png",
        "08_visuels_cles/ep01_insert_cadre_presque_retourne_contenu_cache_01.jpg",
        "08_visuels_cles/ep01_flashback_porte_entrouverte_chambre_luna_01.png",
        "08_visuels_cles/luna_malik_conversation_cafe_la_defense_01.png",
        "08_visuels_cles/visuel_cle_luna_aby_malik_objets_01.png",
    ],
}


def make_contact_sheet(name, paths, thumb_w=360, thumb_h=640, margin=10):
    """Crée une planche de contact verticale 9:16."""
    valid_paths = []
    for p in paths:
        full = ASSETS_DIR / p
        if full.exists():
            valid_paths.append(full)
        else:
            print(f"[WARN] {full} non trouvé")

    if not valid_paths:
        print(f"[SKIP] {name}: aucune image")
        return

    cols = 3
    rows = math.ceil(len(valid_paths) / cols)

    sheet_w = cols * thumb_w + (cols + 1) * margin
    sheet_h = rows * (thumb_h + 60) + (rows + 1) * margin + 60

    sheet = Image.new("RGB", (sheet_w, sheet_h), (30, 30, 30))
    draw = ImageDraw.Draw(sheet)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except Exception:
        font = ImageFont.load_default()
        title_font = font

    draw.text((margin, margin), f"AUDIT — {name.upper()}", fill=(255, 255, 255), font=title_font)

    for i, img_path in enumerate(valid_paths):
        col = i % cols
        row = i // cols
        x = margin + col * (thumb_w + margin)
        y = margin + 60 + row * (thumb_h + 60 + margin)

        try:
            img = Image.open(img_path)
            img = img.convert("RGB")
            img.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)

            # Centrer dans la cellule
            paste_x = x + (thumb_w - img.width) // 2
            paste_y = y + (thumb_h - img.height) // 2
            sheet.paste(img, (paste_x, paste_y))

            # Nom du fichier
            label = img_path.name
            draw.text((x, y + thumb_h + 8), label, fill=(220, 220, 220), font=font)
        except Exception as e:
            draw.rectangle([x, y, x + thumb_w, y + thumb_h], outline=(255, 0, 0), width=2)
            draw.text((x + 10, y + 10), f"ERREUR\n{img_path.name}", fill=(255, 0, 0), font=font)
            print(f"[ERROR] {img_path}: {e}")

    output_path = OUTPUT_DIR / f"audit_{name}.jpg"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=90)
    print(f"[OK] {output_path} ({len(valid_paths)} images)")


if __name__ == "__main__":
    for name, paths in GROUPS.items():
        make_contact_sheet(name, paths)
