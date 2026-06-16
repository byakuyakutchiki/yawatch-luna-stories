# Audit Photos — YAWatch Luna Stories

**Date :** 2026-06-16  
**Auditeur :** Kimi (remplaçant Codex)  
**Repo local :** `/home/ludo/PROJETS/YAWATCH_LUNA_STORIES`  
**Sources :** repo Codex copié depuis `/media/windows/Users/saint/Documents/Codex/2026-06-09/yawatch-luna-stories-public-yawatch-luna/work/yawatch-luna-stories`

---

## 🎯 Méthode

1. Copie du repo de Codex sur Linux.
2. Génération de planches de contact par personnage.
3. Analyse visuelle de chaque personnage : visage, âge, cheveux, tenue, émotion.
4. Vérification automatique des ratios 9:16 sur 167 images.

---

## ✅ Verdict global — Cohérence identitaire

| Personnage | Cohérence | Commentaire |
|---|---|---|
| **Luna adulte** | ✅ Très bonne | Toutes les images récentes (`neutral_9x16`, `worried`, `protective`, `looking_out_window`, `office_desk`, `looking_at_turned_photo`) montrent la MÊME femme. Référence `luna_adulte_neutral_9x16_01.png` est le canon prioritaire. |
| **Luna enfant** | ✅ Excellente | `neutral_9x16`, `worried_night`, `comforted_with_doll` : même fille brune, même visage, même pyjama bleu nuit. Très cohérente. |
| **Aby adulte** | ✅ Excellente | Toutes les images (`neutral_9x16`, `observing_luna`, `vulnerable`, `controlled_anger`, `bureau_public`, `reunion_publique`, `privee_baie_vitree`) : MÊME femme blonde, chignon haut, tailleur noir. |
| **Aby enfant** | ✅ Bonne | `app_aby_enfant_current.png` et `aby_enfant_canon_apk_maquette_ville_01.png` : même petite fille blonde. Distincte de Luna enfant (brune). |
| **Malik** | ⚠️ Deux familles | Les nouvelles images `malik_adulte_neutral_canon_realiste_01.png` et `malik_adulte_travail_couloir_jour_01.png` sont cohérentes entre elles. Les anciennes `personnage_masculin_noir_*` montrent le même homme mais avec un traitement plus dramatique/violet. Il faut choisir le canon principal. |
| **Mère de Luna/Aby** | ✅ Excellente | `neutral_9x16`, `worried_apartment`, `protective_memory_box`, `vulnerable_closed_box`, `mere_transmet_boite` : MÊME femme mature, cheveux bruns mi-courts, chemisier ivoire. |
| **Père de Luna** | ✅ Excellente | Toutes les images (`portrait_clan`, `bureau_face_dossier`, `bureau_verre_silence`, `diner_tension`, `intimidation_contact`, `parking_lunettes`, `appel_nuit_tour_eiffel`) : MÊME homme grisonnant, barbe, costume sombre. |
| **Sophie DRH** | ✅ Bonne | Cheveux courts poivre et sel, bien distincte de Luna et Aby. Version corrigée validée. |
| **Thomas assistant** | ✅ Bonne | Homme jeune brun, badge, style professionnel. |
| **Luna Doll** | ❌ Problème majeur | Plusieurs designs incompatibles : poupée porcelaine blonde (`poupee_luna_violette_01.jpg`) vs poupée tissu brune (`poupee_luna_gros_plan_yeux_mystere_01.png`). Le canon actuel est "tissu, cheveux bruns, robe violette". Il faut une référence propre cohérente. |

---

## ⚠️ Problèmes détectés

### 1. Format 16:9 au lieu de 9:16 (critique)

Beaucoup d'images générées récemment sont en **16:9 paysage** au lieu de **9:16 vertical**.  
**131 images sur 167** ne respectent pas le ratio 9:16 (tolérance 5%).

Exemples d'images importantes en 16:9 :

- `aby_adulte_bureau_public_realiste_01.png` (1672×941)
- `aby_adulte_reunion_publique_collaborateurs_01.png` (1672×941)
- `ep01_aby_entre_bureau_luna_01.png` (1672×941)
- `ep01_dialogue_luna_aby_cadre_retourne_01.png` (1672×941)
- `ep01_luna_consulte_historique_yawatch_01.png` (1672×941)
- `luna_malik_conversation_cafe_la_defense_01.png` (1672×941)
- `yawatch_cafeteria_jour_employes_01.png` (1672×941)
- `yawatch_hall_openspace_jour_realiste_sans_logo_01.png` (1672×941)

**Conséquence :** ces images ne sont pas directement utilisables pour des Shorts 9:16 sans recadrage lourd.

**Recommandation :** corriger les prompts pour forcer explicitement `vertical 9:16, 1080x1920` et vérifier que ChatGPT produit bien du portrait.

### 2. Luna Doll — designs divergents (critique)

| Image | Design |
|---|---|
| `poupee_luna_violette_01.jpg` | Poupée porcelaine, cheveux blonds, robe violette |
| `poupee_luna_gros_plan_yeux_mystere_01.png` | Poupée tissu, cheveux bruns, visage texturé |
| `poupee_luna_portrait_02.jpg` | Poupée ancienne sombre avec bébé |
| `poupee_luna_portrait_03.jpg` | Poupée blonde avec fleurs |

Le workflow officiel dit : *"Luna Doll reste exactement la même petite poupée artisanale en tissu : mêmes cheveux bruns en laine, même peau textile cousue"*.

**Recommandation :** générer une nouvelle référence canon propre de Luna Doll en tissu avec cheveux bruns et robe violette, puis supprimer ou archiver les anciennes versions porcelaine.

### 3. Malik — double traitement (mineur)

Les anciennes images `personnage_masculin_noir_*` ont un éclairage très violet/bleu nuit (style plus "banque d'image"). Les nouvelles `malik_adulte_*` sont plus naturelles et réalistes.

**Recommandation :** garder `malik_adulte_neutral_canon_realiste_01.png` comme référence prioritaire. Déplacer les anciennes `personnage_masculin_noir_*` dans un dossier `archive/` ou les marquer `[~]`.

### 4. Images anciennes CEO Luna (mineur)

`luna_adulte_ceo_01.png` et `luna_adulte_ceo_03_portrait.png` montrent une femme similaire mais avec un style plus "corporate glamour" et des logos YAWATCH explicites. Elles sont cohérentes mais moins naturelles que `luna_adulte_neutral_9x16_01.png`.

**Recommandation :** garder comme références secondaires, ne pas les utiliser comme canon principal.

---

## 📊 Résumé par personnage

### Luna adulte — canon validé

**Référence prioritaire :** `assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png`

Images cohérentes avec cette référence :
- `luna_adulte_worried_9x16_01.png` ✅
- `luna_adulte_protective_luna_doll_01.png` ✅
- `luna_adulte_looking_out_window_01.png` ✅
- `luna_adulte_office_desk_01.png` ✅
- `luna_adulte_looking_at_turned_photo_01.png` ✅

Images à utiliser avec précaution :
- `luna_adulte_reference_realiste_01.jpg` — style différent, lumière turquoise
- `luna_adulte_ceo_01.png` / `luna_adulte_ceo_03_portrait.png` — style plus corporate/ancien

### Aby adulte — canon validé

**Référence prioritaire :** `assets/luna_stories_assets/03_aby/aby_adulte_neutral_9x16_01.png`

Images cohérentes avec cette référence :
- `aby_adulte_observing_luna_01.png` ✅
- `aby_adulte_vulnerable_after_meeting_01.png` ✅
- `aby_adulte_controlled_anger_01.png` ✅
- `aby_adulte_bureau_public_realiste_01.png` ✅ (mais format 16:9)
- `aby_adulte_reunion_publique_collaborateurs_01.png` ✅ (mais format 16:9)
- `aby_adulte_privee_baie_vitree_dossier_01.png` ✅
- `aby_adulte_mains_referme_dossier_01.png` ✅ (pas de visage, mais tenue cohérente)

### Malik — canon à consolider

**Référence prioritaire recommandée :** `assets/luna_stories_assets/06_personnage_masculin_noir/malik_adulte_neutral_canon_realiste_01.png`

Images cohérentes avec cette référence :
- `malik_adulte_travail_couloir_jour_01.png` ✅

Images cohérentes mais traitement différent :
- `personnage_masculin_noir_portrait_face_stresse_01.png` ⚠️
- `personnage_masculin_noir_portrait_trois_quarts_calme_01.png` ⚠️
- `personnage_masculin_noir_portrait_profil_01.png` ⚠️
- `personnage_masculin_noir_scene_salon_seul_01.png` ⚠️
- etc.

### Mère — canon validé

**Référence prioritaire :** `assets/luna_stories_assets/10_famille_luna/mere_luna_aby_neutral_9x16_01.png`

Images cohérentes :
- `mere_luna_aby_worried_apartment_01.png` ✅
- `mere_luna_aby_protective_memory_box_01.png` ✅
- `mere_luna_aby_vulnerable_closed_box_01.png` ✅
- `mere_transmet_boite_luna_adulte_01.png` ✅

### Père — canon validé

**Référence prioritaire :** `assets/luna_stories_assets/10_famille_luna/luna_pere_portrait_clan_01.png`

Images cohérentes :
- `luna_pere_bureau_face_dossier_01.png` ✅
- `luna_pere_bureau_verre_silence_01.png` ✅
- `luna_pere_diner_tension_01.png` ✅
- `luna_pere_intimidation_contact_01.png` ✅
- `luna_pere_parking_lunettes_01.png` ✅ (mais format très large)
- `luna_pere_appel_nuit_tour_eiffel_01.png` ✅

---

## 🔧 Actions recommandées immédiates

1. **Corriger les prompts pour forcer le format 9:16** dans tous les futurs prompts.
2. **Régénérer Luna Doll** avec un design unique en tissu, cheveux bruns, robe violette.
3. **Choisir le canon Malik** et archiver les anciennes versions trop dramatiques.
4. **Recadrer ou regénérer** les images clés en 16:9 (EP01, Aby public, Malik/Luna café, etc.).
5. **Mettre à jour `CATALOGUE_ASSETS_LUNA_STORIES.md`** avec les statuts `[x]` / `[~]` / `[ ]` et les références canoniques.

---

## 📎 Fichiers générés

- `audit_contact_sheets/audit_*.jpg` — planches de contact par personnage
- `audit_assets_dimensions.csv` — dimensions et ratios de toutes les images
- `AUDIT_PHOTOS_KIMI_2026-06-16.md` — ce rapport
