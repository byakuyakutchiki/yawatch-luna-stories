"""Rôle : Trailer Designer.

Responsabilité : valider que le teaser respecte la structure narrative,
le hook en 3 secondes, la title card finale, les safe zones YouTube Shorts.
"""

from pathlib import Path
from typing import Optional

from app.roles.base_role import BaseRole, VerdictResult

HOOK_WINDOW_S = 3.0          # Le hook doit être dans les 3 premières secondes
TITLE_CARD_DURATION_MIN = 2.0
TEASER_DURATION_MIN = 24.0
TEASER_DURATION_MAX = 32.0

REQUIRED_TITLE_CARD_TEXT = "LUNA"   # Au minimum ce mot dans la title card finale
CANON_TITLE_CARD = "LUNA / Tout a commencé par un secret."

# Safe zones YouTube Shorts 1080×1920
SAFE_ZONE_TOP_PX = 120
SAFE_ZONE_BOTTOM_PX = 1750
SAFE_ZONE_RIGHT_PX = 880


class TrailerDesigner(BaseRole):
    role_name = "TrailerDesigner"
    knowledge_doc = "VIDEO_ENGINE_ARCHITECTURE.md"
    verdict_name = "verdict_storytelling"

    def validate(self, context: dict) -> VerdictResult:
        """
        context attendu :
          - "has_hook" : bool — un hook visuel fort existe dans les 3 premières secondes
          - "hook_plan" : str — description du plan de hook (optionnel)
          - "title_card_text" : str — texte de la title card finale
          - "title_card_duration" : float — durée de la title card en secondes
          - "total_duration" : float — durée totale du teaser
          - "subtitle_style_validated" : bool — style sous-titres validé
          - "safe_zones_checked" : bool — les éléments sont dans les safe zones
          - "human_watched" : bool — Ludovic a regardé le teaser
          - "human_verdict" : str — "approved" si validé humainement
        """
        errors: list[str] = []
        warnings: list[str] = []

        has_hook: bool = context.get("has_hook", False)
        hook_plan: str = context.get("hook_plan", "")
        title_card_text: str = context.get("title_card_text", "")
        title_card_duration: float = context.get("title_card_duration", 0.0)
        total_duration: float = context.get("total_duration", 0.0)
        subtitle_style_validated: bool = context.get("subtitle_style_validated", False)
        safe_zones_checked: bool = context.get("safe_zones_checked", False)
        human_watched: bool = context.get("human_watched", False)
        human_verdict: str = context.get("human_verdict", "")

        # Règle 1 : hook obligatoire dans les 3 premières secondes
        if not has_hook:
            errors.append(
                "Aucun hook déclaré dans les 3 premières secondes. "
                "Le plan d'ouverture du teaser doit accrocher immédiatement "
                "(Tour YAWatch révélée, ou Luna au bureau en tension). "
                "Voir TEASER_S01E00_PRODUCTION_PACK.md — Plan 1."
            )

        # Règle 2 : title card finale obligatoire
        if not title_card_text:
            errors.append(
                "Aucune title card finale déclarée. "
                f"Le teaser doit se terminer par : '{CANON_TITLE_CARD}'"
            )
        elif REQUIRED_TITLE_CARD_TEXT.upper() not in title_card_text.upper():
            errors.append(
                f"Title card ne contient pas '{REQUIRED_TITLE_CARD_TEXT}'. "
                f"Text attendu : '{CANON_TITLE_CARD}'"
            )

        if title_card_duration > 0 and title_card_duration < TITLE_CARD_DURATION_MIN:
            warnings.append(
                f"Title card trop courte : {title_card_duration:.1f}s "
                f"(minimum {TITLE_CARD_DURATION_MIN}s). "
                "Le spectateur doit avoir le temps de lire."
            )

        # Règle 3 : durée totale du teaser
        if total_duration > 0:
            if not (TEASER_DURATION_MIN <= total_duration <= TEASER_DURATION_MAX):
                errors.append(
                    f"Durée teaser {total_duration:.1f}s hors plage "
                    f"[{TEASER_DURATION_MIN}-{TEASER_DURATION_MAX}s]. "
                    "Voir TEASER_S01E00_PRODUCTION_PACK.md."
                )

        # Règle 4 : style sous-titres
        if not subtitle_style_validated:
            warnings.append(
                "subtitle_style_validated=False. "
                "Vérifier : Montserrat Bold, 72px, blanc, contour 3px noir, "
                "MarginV=180, max 35 caractères/ligne. "
                "Voir FFMPEG_PROFESSIONAL_VIDEO_PIPELINE.md section 5."
            )

        # Règle 5 : safe zones
        if not safe_zones_checked:
            warnings.append(
                "safe_zones_checked=False. "
                "Vérifier que le contenu principal est entre y=120 et y=1750 "
                "et x=0 et x=880. Interface YouTube masque les bords."
            )

        # Règle 6 : validation humaine OBLIGATOIRE
        if not human_watched:
            return VerdictResult(
                self.verdict_name, "NEEDS_HUMAN",
                errors + [
                    "Le verdict storytelling requiert un visionnage humain. "
                    "Ludovic doit regarder le teaser sur mobile avec casque. "
                    "Appeler QualityGate.record_human_verdict() après visionnage."
                ],
                warnings
            )

        if human_verdict.lower() != "approved":
            return VerdictResult(
                self.verdict_name, "FAIL",
                errors + [
                    f"Verdict humain : '{human_verdict}' (attendu 'approved'). "
                    "Le teaser a été visionné mais non approuvé."
                ],
                warnings
            )

        if errors:
            return VerdictResult(self.verdict_name, "FAIL", errors, warnings)
        return VerdictResult(self.verdict_name, "PASS", [], warnings)
