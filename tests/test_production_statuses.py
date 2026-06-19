"""Tests des statuts de production et des guards contre les strings interdites."""

import pytest
from app.production_statuses import ProductionStatus, assert_not_forbidden, FORBIDDEN_STATUS_STRINGS


def test_status_values_are_stable():
    assert ProductionStatus.PROTOTYPE_TECHNIQUE.value == "prototype_technique"
    assert ProductionStatus.TEST_VIDEO_IA.value == "test_video_ia"
    assert ProductionStatus.TEASER_CANDIDAT.value == "teaser_candidat"
    assert ProductionStatus.TEASER_VALIDE.value == "teaser_valide"


def test_forbidden_strings_raises():
    for bad in FORBIDDEN_STATUS_STRINGS:
        with pytest.raises(ValueError, match="interdit"):
            assert_not_forbidden(bad)


def test_forbidden_strings_case_insensitive():
    with pytest.raises(ValueError):
        assert_not_forbidden("READY")
    with pytest.raises(ValueError):
        assert_not_forbidden("Production_Ready")


def test_valid_status_does_not_raise():
    for status in ProductionStatus:
        assert_not_forbidden(status.value)  # les valeurs de l'enum sont autorisées


def test_status_is_string_comparable():
    # ProductionStatus hérite de str — compatible avec JSON et comparaisons directes
    assert ProductionStatus.PROTOTYPE_TECHNIQUE == "prototype_technique"
    assert ProductionStatus.TEASER_VALIDE != "ready"
