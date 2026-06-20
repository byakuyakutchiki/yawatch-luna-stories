from pathlib import Path

import pytest

from app.i2v_engine import comfyui_backend


class FakeGateResult:
    def __init__(self, passed):
        self.passed = passed

    def __str__(self):
        return f"FakeGateResult(passed={self.passed})"


def test_enforce_i2v_quality_gate_passes(monkeypatch, tmp_path):
    video = tmp_path / "clip.mp4"
    video.write_bytes(b"fake mp4")
    expected_report = video.with_suffix(".i2v_quality_gate.json")

    calls = {}

    def fake_run_i2v_quality_gate(path, output_json=None):
        calls["path"] = Path(path)
        calls["output_json"] = Path(output_json)
        Path(output_json).write_text('{"passed": true}', encoding="utf-8")
        return FakeGateResult(passed=True)

    monkeypatch.setattr(
        "app.i2v_quality_gate.run_i2v_quality_gate",
        fake_run_i2v_quality_gate,
    )

    report = comfyui_backend.enforce_i2v_quality_gate(video)

    assert report == expected_report
    assert calls == {"path": video, "output_json": expected_report}
    assert expected_report.exists()


def test_enforce_i2v_quality_gate_blocks_fail(monkeypatch, tmp_path):
    video = tmp_path / "clip.mp4"
    video.write_bytes(b"fake mp4")
    expected_report = video.with_suffix(".i2v_quality_gate.json")

    def fake_run_i2v_quality_gate(path, output_json=None):
        Path(output_json).write_text('{"passed": false}', encoding="utf-8")
        return FakeGateResult(passed=False)

    monkeypatch.setattr(
        "app.i2v_quality_gate.run_i2v_quality_gate",
        fake_run_i2v_quality_gate,
    )

    with pytest.raises(RuntimeError, match="Quality Gate I2V échoué"):
        comfyui_backend.enforce_i2v_quality_gate(video)

    assert expected_report.exists()


def test_video_job_runs_i2v_quality_gate_by_default():
    job = comfyui_backend.VideoJob(
        output_name="clip.mp4",
        deposit_dir="out",
        image_path="image.png",
        prompt_positive="positive",
        prompt_negative="negative",
    )

    assert job.run_i2v_quality_gate is True
