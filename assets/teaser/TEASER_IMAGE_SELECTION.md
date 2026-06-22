# Teaser Luna - selection plan01-09

Objectif: preparer les 9 images sources du teaser YAWatch-LUNA pour generation I2V locale.

Regle: les fichiers `plan01.png` a `plan09.png` determinent l'ordre du teaser.

## Selection

| Plan | Fichier source | Correspondance prompt | Statut |
| --- | --- | --- | --- |
| plan01 | `assets/luna_stories_assets/01_luna_adulte/luna_adulte_determination_9x16_01.png` | Luna determinee, plan large/poitrine, energie de marche possible | OK |
| plan02 | `assets/luna_stories_assets/01_luna_adulte/luna_adulte_looking_out_window_01.png` | Luna s'arrete, regarde a droite/hors champ | OK |
| plan03 | `assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png` | Gros plan neutre, respiration et micro-mouvements | OK |
| plan04 | `assets/luna_stories_assets/01_luna_adulte/luna_adulte_worried_9x16_01.png` | Se retourne / cheveux au vent | A ameliorer: image emotionnelle correcte, mais pas un vrai plan large cheveux au vent |
| plan05 | `assets/luna_stories_assets/01_luna_adulte/luna_adulte_office_desk_01.png` | Mains / posture pensive | OK, mais pas mains dans les poches |
| plan06 | `assets/luna_stories_assets/01_luna_adulte/luna_adulte_looking_at_turned_photo_01.png` | Gros plan hesitation, tension intime | OK |
| plan07 | `assets/luna_stories_assets/01_luna_adulte/luna_adulte_ceo_03_portrait.png` | Confiance, avance vers la camera possible en I2V | OK |
| plan08 | `assets/luna_stories_assets/01_luna_adulte/luna_adulte_ceo_01.png` | Regard intense, posture dirigeante | OK |
| plan09 | `assets/luna_stories_assets/01_luna_adulte/luna_adulte_ceo_02_landscape.png` | Sourire leger / respiration profonde | A ameliorer: image premium, mais sourire peu visible |

## Validation

- 9 images presentes exactement: `plan01.png` a `plan09.png`.
- Toutes les images sont au format PNG.
- Toutes les images depassent 512x512.
- Luna adulte uniquement: aucune image avec Aby, Malik ou un autre personnage visible n'a ete retenue.
- Aucune retouche, aucun filtre, aucune generation nouvelle.

## Notes pour MotionDirector

Les prompts existants peuvent etre utilises tels quels pour un premier test.

Pour une version plus stricte, il faudra idealement produire/remplacer:

1. `plan04.png`: Luna en plan plus large, se retournant, cheveux en mouvement.
2. `plan09.png`: Luna gros plan ou plan poitrine avec sourire tres leger, respiration profonde.

Ces deux remplacements ne bloquent pas le test technique sur RTX 4060, mais ils amelioreraient la coherence artistique du teaser.
