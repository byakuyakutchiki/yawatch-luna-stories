from app.i2v_quality_gate import (
    I2V_QUALITY_THRESHOLDS,
    evaluate_i2v_metrics,
)


def test_framepack_reference_metrics_pass_i2v_gate():
    result = evaluate_i2v_metrics(
        "framepack.mp4",
        {
            "face_identity_ssim_min": 0.925,
            "face_lighting_peak_to_peak_pct": 10.69,
            "face_flicker_mean_abs_delta": 0.162,
        },
    )

    assert result.passed is True
    assert result.status == "PASS"
    assert result.failures == []
    assert result.thresholds == I2V_QUALITY_THRESHOLDS


def test_wan_reference_metrics_fail_i2v_gate():
    result = evaluate_i2v_metrics(
        "wan.mp4",
        {
            "face_identity_ssim_min": 0.522,
            "face_lighting_peak_to_peak_pct": 27.42,
            "face_flicker_mean_abs_delta": 1.307,
        },
    )

    assert result.passed is False
    assert result.status == "FAIL"
    assert {failure.metric for failure in result.failures} == {
        "face_identity_ssim_min",
        "face_lighting_peak_to_peak_pct",
        "face_flicker_mean_abs_delta",
    }


def test_threshold_boundaries_are_inclusive():
    result = evaluate_i2v_metrics(
        "boundary.mp4",
        {
            "face_identity_ssim_min": 0.85,
            "face_lighting_peak_to_peak_pct": 15.0,
            "face_flicker_mean_abs_delta": 0.5,
        },
    )

    assert result.passed is True


def test_missing_metric_fails_gate():
    result = evaluate_i2v_metrics(
        "missing.mp4",
        {
            "face_identity_ssim_min": 0.90,
            "face_lighting_peak_to_peak_pct": 10.0,
        },
    )

    assert result.passed is False
    assert [failure.metric for failure in result.failures] == [
        "face_flicker_mean_abs_delta"
    ]
