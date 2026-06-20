# Governance Rules — I2V Engine Candidate Test

## Roles

Linux / repo:

- conserve les bibliotheques;
- prepare les prompts;
- archive les manifests et resultats;
- compare les sorties;
- garde le statut moteur.

Windows / ComfyUI:

- installe les modeles;
- execute les workflows;
- produit les MP4 et logs;
- ne decide pas du moteur gagnant.

## Regles bloquantes

1. Aucun moteur n'est declare `VALIDATED` sans MP4 regarde.
2. Aucun workflow n'est execute si les noeuds attendus ne sont pas presents dans `/object_info`.
3. Aucun fallback silencieux n'est autorise.
4. Si Wan Q5 tombe en OOM, le resultat est `FAILED_Q5_VRAM`, pas `Wan valide`.
5. Si FramePack autodownload un modele different du manifest, le rapport doit l'indiquer.
6. La comparaison doit etre faite sur la meme image et le meme prompt.
7. La duree cible est 5 secondes; un test 2 secondes ne valide pas la stabilite visage.
8. Le gagnant provisoire doit repasser par le Quality Gate YAWatch avant integration dans `I2V_ENGINE`.

## Statuts autorises

- `NOT_INSTALLED`
- `INSTALLED_NOT_VERIFIED`
- `WORKFLOW_LOADS`
- `MP4_GENERATED`
- `QUALITY_REJECTED`
- `LUDOVIC_REJECTED`
- `CANDIDATE_APPROVED`
- `I2V_ENGINE_SELECTED`

## Interdiction

Ne pas modifier le pipeline episode pour brancher FramePack ou Wan avant que le test PLAN02 soit valide.

