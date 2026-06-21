# YAWatch-LUNA I2V Objective Metrics

These metrics are machine signals. They guide the artistic review; they do not replace it.

## Summary

| Video | Duration | FPS | Face SSIM min | Face light peak-to-peak | Face flicker | Shoulder flow | Hair flow | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| plan02_luna_FRAMEPACK.mp4 | 9.08s | 25.00 | 0.942 | 10.40% | 0.190 | 0.0961 | 0.0857 | identity_proxy:PASS, lighting_face:REVIEW, flicker_face:PASS, shoulder_motion:PASS, hair_motion:PASS |
| plan02_luna_WAN.mp4 | 5.12s | 25.00 | 0.829 | 8.56% | 0.250 | 0.2704 | 0.1853 | identity_proxy:PASS, lighting_face:PASS, flicker_face:PASS, shoulder_motion:PASS, hair_motion:PASS |

## Region Details

### plan02_luna_FRAMEPACK.mp4

| Region | Luma mean | Luma std | Luma CV | Luma peak-to-peak | Flicker | Flow mean | Flow p95 |
|---|---:|---:|---:|---:|---:|---:|---:|
| face | 67.93 | 1.28 | 1.88% | 10.40% | 0.190 | 0.1107 | 0.2298 |
| hair | 77.64 | 1.24 | 1.60% | 9.08% | 0.186 | 0.0857 | 0.1876 |
| shoulders | 27.59 | 1.17 | 4.25% | 25.22% | 0.187 | 0.0961 | 0.2665 |
| background | 91.79 | 1.35 | 1.47% | 8.69% | 0.206 | 0.0371 | 0.0959 |
| full_frame | 52.47 | 1.04 | 1.98% | 11.93% | 0.164 | 0.0578 | 0.1444 |

### plan02_luna_WAN.mp4

| Region | Luma mean | Luma std | Luma CV | Luma peak-to-peak | Flicker | Flow mean | Flow p95 |
|---|---:|---:|---:|---:|---:|---:|---:|
| face | 66.67 | 1.73 | 2.60% | 8.56% | 0.250 | 0.2305 | 1.0060 |
| hair | 76.67 | 0.75 | 0.97% | 2.90% | 0.130 | 0.1853 | 0.7843 |
| shoulders | 26.39 | 3.13 | 11.87% | 41.49% | 0.441 | 0.2704 | 1.2427 |
| background | 90.71 | 1.33 | 1.47% | 5.52% | 0.184 | 0.0665 | 0.3006 |
| full_frame | 51.14 | 1.07 | 2.10% | 6.12% | 0.149 | 0.1415 | 0.6055 |
