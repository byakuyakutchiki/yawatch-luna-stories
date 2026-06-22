# Expérience : wan_restore

**Question :** La restauration GFPGAN sauve-t-elle l identite de Wan sans casser le mouvement ?

| label | ssim_face_min | lighting_face_pct | flicker_face | flow_full | translation_risk | organic_score | gate_passed |
|---|---|---|---|---|---|---|---|
| wan_clip__avant | 0.7747 | 12.0112 | 0.31 | 0.143 | 0.0211 | 0.857 | False |
| wan_clip__apres_gfpgan | 0.7677 | 12.3284 | 0.354 | 0.1788 | 0.0156 | 0.8404 | False |
