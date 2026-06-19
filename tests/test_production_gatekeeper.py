"""Tests du ProductionGatekeeper — chargement des rôles et de la base de connaissances."""

import pytest
from pathlib import Path
from app.production_gatekeeper import ProductionGatekeeper, KnowledgeBaseNotLoaded, KNOWLEDGE_DIR
from app.roles import ALL_ROLES


def test_knowledge_dir_exists():
    """La base de connaissances doit être présente dans le repo."""
    assert KNOWLEDGE_DIR.exists(), (
        f"Dossier de connaissances absent : {KNOWLEDGE_DIR}. "
        "Créer docs/AI_VIDEO_ENGINE_KNOWLEDGE/ avec les 7 documents."
    )


def test_all_knowledge_docs_present():
    """Les 7 documents obligatoires doivent exister."""
    from app.production_gatekeeper import REQUIRED_KNOWLEDGE_DOCS
    missing = [d for d in REQUIRED_KNOWLEDGE_DOCS if not (KNOWLEDGE_DIR / d).exists()]
    assert not missing, f"Documents manquants : {missing}"


def test_gatekeeper_loads_all_roles():
    gk = ProductionGatekeeper.load(strict=False)
    for role_class in ALL_ROLES:
        role = gk.get_role(role_class.role_name)
        assert role is not None
        assert role.role_name == role_class.role_name


def test_gatekeeper_require_succeeds_when_docs_present():
    """require() ne doit pas lever si tous les docs sont présents."""
    gk = ProductionGatekeeper.require()
    assert gk is not None


def test_gatekeeper_role_access_by_property():
    gk = ProductionGatekeeper.load(strict=False)
    assert gk.video_qa_engineer is not None
    assert gk.motion_engineer is not None
    assert gk.monteur_cinema is not None
    assert gk.sound_designer is not None
    assert gk.video_generation_engineer is not None
    assert gk.trailer_designer is not None


def test_gatekeeper_assert_not_placeholder_passes_canon():
    gk = ProductionGatekeeper.load(strict=False)
    canon_images = [
        Path("assets/luna_stories_assets/01_luna_adulte/luna_adulte_neutral_9x16_01.png"),
        Path("assets/luna_stories_assets/03_aby/aby_adulte_observing_luna_01.png"),
    ]
    gk.assert_not_placeholder(canon_images)  # ne doit pas lever


def test_gatekeeper_assert_not_placeholder_blocks_test_images():
    gk = ProductionGatekeeper.load(strict=False)
    placeholder_images = [
        Path("content/images/episode_test/scene_hook.jpg"),
        Path("content/images/episode_test/scene_story.jpg"),
    ]
    with pytest.raises(ValueError, match="placeholder"):
        gk.assert_not_placeholder(placeholder_images)


def test_gatekeeper_unknown_role_raises():
    gk = ProductionGatekeeper.load(strict=False)
    with pytest.raises(KeyError):
        gk.get_role("RoleInexistant")


def test_status_report_is_string():
    gk = ProductionGatekeeper.load(strict=False)
    report = gk.status_report()
    assert isinstance(report, str)
    assert "ProductionGatekeeper" in report
