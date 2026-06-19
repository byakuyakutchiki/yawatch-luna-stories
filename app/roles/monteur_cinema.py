"""Rôle : Monteur cinéma.

Responsabilité : valider la structure du montage — offsets xfade, durée totale,
nombre de plans, cohérence avec le PRODUCTION_PACK.
"""

import subprocess
from pathlib import Path
from typing import Optional

from app.roles.base_role import BaseRole, VerdictResult

TEASER_EXPECTED_PLANS = 9
TEASER_DURATION_MIN = 24.0
TEASER_DURATION_MAX = 32.0
XFADE_DURATION = 0.5
MIN_PLAN_DURATION = 2.5  # secondes


class MonteurCinema(BaseRole):
    role_name = "MonteurCinema"
    knowledge_doc = "FFMPEG_PROFESSIONAL_VIDEO_PIPELINE.md"
    verdict_name = "verdict_montage"

    def validate(self, context: dict) -> VerdictResult:
        """
        context attendu :
          - "assembled_path" : str|Path — fichier MP4 assemblé (optionnel)
          - "plan_durations" : list[float] — durée de chaque clip en secondes
          - "xfade_offsets" : list[float] — offsets calculés pour les xfades
          - "episode_id" : str — pour appliquer les contraintes spécifiques
          - "n_plans" : int — nombre de plans (si pas de plan_durations)
        """
        errors: list[str] = []
        warnings: list[str] = []

        plan_durations: list[float] = context.get("plan_durations", [])
        xfade_offsets: list[float] = context.get("xfade_offsets", [])
        episode_id: str = context.get("episode_id", "")
        assembled_path: Optional[str] = context.get("assembled_path")
        n_plans: int = context.get("n_plans", len(plan_durations))

        # Règle 1 : offsets xfade non négatifs
        for i, offset in enumerate(xfade_offsets):
            if offset <= 0:
                errors.append(
                    f"xfade offset[{i}] = {offset:.3f}s → négatif ou nul. "
                    "Provoque un crash FFmpeg ou une transition manquante. "
                    "Le clip précédent est trop court pour un xfade de "
                    f"{XFADE_DURATION}s."
                )

        # Règle 2 : durée minimale par plan
        for i, dur in enumerate(plan_durations):
            if dur < MIN_PLAN_DURATION:
                warnings.append(
                    f"Plan {i+1} : durée {dur:.1f}s < {MIN_PLAN_DURATION}s. "
                    "Un plan trop court ne laisse pas le temps à l'émotion de s'installer."
                )

        # Règle 3 : contraintes teaser
        if "teaser" in episode_id.lower() or "s01e00" in episode_id.lower():
            if n_plans and n_plans != TEASER_EXPECTED_PLANS:
                errors.append(
                    f"Teaser S01E00 requiert exactement {TEASER_EXPECTED_PLANS} plans "
                    f"(TEASER_S01E00_PRODUCTION_PACK.md). Trouvé : {n_plans}."
                )

        # Règle 4 : durée totale de l'assemblage
        if assembled_path and Path(str(assembled_path)).exists():
            duration = _get_video_duration(str(assembled_path))
            if duration is not None:
                if "teaser" in episode_id.lower() or "s01e00" in episode_id.lower():
                    if not (TEASER_DURATION_MIN <= duration <= TEASER_DURATION_MAX):
                        errors.append(
                            f"Durée assemblage teaser : {duration:.1f}s. "
                            f"Attendu : {TEASER_DURATION_MIN}-{TEASER_DURATION_MAX}s "
                            "selon TEASER_S01E00_PRODUCTION_PACK.md."
                        )

        # Règle 5 : cohérence offsets vs plans
        if plan_durations and xfade_offsets:
            expected_n_offsets = len(plan_durations) - 1
            if len(xfade_offsets) != expected_n_offsets:
                errors.append(
                    f"Nombre d'offsets xfade incohérent : {len(xfade_offsets)} offsets "
                    f"pour {len(plan_durations)} plans (attendu {expected_n_offsets})."
                )

        if errors:
            return VerdictResult(self.verdict_name, "FAIL", errors, warnings)
        return VerdictResult(self.verdict_name, "PASS", [], warnings)


def _get_video_duration(path: str) -> Optional[float]:
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            return float(result.stdout.strip())
    except Exception:
        pass
    return None
