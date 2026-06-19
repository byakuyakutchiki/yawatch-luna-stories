"""Statuts officiels du pipeline vidéo YAWatch-LUNA.

Règle absolue :
- TEASER_VALIDE ne peut être assigné que par un humain (Ludovic) après visionnage.
- Toute string ambiguë ("usable", "ready", "production_ready"...) est interdite.
- Le pipeline ne peut assigner que PROTOTYPE_TECHNIQUE ou TEST_VIDEO_IA.
"""

from enum import Enum


class ProductionStatus(str, Enum):
    PROTOTYPE_TECHNIQUE = "prototype_technique"
    # FFmpeg local, images placeholder possibles, jamais publié.
    # Assigné automatiquement par le pipeline.

    TEST_VIDEO_IA = "test_video_ia"
    # Clip généré par Kling/SVD/CogVideoX, visionné individuellement.
    # Assigné après téléchargement du clip IA ET visionnage humain du clip seul.

    TEASER_CANDIDAT = "teaser_candidat"
    # Assemblage complet avec clips IA validés + audio canon.
    # A passé les verdicts technique, mouvement et son automatiques.
    # En attente de validation humaine complète (verdicts artistique + storytelling).

    TEASER_VALIDE = "teaser_valide"
    # Approuvé par Ludovic après visionnage complet sur mobile avec casque.
    # SEUL statut publié sur YouTube.
    # NE PEUT PAS être assigné par du code — uniquement par la méthode
    # QualityGate.approve_human(approved_by="Ludovic").


# Strings interdites dans tout le pipeline.
# Si l'une d'elles apparaît dans un champ "status" d'un manifest JSON,
# ProductionGatekeeper.assert_clean_status() lève une erreur.
FORBIDDEN_STATUS_STRINGS: frozenset[str] = frozenset({
    "usable",
    "ready",
    "production_ready",
    "ready_for_review",
    "final",
    "approved",
    "done",
    "complete",
    "finished",
    "ok",
})


def assert_not_forbidden(status: str) -> None:
    """Lève ValueError si le statut est une string interdite."""
    normalized = status.lower().strip()
    if normalized in FORBIDDEN_STATUS_STRINGS:
        raise ValueError(
            f"Statut interdit : '{status}'. "
            f"Utiliser ProductionStatus enum uniquement. "
            f"TEASER_VALIDE ne peut être assigné que par validation humaine explicite."
        )
