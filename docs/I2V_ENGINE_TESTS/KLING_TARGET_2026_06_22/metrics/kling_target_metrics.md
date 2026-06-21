# Kling Target Metrics — Custom Landscape Regions

Ces métriques utilisent des régions adaptées au cadrage paysage Kling. Elles servent de cible, pas de Quality Gate direct pour les clips portrait.

| Video | Duration | FPS | Face SSIM min | Face light peak-to-peak | Face flicker | Shoulder flow | Hair flow | Hands/frame flow |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| kling_20260619_VIDEO_Cinematic__4730_0.mp4 | 5.04s | 24.00 | 0.729 | 28.68% | 0.085 | 0.1590 | 0.1602 | 0.1635 |

## Region Details

| Region | Luma mean | Luma std | Luma CV | Luma peak-to-peak | Flicker | Flow mean | Flow p95 |
|---|---:|---:|---:|---:|---:|---:|---:|
| face | 8.73 | 0.68 | 7.73% | 28.68% | 0.085 | 0.1072 | 0.2041 |
| hair | 11.81 | 0.47 | 3.96% | 14.33% | 0.067 | 0.1602 | 0.3207 |
| shoulders | 11.92 | 1.77 | 14.84% | 47.82% | 0.066 | 0.1590 | 0.3432 |
| hands_frame | 6.25 | 0.86 | 13.75% | 42.35% | 0.043 | 0.1635 | 0.3337 |
| background_city | 13.52 | 0.17 | 1.24% | 6.74% | 0.065 | 0.1810 | 0.4157 |
| full_frame | 12.72 | 0.32 | 2.52% | 11.25% | 0.046 | 0.2346 | 0.4668 |