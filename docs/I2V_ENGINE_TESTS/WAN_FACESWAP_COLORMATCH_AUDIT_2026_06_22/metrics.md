# Metrics - WAN -> face-swap -> colormatch audit

| Clip | face luma mean | peak-to-peak % | flicker | face/scene DeltaLAB | sharpness | border artifact | screen-face corr | detect rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| WAN original | 60.7165 | 47.2468 | 1.2409 | 13.1339 | 18.6612 | 1.0222 | 0.7042 | 1.0000 |
| WAN + GFPGAN | 58.8539 | 42.5112 | 0.7266 | 12.9556 | 23.3823 | 0.9675 | 0.7794 | 1.0000 |
| WAN + face-swap | 61.4509 | 42.9764 | 1.6195 | 15.5561 | 9.3053 | 1.1527 | 0.5227 | 1.0000 |
| WAN + face-swap + colormatch | 58.8202 | 45.3255 | 2.0574 | 14.0057 | 8.7572 | 1.1136 | 0.5864 | 1.0000 |
| Kling reference | 27.5184 | 15.1686 | 0.4229 | 16.3138 | 14.1419 | 0.7102 | -0.1280 | 1.0000 |
