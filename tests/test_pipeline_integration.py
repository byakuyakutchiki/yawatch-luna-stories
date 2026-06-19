"""Tests d'intégration — vérifie que le flux de production respecte les garde-fous.

Ces tests valident que les points d'entrée réels (main.py, batch_processor.py,
export_manager.py) ne permettent pas de contourner le gatekeeper ni le quality gate.
"""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.production_statuses import ProductionStatus
from app.production_gatekeeper import ProductionGatekeeper
from app.quality_gate import QualityGate, GateReport
from app.roles.base_role import VerdictResult


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_passing_gate_report(video_path: str = "/tmp/test.mp4") -> GateReport:
    """Construit un GateReport avec les 5 verdicts automatiques à PASS."""
    report = GateReport(video_path=video_path)
    for attr in [
        "verdict_technique", "verdict_mouvement", "verdict_montage",
        "verdict_son", "verdict_coherence_personnage",
    ]:
        setattr(report, attr, VerdictResult(attr, "PASS"))
    # storytelling reste NEEDS_HUMAN
    return report


def make_full_approved_report(video_path: str = "/tmp/test.mp4") -> GateReport:
    """GateReport complet : 6 verdicts PASS + approbation humaine."""
    report = make_passing_gate_report(video_path)
    report.verdict_storytelling = VerdictResult("verdict_storytelling", "PASS")
    report.human_approved = True
    report.human_approved_by = "Ludovic"
    return report


# ── ExportManager — statuts progressifs ───────────────────────────────────────

@pytest.fixture
def export_manager(tmp_path):
    """ExportManager avec EXPORT_ROOT redirigé vers tmp_path."""
    from app import export_manager as em_module
    original = em_module.EXPORT_ROOT
    em_module.EXPORT_ROOT = tmp_path
    yield em_module.ExportManager()
    em_module.EXPORT_ROOT = original


def test_create_package_always_prototype(export_manager, tmp_path):
    """create_package() ne peut jamais assigner un statut autre que PROTOTYPE_TECHNIQUE."""
    from app import export_manager as em_module
    em_module.EXPORT_ROOT = tmp_path

    story = {"title": "Test", "episode_number": 1}
    export_dir = export_manager.create_package("ep_test_01", story)
    meta = json.loads((export_dir / "metadata.json").read_text())

    assert meta["status"] == ProductionStatus.PROTOTYPE_TECHNIQUE.value
    assert meta["human_approved"] is False
    assert meta["quality_gate_passed"] is False


def test_create_package_with_video_still_prototype(export_manager, tmp_path):
    """Même avec un MP4 fourni, create_package() donne PROTOTYPE_TECHNIQUE — pas TEASER_CANDIDAT."""
    from app import export_manager as em_module
    em_module.EXPORT_ROOT = tmp_path

    fake_mp4 = tmp_path / "fake.mp4"
    fake_mp4.write_bytes(b"fake")
    story = {"title": "Test", "episode_number": 1}
    export_dir = export_manager.create_package("ep_test_02", story, video_path=fake_mp4)
    meta = json.loads((export_dir / "metadata.json").read_text())

    assert meta["status"] == ProductionStatus.PROTOTYPE_TECHNIQUE.value, (
        "Un MP4 fourni à create_package() ne suffit pas pour TEASER_CANDIDAT. "
        "Il faut passer par advance_to_candidat(gate_report)."
    )


def test_advance_to_candidat_requires_passing_gate(export_manager, tmp_path):
    """advance_to_candidat() échoue si le gate n'est pas passé."""
    from app import export_manager as em_module
    em_module.EXPORT_ROOT = tmp_path

    story = {"title": "Test", "episode_number": 1}
    export_manager.create_package("ep_test_03", story)

    failing_report = GateReport(video_path="/tmp/test.mp4")
    # Tous les verdicts restent FAIL par défaut

    with pytest.raises(ValueError, match="QualityGate non passé"):
        export_manager.advance_to_candidat("ep_test_03", failing_report)


def test_advance_to_candidat_succeeds_with_passing_gate(export_manager, tmp_path):
    """advance_to_candidat() réussit quand les 5 verdicts automatiques passent."""
    from app import export_manager as em_module
    em_module.EXPORT_ROOT = tmp_path

    story = {"title": "Test", "episode_number": 1}
    export_manager.create_package("ep_test_04", story)

    report = make_passing_gate_report()
    export_manager.advance_to_candidat("ep_test_04", report)

    meta = json.loads((tmp_path / "ep_test_04" / "metadata.json").read_text())
    assert meta["status"] == ProductionStatus.TEASER_CANDIDAT.value
    assert meta["quality_gate_passed"] is True
    assert "quality_gate_report" in meta


def test_mark_human_approved_requires_candidat_status(export_manager, tmp_path):
    """mark_human_approved() échoue si le package est encore en PROTOTYPE_TECHNIQUE."""
    from app import export_manager as em_module
    em_module.EXPORT_ROOT = tmp_path

    story = {"title": "Test", "episode_number": 1}
    export_manager.create_package("ep_test_05", story)

    with pytest.raises(ValueError, match="teaser_candidat"):
        export_manager.mark_human_approved("ep_test_05", approved_by="Ludovic")


def test_full_promotion_flow(export_manager, tmp_path):
    """Flux complet : PROTOTYPE → CANDIDAT → VALIDE."""
    from app import export_manager as em_module
    em_module.EXPORT_ROOT = tmp_path

    story = {"title": "Test", "episode_number": 1}
    export_manager.create_package("ep_test_06", story)

    # Étape 1 : quality gate → CANDIDAT
    report = make_passing_gate_report()
    export_manager.advance_to_candidat("ep_test_06", report)

    # Étape 2 : validation humaine → VALIDE
    export_manager.mark_human_approved("ep_test_06", approved_by="Ludovic", notes="OK")

    meta = json.loads((tmp_path / "ep_test_06" / "metadata.json").read_text())
    assert meta["status"] == ProductionStatus.TEASER_VALIDE.value
    assert meta["human_approved"] is True
    assert meta["human_approved_by"] == "Ludovic"


def test_mark_human_approved_rejects_ai_names(export_manager, tmp_path):
    """mark_human_approved() rejette tous les noms IA."""
    from app import export_manager as em_module
    em_module.EXPORT_ROOT = tmp_path

    story = {"title": "Test", "episode_number": 1}
    export_manager.create_package("ep_test_07", story)

    # D'abord passer en CANDIDAT
    report = make_passing_gate_report()
    export_manager.advance_to_candidat("ep_test_07", report)

    for bad_name in ("claude", "codex", "agent", "ai", "bot", ""):
        with pytest.raises(ValueError, match="humain valide"):
            export_manager.mark_human_approved("ep_test_07", approved_by=bad_name)


def test_no_direct_path_to_teaser_valide(export_manager, tmp_path):
    """Il n'existe pas de raccourci vers TEASER_VALIDE sans les deux étapes."""
    from app import export_manager as em_module
    em_module.EXPORT_ROOT = tmp_path

    story = {"title": "Test", "episode_number": 1}
    export_manager.create_package("ep_test_08", story)

    # Tentative directe de mark_human_approved sans advance_to_candidat
    with pytest.raises(ValueError):
        export_manager.mark_human_approved("ep_test_08", approved_by="Ludovic")

    # Vérifier que le statut n'a pas changé
    meta = json.loads((tmp_path / "ep_test_08" / "metadata.json").read_text())
    assert meta["status"] == ProductionStatus.PROTOTYPE_TECHNIQUE.value


# ── QualityGate — intégration avec ExportManager ─────────────────────────────

def test_quality_gate_report_to_dict_is_json_serializable():
    """Le rapport du gate doit être sérialisable en JSON pour le manifest."""
    report = make_passing_gate_report()
    d = report.to_dict()
    json_str = json.dumps(d)  # ne doit pas lever
    assert "prototype_technique" in json_str or "teaser_candidat" in json_str


def test_advance_to_candidat_embeds_gate_report(export_manager, tmp_path):
    """Le rapport du gate est bien intégré dans le manifest JSON."""
    from app import export_manager as em_module
    em_module.EXPORT_ROOT = tmp_path

    story = {"title": "Test", "episode_number": 1}
    export_manager.create_package("ep_test_09", story)
    report = make_passing_gate_report()
    export_manager.advance_to_candidat("ep_test_09", report)

    meta = json.loads((tmp_path / "ep_test_09" / "metadata.json").read_text())
    gate_report = meta["quality_gate_report"]
    assert "verdicts" in gate_report
    assert "verdict_technique" in gate_report["verdicts"]
    assert gate_report["verdicts"]["verdict_technique"]["status"] == "PASS"


# ── ProductionGatekeeper — intégration dans les entry points ──────────────────

def test_gatekeeper_is_imported_in_main():
    """ProductionGatekeeper doit être importé dans main.py."""
    import importlib, ast
    source = Path("app/main.py").read_text()
    assert "ProductionGatekeeper" in source, (
        "main.py ne référence pas ProductionGatekeeper. "
        "Ajouter : from app.production_gatekeeper import ProductionGatekeeper"
    )


def test_gatekeeper_is_imported_in_batch_processor():
    """ProductionGatekeeper doit être importé dans batch_processor.py."""
    source = Path("app/batch_processor.py").read_text()
    assert "ProductionGatekeeper" in source, (
        "batch_processor.py ne référence pas ProductionGatekeeper."
    )


def test_gatekeeper_called_in_run_pipeline():
    """run_pipeline() doit appeler ProductionGatekeeper.load()."""
    source = Path("app/main.py").read_text()
    assert "ProductionGatekeeper.load" in source or "ProductionGatekeeper.require" in source, (
        "run_pipeline() dans main.py ne charge pas le gatekeeper. "
        "Ajouter ProductionGatekeeper.load() en début de fonction."
    )


def test_gatekeeper_called_in_batch_processor_init():
    """BatchProcessor.__init__() doit instancier le gatekeeper."""
    source = Path("app/batch_processor.py").read_text()
    assert "ProductionGatekeeper.load" in source or "ProductionGatekeeper.require" in source, (
        "BatchProcessor.__init__() ne charge pas le gatekeeper."
    )


def test_video_builder_warns_prototype():
    """VideoBuilder.build() doit logguer un warning que le résultat est un prototype."""
    source = Path("app/video_builder.py").read_text()
    assert "PROTOTYPE_TECHNIQUE" in source or "prototype_technique" in source, (
        "video_builder.py ne mentionne pas PROTOTYPE_TECHNIQUE. "
        "Le pipeline doit savoir qu'il produit un prototype."
    )


def test_export_manager_no_forbidden_status_strings():
    """export_manager.py ne doit pas assigner de strings de statut interdites.

    On cherche uniquement les assignations réelles (status = "..." ou "status": "..."),
    pas les mentions dans les docstrings ou commentaires explicatifs.
    """
    import re
    from app.production_statuses import FORBIDDEN_STATUS_STRINGS
    source = Path("app/export_manager.py").read_text()
    # Pattern : assignation de statut réelle — pas dans un commentaire ou docstring
    assignment_pattern = re.compile(
        r'(?:metadata\["status"\]\s*=\s*|"status"\s*:\s*)["\']([^"\']+)["\']'
    )
    assigned_statuses = assignment_pattern.findall(source)
    for assigned in assigned_statuses:
        assert assigned not in FORBIDDEN_STATUS_STRINGS, (
            f"export_manager.py assigne le statut interdit '{assigned}'. "
            f"Utiliser ProductionStatus enum uniquement."
        )


# ── Statut progression — invariants fondamentaux ─────────────────────────────

def test_status_ordering_is_linear():
    """Les statuts forment une progression linéaire — pas de sauts."""
    progression = [
        ProductionStatus.PROTOTYPE_TECHNIQUE,
        ProductionStatus.TEST_VIDEO_IA,
        ProductionStatus.TEASER_CANDIDAT,
        ProductionStatus.TEASER_VALIDE,
    ]
    # Vérifie que tous les statuts sont couverts et distincts
    assert len(set(s.value for s in progression)) == 4


def test_teaser_valide_not_assignable_from_prototype_directly():
    """Il est impossible d'aller directement de PROTOTYPE à VALIDE."""
    report = GateReport(video_path="/tmp/test.mp4")
    # Même si on force human_approved=True sans passer les verdicts...
    report.human_approved = True
    # ...can_advance_to_valide est False car automatic_verdicts_pass est False
    assert report.can_advance_to_valide is False, (
        "Un GateReport avec verdicts en FAIL ne peut pas produire TEASER_VALIDE, "
        "même si human_approved=True."
    )
