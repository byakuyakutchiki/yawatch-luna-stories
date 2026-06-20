"""Automated I2V Quality Gate for raw generated clips.

This gate runs before the full narrative QualityGate. It rejects raw image-to-video
outputs that fail the objective thresholds validated during the Wan vs FramePack
experiments.

It never grants final approval. Ludovic's human validation remains mandatory.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


I2V_QUALITY_THRESHOLDS = {
    "face_identity_ssim_min": 0.85,
    "face_lighting_peak_to_peak_pct": 15.0,
    "face_flicker_mean_abs_delta": 0.5,
}


@dataclass(frozen=True)
class I2VQualityGateFailure:
    metric: str
    value: float
    threshold: float
    operator: str
    reason: str


@dataclass(frozen=True)
class I2VQualityGateResult:
    video_path: str
    run_date: str
    passed: bool
    thresholds: dict[str, float]
    metrics: dict[str, float]
    failures: list[I2VQualityGateFailure] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        return "PASS" if self.passed else "FAIL"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def __str__(self) -> str:
        lines = [
            "=" * 72,
            f"I2V QUALITY GATE — {Path(self.video_path).name}",
            f"Date : {self.run_date}",
            f"Status : {self.status}",
            "=" * 72,
            "Metrics:",
        ]
        for metric, value in self.metrics.items():
            threshold = self.thresholds.get(metric)
            if threshold is None:
                lines.append(f"  INFO {metric}: {value:.4f}")
                continue
            failed = any(f.metric == metric for f in self.failures)
            marker = "FAIL" if failed else "PASS"
            operator = ">=" if "ssim" in metric else "<="
            lines.append(f"  {marker} {metric}: {value:.4f} ({operator} {threshold})")

        if self.failures:
            lines.append("")
            lines.append("Blocking failures:")
            for failure in self.failures:
                lines.append(f"  - {failure.reason}")

        if self.warnings:
            lines.append("")
            lines.append("Warnings:")
            for warning in self.warnings:
                lines.append(f"  - {warning}")

        lines.append("=" * 72)
        return "\n".join(lines)


def _region_by_name(report: Any, name: str) -> Any:
    for region in report.regions:
        if region.name == name:
            return region
    raise ValueError(f"Missing metric region: {name}")


def metrics_from_video_metric_report(report: Any) -> dict[str, float]:
    """Extract the blocking I2V gate metrics from VideoMetricReport."""
    face = _region_by_name(report, "face")
    return {
        "face_identity_ssim_min": float(report.identity_ssim_face_min),
        "face_lighting_peak_to_peak_pct": float(face.luminance_peak_to_peak_pct),
        "face_flicker_mean_abs_delta": float(face.flicker_mean_abs_delta),
        "duration_sec": float(report.duration_sec),
        "fps": float(report.fps),
        "frame_count": float(report.frame_count),
    }


def evaluate_i2v_metrics(
    video_path: str | Path,
    metrics: dict[str, float],
    thresholds: dict[str, float] | None = None,
) -> I2VQualityGateResult:
    """Apply validated I2V thresholds to already-computed metrics."""
    thresholds = thresholds or I2V_QUALITY_THRESHOLDS
    video_path = str(video_path)
    failures: list[I2VQualityGateFailure] = []

    identity = metrics.get("face_identity_ssim_min")
    identity_threshold = thresholds["face_identity_ssim_min"]
    if identity is None or identity < identity_threshold:
        failures.append(
            I2VQualityGateFailure(
                metric="face_identity_ssim_min",
                value=float(identity if identity is not None else -1.0),
                threshold=identity_threshold,
                operator=">=",
                reason=(
                    f"Face identity proxy {identity} below required "
                    f"{identity_threshold}."
                ),
            )
        )

    lighting = metrics.get("face_lighting_peak_to_peak_pct")
    lighting_threshold = thresholds["face_lighting_peak_to_peak_pct"]
    if lighting is None or lighting > lighting_threshold:
        failures.append(
            I2VQualityGateFailure(
                metric="face_lighting_peak_to_peak_pct",
                value=float(lighting if lighting is not None else 999.0),
                threshold=lighting_threshold,
                operator="<=",
                reason=(
                    f"Face lighting variation {lighting}% above allowed "
                    f"{lighting_threshold}%."
                ),
            )
        )

    flicker = metrics.get("face_flicker_mean_abs_delta")
    flicker_threshold = thresholds["face_flicker_mean_abs_delta"]
    if flicker is None or flicker > flicker_threshold:
        failures.append(
            I2VQualityGateFailure(
                metric="face_flicker_mean_abs_delta",
                value=float(flicker if flicker is not None else 999.0),
                threshold=flicker_threshold,
                operator="<=",
                reason=(
                    f"Face flicker {flicker} above allowed "
                    f"{flicker_threshold}."
                ),
            )
        )

    warnings: list[str] = [
        "Automated I2V pass is not final approval; human review remains mandatory.",
    ]

    return I2VQualityGateResult(
        video_path=video_path,
        run_date=datetime.now().isoformat(),
        passed=not failures,
        thresholds=dict(thresholds),
        metrics=dict(metrics),
        failures=failures,
        warnings=warnings,
    )


def run_i2v_quality_gate(
    video_path: str | Path,
    output_json: str | Path | None = None,
    thresholds: dict[str, float] | None = None,
) -> I2VQualityGateResult:
    """Decode the MP4, compute metrics, apply thresholds, optionally write JSON."""
    from app.video_metrics_evaluator import evaluate_video

    video_path = Path(video_path)
    report = evaluate_video(video_path)
    metrics = metrics_from_video_metric_report(report)
    result = evaluate_i2v_metrics(video_path, metrics, thresholds=thresholds)

    if output_json is not None:
        output_path = Path(output_json)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result.to_json(), encoding="utf-8")

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="YAWatch-LUNA raw I2V Quality Gate.")
    parser.add_argument("video", type=Path, help="MP4 file to validate.")
    parser.add_argument("--output-json", type=Path, default=None)
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text report.")
    args = parser.parse_args()

    result = run_i2v_quality_gate(args.video, output_json=args.output_json)
    if args.json:
        print(result.to_json())
    else:
        print(result)
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
