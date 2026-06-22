"""Objective video metrics for YAWatch-LUNA I2V tests.

This module does not replace Ludovic's artistic validation. It turns recurring
visual problems into measurable signals: lighting drift, flicker, motion amount,
and face-region stability.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np


@dataclass(frozen=True)
class RegionMetric:
    name: str
    x: float
    y: float
    w: float
    h: float
    luminance_mean: float
    luminance_std: float
    luminance_cv_pct: float
    luminance_peak_to_peak_pct: float
    flicker_mean_abs_delta: float
    optical_flow_mean: float
    optical_flow_p95: float


@dataclass(frozen=True)
class VideoMetricReport:
    video_path: str
    file_size_bytes: int
    width: int
    height: int
    fps: float
    frame_count: int
    duration_sec: float
    sampled_frames: int
    identity_ssim_face_mean: float
    identity_ssim_face_min: float
    regions: list[RegionMetric]
    verdict: dict[str, str]


REGIONS = {
    # Ratios are tuned for the current vertical portrait test framing.
    # They are intentionally transparent and can be adjusted per shot family.
    "face": (0.30, 0.09, 0.40, 0.27),
    "hair": (0.18, 0.05, 0.64, 0.42),
    "shoulders": (0.14, 0.43, 0.72, 0.34),
    "background": (0.08, 0.02, 0.84, 0.20),
    "full_frame": (0.00, 0.00, 1.00, 1.00),
}


def _crop(frame: np.ndarray, region: tuple[float, float, float, float]) -> np.ndarray:
    h, w = frame.shape[:2]
    x, y, rw, rh = region
    x0 = max(0, min(w - 1, int(round(x * w))))
    y0 = max(0, min(h - 1, int(round(y * h))))
    x1 = max(x0 + 1, min(w, int(round((x + rw) * w))))
    y1 = max(y0 + 1, min(h, int(round((y + rh) * h))))
    return frame[y0:y1, x0:x1]


def _luma(frame_bgr: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2LAB)
    return lab[:, :, 0].astype(np.float32)


def _ssim_gray(a: np.ndarray, b: np.ndarray) -> float:
    a = a.astype(np.float64)
    b = b.astype(np.float64)
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2
    mu_a = a.mean()
    mu_b = b.mean()
    var_a = a.var()
    var_b = b.var()
    cov = ((a - mu_a) * (b - mu_b)).mean()
    denom = (mu_a**2 + mu_b**2 + c1) * (var_a + var_b + c2)
    if denom == 0:
        return 1.0
    return float(((2 * mu_a * mu_b + c1) * (2 * cov + c2)) / denom)


def _read_video(video_path: Path, max_frames: int | None = None) -> tuple[list[np.ndarray], float, int, int, int]:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)

    frames: list[np.ndarray] = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frames.append(frame)
        if max_frames and len(frames) >= max_frames:
            break
    cap.release()
    return frames, fps, width, height, frame_count


def _flow_metrics(gray_frames: list[np.ndarray], region: tuple[float, float, float, float]) -> tuple[float, float]:
    magnitudes: list[float] = []
    for prev, curr in zip(gray_frames, gray_frames[1:]):
        prev_roi = _crop(prev, region)
        curr_roi = _crop(curr, region)
        flow = cv2.calcOpticalFlowFarneback(
            prev_roi,
            curr_roi,
            None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0,
        )
        mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        magnitudes.append(float(np.mean(mag)))
    if not magnitudes:
        return 0.0, 0.0
    values = np.asarray(magnitudes, dtype=np.float32)
    return float(values.mean()), float(np.percentile(values, 95))


def _region_metrics(frames: list[np.ndarray], gray_frames: list[np.ndarray], name: str, region: tuple[float, float, float, float]) -> RegionMetric:
    luminance_values = []
    for frame in frames:
        luminance_values.append(float(_luma(_crop(frame, region)).mean()))
    luminance = np.asarray(luminance_values, dtype=np.float32)
    mean = float(luminance.mean())
    std = float(luminance.std())
    cv_pct = float((std / mean) * 100) if mean else 0.0
    ptp_pct = float(((luminance.max() - luminance.min()) / mean) * 100) if mean else 0.0
    flicker = float(np.mean(np.abs(np.diff(luminance)))) if len(luminance) > 1 else 0.0
    flow_mean, flow_p95 = _flow_metrics(gray_frames, region)
    x, y, w, h = region
    return RegionMetric(
        name=name,
        x=x,
        y=y,
        w=w,
        h=h,
        luminance_mean=round(mean, 4),
        luminance_std=round(std, 4),
        luminance_cv_pct=round(cv_pct, 4),
        luminance_peak_to_peak_pct=round(ptp_pct, 4),
        flicker_mean_abs_delta=round(flicker, 4),
        optical_flow_mean=round(flow_mean, 4),
        optical_flow_p95=round(flow_p95, 4),
    )


def _identity_metrics(gray_frames: list[np.ndarray]) -> tuple[float, float]:
    face_region = REGIONS["face"]
    first = _crop(gray_frames[0], face_region)
    scores = []
    for frame in gray_frames[1:]:
        roi = _crop(frame, face_region)
        if roi.shape != first.shape:
            roi = cv2.resize(roi, (first.shape[1], first.shape[0]), interpolation=cv2.INTER_AREA)
        scores.append(_ssim_gray(first, roi))
    if not scores:
        return 1.0, 1.0
    values = np.asarray(scores, dtype=np.float32)
    return float(values.mean()), float(values.min())


def tracked_face_identity_ssim(video_path: Path, max_frames: int | None = None) -> dict:
    """SSIM d'identité sur le visage DÉTECTÉ (boîte qui suit la tête), pas un
    rectangle fixe — mesure juste pour un sujet qui bouge.

    Détection : Haar cascade (livrée avec OpenCV, CPU, zéro modèle à télécharger).
    Si aucun visage détecté (profil, tête tournée) → on réutilise la dernière
    boîte connue. `face_detect_rate` indique la fiabilité de la détection.
    """
    cap = cv2.VideoCapture(str(video_path))
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    frames: list[np.ndarray] = []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        frames.append(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY))
        if max_frames and len(frames) >= max_frames:
            break
    cap.release()
    if len(frames) < 2:
        return {"face_tracked_ssim_min": 1.0, "face_tracked_ssim_mean": 1.0,
                "face_detect_rate": 0.0}

    ref = None
    last_box = None
    detected = 0
    scores: list[float] = []
    for g in frames:
        dets = cascade.detectMultiScale(g, scaleFactor=1.1, minNeighbors=5,
                                        minSize=(60, 60))
        if len(dets) > 0:
            last_box = max(dets, key=lambda b: b[2] * b[3])
            detected += 1
        if last_box is None:
            continue
        x, y, w, h = last_box
        crop = g[y:y + h, x:x + w]
        if crop.size == 0:
            continue
        crop = cv2.resize(crop, (256, 256), interpolation=cv2.INTER_AREA)
        if ref is None:
            ref = crop
            continue
        scores.append(_ssim_gray(ref, crop))
    rate = round(detected / max(1, len(frames)), 3)
    if not scores:
        return {"face_tracked_ssim_min": 0.0, "face_tracked_ssim_mean": 0.0,
                "face_detect_rate": rate}
    arr = np.asarray(scores, dtype=np.float32)
    return {"face_tracked_ssim_min": round(float(arr.min()), 4),
            "face_tracked_ssim_mean": round(float(arr.mean()), 4),
            "face_detect_rate": rate}


def _verdict(report: VideoMetricReport) -> dict[str, str]:
    face = next(region for region in report.regions if region.name == "face")
    shoulders = next(region for region in report.regions if region.name == "shoulders")
    hair = next(region for region in report.regions if region.name == "hair")

    verdict = {}
    verdict["identity_proxy"] = "PASS" if report.identity_ssim_face_min >= 0.72 else "REVIEW"
    verdict["lighting_face"] = "PASS" if face.luminance_peak_to_peak_pct <= 10.0 else "REVIEW"
    verdict["flicker_face"] = "PASS" if face.flicker_mean_abs_delta <= 2.0 else "REVIEW"
    verdict["shoulder_motion"] = "PASS" if shoulders.optical_flow_mean >= 0.08 else "LOW_MOTION"
    verdict["hair_motion"] = "PASS" if hair.optical_flow_mean >= 0.08 else "LOW_MOTION"
    return verdict


def evaluate_video(video_path: Path, max_frames: int | None = None) -> VideoMetricReport:
    frames, fps, width, height, frame_count = _read_video(video_path, max_frames=max_frames)
    if not frames:
        raise RuntimeError(f"No frames decoded: {video_path}")
    gray_frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) for frame in frames]
    ssim_mean, ssim_min = _identity_metrics(gray_frames)
    duration = (frame_count / fps) if fps else 0.0
    regions = [_region_metrics(frames, gray_frames, name, region) for name, region in REGIONS.items()]
    report_without_verdict = VideoMetricReport(
        video_path=str(video_path),
        file_size_bytes=video_path.stat().st_size,
        width=width,
        height=height,
        fps=round(fps, 4),
        frame_count=frame_count,
        duration_sec=round(duration, 4),
        sampled_frames=len(frames),
        identity_ssim_face_mean=round(ssim_mean, 4),
        identity_ssim_face_min=round(ssim_min, 4),
        regions=regions,
        verdict={},
    )
    return VideoMetricReport(
        video_path=report_without_verdict.video_path,
        file_size_bytes=report_without_verdict.file_size_bytes,
        width=report_without_verdict.width,
        height=report_without_verdict.height,
        fps=report_without_verdict.fps,
        frame_count=report_without_verdict.frame_count,
        duration_sec=report_without_verdict.duration_sec,
        sampled_frames=report_without_verdict.sampled_frames,
        identity_ssim_face_mean=report_without_verdict.identity_ssim_face_mean,
        identity_ssim_face_min=report_without_verdict.identity_ssim_face_min,
        regions=report_without_verdict.regions,
        verdict=_verdict(report_without_verdict),
    )


def _write_markdown(reports: Iterable[VideoMetricReport], output_path: Path) -> None:
    reports = list(reports)
    lines = [
        "# YAWatch-LUNA I2V Objective Metrics",
        "",
        "These metrics are machine signals. They guide the artistic review; they do not replace it.",
        "",
        "## Summary",
        "",
        "| Video | Duration | FPS | Face SSIM min | Face light peak-to-peak | Face flicker | Shoulder flow | Hair flow | Verdict |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for report in reports:
        face = next(region for region in report.regions if region.name == "face")
        shoulders = next(region for region in report.regions if region.name == "shoulders")
        hair = next(region for region in report.regions if region.name == "hair")
        verdict = ", ".join(f"{k}:{v}" for k, v in report.verdict.items())
        lines.append(
            "| "
            + " | ".join(
                [
                    Path(report.video_path).name,
                    f"{report.duration_sec:.2f}s",
                    f"{report.fps:.2f}",
                    f"{report.identity_ssim_face_min:.3f}",
                    f"{face.luminance_peak_to_peak_pct:.2f}%",
                    f"{face.flicker_mean_abs_delta:.3f}",
                    f"{shoulders.optical_flow_mean:.4f}",
                    f"{hair.optical_flow_mean:.4f}",
                    verdict,
                ]
            )
            + " |"
        )
    lines.extend(["", "## Region Details", ""])
    for report in reports:
        lines.extend(
            [
                f"### {Path(report.video_path).name}",
                "",
                "| Region | Luma mean | Luma std | Luma CV | Luma peak-to-peak | Flicker | Flow mean | Flow p95 |",
                "|---|---:|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for region in report.regions:
            lines.append(
                "| "
                + " | ".join(
                    [
                        region.name,
                        f"{region.luminance_mean:.2f}",
                        f"{region.luminance_std:.2f}",
                        f"{region.luminance_cv_pct:.2f}%",
                        f"{region.luminance_peak_to_peak_pct:.2f}%",
                        f"{region.flicker_mean_abs_delta:.3f}",
                        f"{region.optical_flow_mean:.4f}",
                        f"{region.optical_flow_p95:.4f}",
                    ]
                )
                + " |"
            )
        lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate YAWatch-LUNA I2V video metrics.")
    parser.add_argument("videos", nargs="+", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-frames", type=int, default=None)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    reports = [evaluate_video(video, max_frames=args.max_frames) for video in args.videos]
    payload = [asdict(report) for report in reports]
    (args.output_dir / "metrics.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    _write_markdown(reports, args.output_dir / "metrics_report.md")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
