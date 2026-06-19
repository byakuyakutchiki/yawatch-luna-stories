"""Tests du Quality Gate — 6 verdicts + validation humaine."""

import pytest
from app.production_gatekeeper import ProductionGatekeeper
from app.production_statuses import ProductionStatus
from app.quality_gate import QualityGate, GateReport
from app.roles.base_role import VerdictResult


@pytest.fixture
def gatekeeper():
    return ProductionGatekeeper.load(strict=False)


@pytest.fixture
def gate(gatekeeper):
    return QualityGate(gatekeeper)


# ── VerdictResult ──────────────────────────────────────────────────────────────

def test_verdict_pass_is_not_blocking():
    v = VerdictResult("test", "PASS")
    assert v.passed is True
    assert v.blocks is False


def test_verdict_fail_is_blocking():
    v = VerdictResult("test", "FAIL", ["erreur"])
    assert v.passed is False
    assert v.blocks is True


def test_verdict_needs_human_blocks():
    v = VerdictResult("test", "NEEDS_HUMAN")
    assert v.passed is False
    assert v.blocks is True


def test_verdict_str_contains_name():
    v = VerdictResult("verdict_technique", "PASS")
    assert "verdict_technique" in str(v)
    assert "PASS" in str(v)


# ── GateReport ─────────────────────────────────────────────────────────────────

def test_gate_report_initial_status_is_prototype():
    report = GateReport(video_path="/tmp/test.mp4")
    # Tous les verdicts sont FAIL par défaut → prototype
    assert report.current_status == ProductionStatus.PROTOTYPE_TECHNIQUE


def test_gate_report_can_advance_to_valide_requires_human():
    report = GateReport(video_path="/tmp/test.mp4")
    report.verdict_technique = VerdictResult("verdict_technique", "PASS")
    report.verdict_mouvement = VerdictResult("verdict_mouvement", "PASS")
    report.verdict_montage = VerdictResult("verdict_montage", "PASS")
    report.verdict_son = VerdictResult("verdict_son", "PASS")
    report.verdict_coherence_personnage = VerdictResult("verdict_coherence_personnage", "PASS")
    # storytelling = NEEDS_HUMAN par défaut
    assert report.can_advance_to_candidat is True
    assert report.can_advance_to_valide is False
    assert report.current_status == ProductionStatus.TEASER_CANDIDAT


def test_gate_report_valide_requires_all_pass_and_human():
    report = GateReport(video_path="/tmp/test.mp4")
    for attr in [
        "verdict_technique", "verdict_mouvement", "verdict_montage",
        "verdict_son", "verdict_coherence_personnage", "verdict_storytelling"
    ]:
        setattr(report, attr, VerdictResult(attr, "PASS"))
    report.human_approved = True
    assert report.can_advance_to_valide is True
    assert report.current_status == ProductionStatus.TEASER_VALIDE


def test_gate_report_to_dict_contains_all_verdicts():
    report = GateReport(video_path="/tmp/test.mp4")
    d = report.to_dict()
    assert "verdicts" in d
    assert len(d["verdicts"]) == 6
    assert "final_status" in d


# ── QualityGate.run() ──────────────────────────────────────────────────────────

def test_gate_run_empty_context_fails_technique(gate):
    report = gate.run({"video_path": "/nonexistent/file.mp4"})
    assert report.verdict_technique.status == "FAIL"
    assert "introuvable" in report.verdict_technique.errors[0].lower() or \
           "manquant" in report.verdict_technique.errors[0].lower() or \
           "introuvable" in str(report.verdict_technique.errors).lower()


def test_gate_run_storytelling_needs_human_without_context(gate):
    report = gate.run({"video_path": "/tmp/test.mp4"})
    assert report.verdict_storytelling.status == "NEEDS_HUMAN"


def test_gate_run_storytelling_needs_human_explicit(gate):
    report = gate.run(
        {"video_path": "/tmp/test.mp4"},
        storytelling_context={"human_watched": False}
    )
    assert report.verdict_storytelling.status == "NEEDS_HUMAN"


def test_gate_run_report_str_contains_statuts(gate):
    report = gate.run({"video_path": "/tmp/test.mp4"})
    output = str(report)
    assert "QUALITY GATE" in output
    assert "verdict_technique" in output


# ── QualityGate.record_human_verdict() ────────────────────────────────────────

def test_human_verdict_approved(gate):
    report = GateReport(video_path="/tmp/test.mp4")
    gate.record_human_verdict(report, approved=True, approved_by="Ludovic", notes="RAS")
    assert report.human_approved is True
    assert report.human_approved_by == "Ludovic"
    assert report.verdict_storytelling.status == "PASS"


def test_human_verdict_rejected(gate):
    report = GateReport(video_path="/tmp/test.mp4")
    gate.record_human_verdict(report, approved=False, approved_by="Ludovic", notes="Dérive chromatique plan 3")
    assert report.human_approved is False
    assert report.verdict_storytelling.status == "FAIL"
    assert "Ludovic" in report.verdict_storytelling.errors[0]


def test_human_verdict_rejects_ai_approver(gate):
    report = GateReport(video_path="/tmp/test.mp4")
    for bad_approver in ("claude", "codex", "agent", "ai", "bot", ""):
        with pytest.raises(ValueError, match="humain valide"):
            gate.record_human_verdict(report, approved=True, approved_by=bad_approver)


# ── Rôles individuels — tests unitaires ────────────────────────────────────────

def test_video_qa_engineer_fails_nonexistent_file(gatekeeper):
    result = gatekeeper.video_qa_engineer.validate({"video_path": "/nonexistent.mp4"})
    assert result.status == "FAIL"
    assert any("introuvable" in e.lower() for e in result.errors)


def test_motion_engineer_fails_too_many_ken_burns(gatekeeper):
    result = gatekeeper.motion_engineer.validate({
        "i2v_tool": "ffmpeg",
        "ken_burns_count": 9,
        "total_plans": 9,
        "clips": [],
    })
    assert result.status == "FAIL"
    assert any("Ken Burns" in e or "diaporama" in e for e in result.errors)


def test_motion_engineer_fails_zoompan_without_fps(gatekeeper):
    result = gatekeeper.motion_engineer.validate({
        "i2v_tool": "ffmpeg_zoompan",
        "ken_burns_count": 1,
        "total_plans": 1,
        "clips": [],
        "zoompan_params": {
            "fps_specified": False,
            "zoom_increment": 0.002,
            "max_zoom": 1.5,
            "xy_anchored": True,
        }
    })
    assert result.status == "FAIL"
    assert any("fps=25" in e for e in result.errors)


def test_monteur_cinema_fails_negative_xfade_offset(gatekeeper):
    result = gatekeeper.monteur_cinema.validate({
        "plan_durations": [0.3, 5.0, 5.0],  # 0.3s < fade_duration → offset négatif
        "xfade_offsets": [-0.2, 4.8],
        "episode_id": "test",
    })
    assert result.status == "FAIL"
    assert any("négatif" in e for e in result.errors)


def test_sound_designer_fails_no_audio(gatekeeper):
    result = gatekeeper.sound_designer.validate({})
    assert result.status == "FAIL"
    assert any("audio" in e.lower() for e in result.errors)


def test_video_generation_engineer_fails_placeholder(gatekeeper):
    result = gatekeeper.video_generation_engineer.validate({
        "clips": [],
        "source_images": ["content/images/episode_test/scene_hook.jpg"],
        "i2v_tool": "kling",
    })
    assert result.status == "FAIL"
    assert any("placeholder" in e.lower() for e in result.errors)


def test_trailer_designer_needs_human_without_watch(gatekeeper):
    result = gatekeeper.trailer_designer.validate({
        "has_hook": True,
        "title_card_text": "LUNA / Tout a commencé par un secret.",
        "title_card_duration": 3.0,
        "total_duration": 28.0,
        "human_watched": False,
    })
    assert result.status == "NEEDS_HUMAN"


def test_trailer_designer_fails_missing_hook(gatekeeper):
    result = gatekeeper.trailer_designer.validate({
        "has_hook": False,
        "title_card_text": "LUNA",
        "human_watched": True,
        "human_verdict": "approved",
    })
    assert result.status == "FAIL"
    assert any("hook" in e.lower() for e in result.errors)


def test_trailer_designer_fails_wrong_title_card(gatekeeper):
    result = gatekeeper.trailer_designer.validate({
        "has_hook": True,
        "title_card_text": "YAWatch Industries présente",  # pas de "LUNA"
        "human_watched": True,
        "human_verdict": "approved",
    })
    assert result.status == "FAIL"
    assert any("LUNA" in e for e in result.errors)
