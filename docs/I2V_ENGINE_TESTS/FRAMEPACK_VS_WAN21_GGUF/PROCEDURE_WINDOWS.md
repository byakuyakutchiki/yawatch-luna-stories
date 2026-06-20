# Procedure Windows — Test FramePack vs Wan2.1 GGUF

Chemin ComfyUI attendu:

```powershell
C:\Users\saint\Documents\Codex\ComfyUI
```

## Phase 0 — Etat initial

Executer:

```powershell
.\scripts\verify_install.ps1
```

Resultat attendu avant installation:

- ComfyUI existe.
- GPU CUDA deja valide.
- FramePack custom node absent ou non valide.
- ComfyUI-GGUF custom node absent ou non valide.
- Modeles FramePack/Wan absents.

## Phase 1 — Installer les custom nodes

Depuis ce dossier de kit:

```powershell
.\scripts\install_custom_nodes.ps1
```

Puis redemarrer ComfyUI.

## Phase 2 — Telecharger les modeles

Executer:

```powershell
.\scripts\download_models.ps1 -Engine framepack
.\scripts\download_models.ps1 -Engine wan
```

Si l'espace disque devient critique, priorite:

1. FramePack seul.
2. Wan Q4 au lieu de Wan Q5.
3. Ne pas garder les deux moteurs si Windows passe sous 40 Go libres.

## Phase 3 — Verifier l'installation

Executer:

```powershell
.\scripts\verify_install.ps1
```

Puis lancer ComfyUI et verifier:

```text
http://127.0.0.1:8188/object_info
```

Regle bloquante: si les noeuds FramePack ou GGUF ne sont pas presents dans `/object_info`, ne pas generer.

## Phase 4 — Workflow FramePack

1. Copier l'image canonique Luna adulte vers:

```powershell
C:\Users\saint\Documents\Codex\ComfyUI\input\yawatch_plan02_luna_adulte_portrait.png
```

2. Charger dans ComfyUI un workflow officiel trouve dans:

```powershell
C:\Users\saint\Documents\Codex\ComfyUI\custom_nodes\ComfyUI-FramePackWrapper\example_workflows
```

3. Adapter uniquement:

- image source
- prompt positif
- prompt negatif
- seed
- duree cible 5 secondes
- sortie `YAWATCH_FRAMEPACK_PLAN02_LUNA`

4. Generer un MP4.

## Phase 5 — Workflow Wan2.1 GGUF

1. Charger un workflow Wan I2V compatible GGUF.
2. Adapter uniquement:

- image source
- modele GGUF Q5 ou Q4
- prompt positif
- prompt negatif
- seed
- duree cible 5 secondes
- sortie `YAWATCH_WAN21_GGUF_PLAN02_LUNA`

3. Generer un MP4.

## Prompt commun

Prompt positif:

```text
cinematic premium psychological thriller portrait of Luna, adult woman, same identity as source image, subtle natural breathing, imperceptible slow push-in, restrained emotion, calm serious gaze, Paris La Defense office atmosphere, realistic skin, natural hair movement, shallow depth of field, film grain, high quality, no text
```

Prompt negatif:

```text
different person, identity change, face swap, deformed face, distorted eyes, asymmetric eyes, melting face, bad anatomy, extra fingers, fused fingers, child, teen, glamour, sexualized, cartoon, anime, cyberpunk, neon, purple dominant lighting, text, watermark, logo, low quality, heavy flicker, jitter, violent motion
```

## Phase 6 — Comparaison

Pour chaque MP4:

- mesurer duree, resolution, fps;
- extraire une planche de frames;
- regarder le MP4 en lecture reelle;
- remplir `EVALUATION_SHEET.md`;
- ne retenir aucun moteur sans validation humaine Ludovic.

