"""Rôle : Motion Engineer.

Responsabilité : valider que les mouvements sont cinématiques, pas un diaporama.
Règle Ken Burns : 20% maximum des plans.
"""

import subprocess
import json
from pathlib import Path
from typing import Optional

from app.roles.base_role import BaseRole, VerdictResult

MAX_KEN_BURNS_RATIO = 0.20  # 20% max des plans


class MotionEngineer(BaseRole):
    role_name = "MotionEngineer"
    knowledge_doc = "IMAGE_TO_VIDEO_ENGINE_RULES.md"
    verdict_name = "verdict_mouvement"

    def validate(self, context: dict) -> VerdictResult:
        """
        context attendu :
          - "clips" : list[str|Path] — clips à valider
          - "ken_burns_count" : int — nombre de plans en Ken Burns FFmpeg
          - "total_plans" : int — nombre total de plans
          - "i2v_tool" : str — outil utilisé
          - "zoompan_params" : dict — paramètres zoompan si utilisé (optionnel)
        """
        errors: list[str] = []
        warnings: list[str] = []

        clips: list[str] = [str(p) for p in context.get("clips", [])]
        ken_burns_count: int = context.get("ken_burns_count", 0)
        total_plans: int = context.get("total_plans", len(clips))
        i2v_tool: str = context.get("i2v_tool", "unknown").lower()
        zoompan_params: dict = context.get("zoompan_params", {})

        # Règle 1 : ratio Ken Burns
        if total_plans > 0:
            ratio = ken_burns_count / total_plans
            if ratio > MAX_KEN_BURNS_RATIO:
                errors.append(
                    f"Trop de plans en Ken Burns FFmpeg : {ken_burns_count}/{total_plans} "
                    f"({ratio:.0%}). Maximum autorisé : {MAX_KEN_BURNS_RATIO:.0%}. "
                    "Générer les plans manquants avec Kling ou SVD."
                )

        # Règle 2 : si FFmpeg seul, c'est forcément du diaporama
        if i2v_tool in ("ffmpeg", "moviepy") and total_plans > 0:
            if ken_burns_count < total_plans:
                non_kb = total_plans - ken_burns_count
                errors.append(
                    f"{non_kb} plan(s) assemblé(s) depuis des images fixes sans Ken Burns "
                    "— résultat = slideshow immobile. "
                    "Tout plan avec un personnage vivant nécessite un outil IA."
                )

        # Règle 3 : paramètres zoompan (si applicable)
        if zoompan_params:
            fps_in_filter = zoompan_params.get("fps_specified", False)
            increment = zoompan_params.get("zoom_increment", 0.002)
            max_zoom = zoompan_params.get("max_zoom", 2.0)
            xy_anchored = zoompan_params.get("xy_anchored", False)

            if not fps_in_filter:
                errors.append(
                    "zoompan sans fps=25 spécifié → zoom tremblant garanti. "
                    "Ajouter 'fps=25' AVANT zoompan dans le filtre. "
                    "Voir FFMPEG_PROFESSIONAL_VIDEO_PIPELINE.md section 2."
                )
            if increment > 0.0015:
                warnings.append(
                    f"zoom_increment={increment} trop élevé (recommandé ≤ 0.0012). "
                    "Mouvement visible et brusque."
                )
            if max_zoom > 1.15:
                warnings.append(
                    f"max_zoom={max_zoom} trop élevé (recommandé ≤ 1.15). "
                    "Perte de qualité et effet grossier."
                )
            if not xy_anchored:
                errors.append(
                    "zoompan sans x,y ancrés explicitement → dérive aléatoire de caméra. "
                    "Spécifier x='iw/2-(iw/zoom/2)' et y='ih/2-(ih/zoom/2)'."
                )

        # Règle 4 : vérifier que les clips vidéo ont une durée réelle
        for clip_path in clips:
            p = Path(clip_path)
            if not p.exists():
                continue
            duration = _get_clip_duration(clip_path)
            if duration is not None and duration < 2.0:
                warnings.append(
                    f"Clip très court ({duration:.1f}s) : {p.name}. "
                    "Durée minimale recommandée : 3s pour un plan cinématique."
                )

        if errors:
            return VerdictResult(self.verdict_name, "FAIL", errors, warnings)
        return VerdictResult(self.verdict_name, "PASS", [], warnings)


def _get_clip_duration(clip_path: str) -> Optional[float]:
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", clip_path],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return float(result.stdout.strip())
    except Exception:
        pass
    return None
