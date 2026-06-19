"""Rôles métier du moteur vidéo YAWatch-LUNA.

Chaque rôle encode les règles d'un domaine et expose validate(context) -> VerdictResult.
Tous les rôles sont instanciés par ProductionGatekeeper avant toute production vidéo.
"""

from app.roles.base_role import BaseRole, RuleViolation, VerdictResult
from app.roles.video_generation_engineer import VideoGenerationEngineer
from app.roles.motion_engineer import MotionEngineer
from app.roles.monteur_cinema import MonteurCinema
from app.roles.sound_designer import SoundDesigner
from app.roles.video_qa_engineer import VideoQAEngineer
from app.roles.trailer_designer import TrailerDesigner

ALL_ROLES: list[type[BaseRole]] = [
    VideoGenerationEngineer,
    MotionEngineer,
    MonteurCinema,
    SoundDesigner,
    VideoQAEngineer,
    TrailerDesigner,
]

__all__ = [
    "BaseRole", "RuleViolation", "VerdictResult",
    "VideoGenerationEngineer", "MotionEngineer", "MonteurCinema",
    "SoundDesigner", "VideoQAEngineer", "TrailerDesigner",
    "ALL_ROLES",
]
