# Résultat FramePack — PLAN02 Luna adulte — RunPod Cloud (run 001)

Date : 2026-06-21
Statut : SUCCESS_MP4 + I2V_QUALITY_GATE_PASS
Pour audit : DeepSeek (coordinateur)

## Provenance

| Champ | Valeur |
|---|---|
| Environnement | RunPod Pod (cloud) |
| GPU | NVIDIA RTX PRO 4500 Blackwell, 32 Go VRAM |
| Moteur | FramePack (HunyuanVideo) via ComfyUI-FramePackWrapper |
| Workflow | `framepack_plan02_luna_api_test_001.json` (API, inchangé) |
| Image source | `luna.png` = `assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png` (md5 d0696611...) |
| Modèle | FramePackI2V_HY_fp8_e4m3fn + hunyuan_video_vae_bf16 + sigclip_vision_patch14_384 + clip_l + llava_llama3_fp16 |
| Seed | 2406202621 |
| Steps / CFG / Guidance / Sampler | 20 / 1.0 / 10.0 / unipc_bh1 |
| Temps de génération | 348 s (~5 min 48 s) |

Comparaison vitesse : ~348 s sur RunPod RTX PRO 4500 vs ~1776 s sur RTX 4060 locale (même workflow).

## Sortie vidéo (ffprobe)

| Champ | Valeur |
|---|---|
| Codec | h264 |
| Résolution | 480x832 (9:16) |
| Pixel format | yuv420p |
| FPS | 16 |
| Frames | 145 |
| Durée | 9.0625 s |

Note : durée réelle 9.06 s alors que `total_second_length=5.0` demandé — comportement FramePack connu (logique de fenêtres latentes), à maîtriser avant production.

## Quality Gate I2V — verdict automatique : PASS

| Métrique | Mesuré | Seuil | Verdict |
|---|---|---|---|
| face_identity_ssim_min | 0.9552 | >= 0.85 | PASS |
| face_lighting_peak_to_peak_pct | 11.1989 | <= 15.0 | PASS |
| face_flicker_mean_abs_delta | 0.1694 | <= 0.5 | PASS |

Rapport machine complet : `YAWATCH_FRAMEPACK_PLAN02_LUNA_TEST_00001.i2v_quality_gate.json`

## Limite (gouvernance)

L'avis automatique n'est PAS l'approbation finale. Le visionnage humain de Ludovic reste obligatoire
(respiration, cou/épaules, cheveux, émotion, sensation cinématographique). Plans restants à générer en
FramePack cloud : plan06 (Luna enfant + poupée), plan09 (Aby enfant + jeton).
