"""Module MotionDirector — préparateur de VideoJob piloté par les bibliothèques.

Respecte le principe de gouvernance YAWatch-LUNA :

    bibliothèques → MotionDirector → VideoJob → backend ComfyUI → Quality Gate → humain

Le MotionDirector lit la connaissance (CHARACTER_BIBLE, VISUAL_DIRECTION,
TEASER_S01E00_PRODUCTION_PACK, MOTION_CONTROL_RULES) et produit un job exécutable.
Il ne génère ni ne valide rien.
"""

from app.motion_director.director import (
    MotionDirector,
    TargetPaths,
    LibrariesNotAvailable,
    REQUIRED_LIBRARIES,
)

__all__ = ["MotionDirector", "TargetPaths", "LibrariesNotAvailable", "REQUIRED_LIBRARIES"]
