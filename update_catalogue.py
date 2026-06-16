"""Met à jour le catalogue d'assets avec les nouvelles images."""

from pathlib import Path
import re

CATALOGUE_PATH = Path("assets/luna_stories_assets/CATALOGUE_ASSETS_LUNA_STORIES.md")

text = CATALOGUE_PATH.read_text(encoding="utf-8")

# Nouvelles entrées à ajouter dans la section "Assets classes"
new_entries = """- `01_luna_adulte/luna_adulte_neutral_9x16_01.png` - Nouvelle référence canonique prioritaire de Luna adulte (portrait vertical 9:16).
- `01_luna_adulte/luna_adulte_determination_9x16_01.png` - Luna adulte, émotion détermination contenue, vertical 9:16. ✅ Validé le 16 juin 2026.
- `01_luna_adulte/luna_adulte_worried_9x16_01.png` - Luna adulte, émotion worried, vertical 9:16.
- `01_luna_adulte/luna_adulte_protective_luna_doll_01.png` - Luna adulte protectrice avec Luna Doll.
- `01_luna_adulte/luna_adulte_looking_out_window_01.png` - Luna adulte regardant Paris de nuit.
- `01_luna_adulte/luna_adulte_office_desk_01.png` - Luna adulte à son bureau avec Luna Doll.
- `01_luna_adulte/luna_adulte_looking_at_turned_photo_01.png` - Luna adulte regardant une photo retournée.
- `02_luna_enfant/luna_enfant_neutral_9x16_01.png` - Nouvelle référence canonique prioritaire de Luna enfant (portrait vertical 9:16).
- `02_luna_enfant/luna_enfant_worried_night_01.png` - Luna enfant inquiète la nuit.
- `02_luna_enfant/luna_enfant_comforted_with_doll_01.png` - Luna enfant rassurée avec Luna Doll.
- `03_aby/aby_adulte_neutral_9x16_01.png` - Nouvelle référence canonique prioritaire d'Aby adulte (portrait vertical 9:16).
- `03_aby/aby_adulte_observing_luna_01.png` - Aby observe Luna en réunion.
- `03_aby/aby_adulte_vulnerable_after_meeting_01.png` - Aby vulnérable après une réunion.
- `03_aby/aby_adulte_controlled_anger_01.png` - Aby colère contrôlée.
- `03_aby/aby_adulte_bureau_public_realiste_01.png` - Aby en contexte public réaliste (format paysage, à recadrer ou regénérer).
- `03_aby/aby_adulte_reunion_publique_collaborateurs_01.png` - Aby en réunion avec collaborateurs (format paysage, à recadrer ou regénérer).
- `03_aby/aby_adulte_privee_baie_vitree_dossier_01.png` - Aby seule, baie vitrée, dossier.
- `03_aby/aby_adulte_mains_referme_dossier_01.png` - Gros plan mains d'Aby refermant un dossier.
- `03_aby/aby_adulte_strategique_froide_9x16_01.png` - Aby stratégique froide, vertical 9:16. ✅ Validé le 16 juin 2026.
- `05_objets_symboliques_poupees/poupee_luna_canon_tissu_propre_9x16_01.png` - Nouvelle référence canonique propre de Luna Doll : poupée artisanale en tissu, cheveux bruns, robe violette. ✅ Validée le 16 juin 2026.
- `06_personnage_masculin_noir/malik_adulte_neutral_canon_realiste_01.png` - Nouvelle référence canonique prioritaire de Malik adulte au présent.
- `06_personnage_masculin_noir/malik_adulte_travail_couloir_jour_01.png` - Malik au travail en journée.
- `06_personnage_masculin_noir/malik_jouet_symbolique_enfance_01.png` - Jouet symbolique de Malik.
- `06_personnage_masculin_noir/malik_adulte_portrait_appartement_9x16_01.png` - Malik portrait appartement, vertical 9:16. ✅ Validé le 16 juin 2026.
- `06_personnages_secondaires_a_valider/sophie_drh_yawatch_neutral_canon_01.png` - Sophie DRH, cheveux courts poivre et sel, distincte de Luna.
- `06_personnages_secondaires_a_valider/thomas_assistant_yawatch_neutral_canon_01.png` - Thomas assistant YAWatch.
- `08_visuels_cles/luna_malik_conversation_cafe_la_defense_01.png` - Luna et Malik au café, Luna de dos/trois-quarts. ✅ Validé.
- `08_visuels_cles/luna_malik_cafe_la_defense_9x16_01.png` - Luna et Malik au café, vertical 9:16. ✅ Validé le 16 juin 2026.
- `09_decors_paris_la_defense/pack_01_yawatch_industries/yawatch_hall_openspace_jour_realiste_sans_logo_01.png` - Hall/open space YAWatch vivant (format paysage).
- `09_decors_paris_la_defense/pack_01_yawatch_industries/yawatch_hall_vivant_9x16_01.png` - Hall YAWatch vivant, vertical 9:16. ✅ Validé le 16 juin 2026.
- `10_famille_luna/mere_luna_aby_neutral_9x16_01.png` - Nouvelle référence canonique prioritaire de la mère.
- `10_famille_luna/mere_luna_aby_worried_apartment_01.png` - Mère inquiète dans son appartement.
- `10_famille_luna/mere_luna_aby_protective_memory_box_01.png` - Mère protectrice avec la boîte à souvenirs.
- `10_famille_luna/mere_luna_aby_vulnerable_closed_box_01.png` - Mère vulnérable, boîte fermée.
- `10_famille_luna/mere_transmet_boite_luna_adulte_01.png` - Mère transmet la boîte à Luna adulte.
- `10_famille_luna/mere_luna_aby_inquietude_discrete_9x16_01.png` - Mère inquiétude discrète, vertical 9:16. ✅ Validée le 16 juin 2026.
- `10_famille_luna/mere_luna_aby_inquietude_discrete_variante_01.png` - Variante de la mère inquiète. ✅ Validée comme variante.
"""

# Insérer après la ligne "## Assets classes"
if "## Assets classes" in text:
    parts = text.split("## Assets classes", 1)
    text = parts[0] + "## Assets classes\n" + new_entries + "\n" + parts[1]

# Mettre à jour les compteurs de dossiers
counters = {
    "01_luna_adulte": 11,
    "02_luna_enfant": 5,
    "03_aby": 12,
    "05_objets_symboliques_poupees": 6,
    "06_personnage_masculin_noir": 15,
    "06_personnages_secondaires_a_valider": 3,
    "08_visuels_cles": 13,
    "09_decors_paris_la_defense": 1,
    "10_famille_luna": 12,
}

for folder, count in counters.items():
    pattern = rf"- `{re.escape(folder)}` : \d+ fichier\(s\)"
    replacement = f"- `{folder}` : {count} fichier(s)"
    text = re.sub(pattern, replacement, text)

# Mettre à jour la date
text = re.sub(r"Derniere mise a jour : \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", "Derniere mise a jour : 2026-06-16T23:55:00", text)

CATALOGUE_PATH.write_text(text, encoding="utf-8")
print("Catalogue mis à jour.")
