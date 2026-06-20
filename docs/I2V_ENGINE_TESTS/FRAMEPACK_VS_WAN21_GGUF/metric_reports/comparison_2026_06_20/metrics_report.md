# YAWatch-LUNA I2V Objective Metrics

These metrics are machine signals. They guide the artistic review; they do not replace it.

## Summary

| Video | Duration | FPS | Face SSIM min | Face light peak-to-peak | Face flicker | Shoulder flow | Hair flow | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| YAWATCH_WAN21_PLAN02_LUNA_MOTION_TEST_00001.mp4 | 5.06s | 16.00 | 0.522 | 27.42% | 1.307 | 0.5636 | 0.5299 | identity_proxy:REVIEW, lighting_face:REVIEW, flicker_face:PASS, shoulder_motion:PASS, hair_motion:PASS |
| YAWATCH_WAN21_PLAN02_LUNA_LIGHTING_STABLE_TEST_00001.mp4 | 5.06s | 16.00 | 0.500 | 28.37% | 1.297 | 0.5517 | 0.5280 | identity_proxy:REVIEW, lighting_face:REVIEW, flicker_face:PASS, shoulder_motion:PASS, hair_motion:PASS |
| YAWATCH_FRAMEPACK_PLAN02_LUNA_TEST_00001.mp4 | 9.06s | 16.00 | 0.925 | 10.69% | 0.162 | 0.0720 | 0.0724 | identity_proxy:PASS, lighting_face:REVIEW, flicker_face:PASS, shoulder_motion:LOW_MOTION, hair_motion:LOW_MOTION |

## Region Details

### YAWATCH_WAN21_PLAN02_LUNA_MOTION_TEST_00001.mp4

| Region | Luma mean | Luma std | Luma CV | Luma peak-to-peak | Flicker | Flow mean | Flow p95 |
|---|---:|---:|---:|---:|---:|---:|---:|
| face | 67.90 | 4.41 | 6.49% | 27.42% | 1.307 | 0.6408 | 1.5908 |
| hair | 80.88 | 4.38 | 5.41% | 17.43% | 0.728 | 0.5299 | 1.2475 |
| shoulders | 26.29 | 4.57 | 17.37% | 77.39% | 1.923 | 0.5636 | 1.1532 |
| background | 104.70 | 7.43 | 7.09% | 26.16% | 0.913 | 0.4046 | 1.2297 |
| full_frame | 55.76 | 3.45 | 6.19% | 23.42% | 0.673 | 0.3746 | 0.8422 |

### YAWATCH_WAN21_PLAN02_LUNA_LIGHTING_STABLE_TEST_00001.mp4

| Region | Luma mean | Luma std | Luma CV | Luma peak-to-peak | Flicker | Flow mean | Flow p95 |
|---|---:|---:|---:|---:|---:|---:|---:|
| face | 68.35 | 4.69 | 6.87% | 28.37% | 1.297 | 0.6288 | 1.3638 |
| hair | 81.22 | 4.60 | 5.66% | 17.89% | 0.732 | 0.5280 | 1.2360 |
| shoulders | 26.50 | 4.66 | 17.57% | 78.29% | 1.927 | 0.5517 | 1.2042 |
| background | 104.04 | 7.61 | 7.32% | 26.46% | 0.902 | 0.3952 | 1.1494 |
| full_frame | 55.84 | 3.59 | 6.42% | 23.71% | 0.677 | 0.3681 | 0.8627 |

### YAWATCH_FRAMEPACK_PLAN02_LUNA_TEST_00001.mp4

| Region | Luma mean | Luma std | Luma CV | Luma peak-to-peak | Flicker | Flow mean | Flow p95 |
|---|---:|---:|---:|---:|---:|---:|---:|
| face | 65.29 | 1.66 | 2.55% | 10.69% | 0.162 | 0.0783 | 0.1311 |
| hair | 75.97 | 1.29 | 1.70% | 8.94% | 0.142 | 0.0724 | 0.1168 |
| shoulders | 25.37 | 1.33 | 5.25% | 25.89% | 0.138 | 0.0720 | 0.1242 |
| background | 93.80 | 1.34 | 1.43% | 7.87% | 0.130 | 0.0618 | 0.1113 |
| full_frame | 52.09 | 1.08 | 2.08% | 11.65% | 0.114 | 0.0549 | 0.0961 |
