"""Quality Gate bloquant à 6 verdicts — YAWatch-LUNA.

Aucun fichier ne peut obtenir STATUS=TEASER_VALIDE sans passer ce gate.
La validation humaine (verdict storytelling) ne peut pas être bypassée.

Usage :
    gate = QualityGate(gatekeeper)
    report = gate.run(video_context, character_context, storytelling_context)
    print(report)
    if report.can_advance_to_candidat:
        # ...passer à TEASER_CANDIDAT
    # Pour passer à TEASER_VALIDE, seul human_approve() est autorisé
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from app.production_gatekeeper import ProductionGatekeeper
from app.production_statuses import ProductionStatus
from app.roles.base_role import VerdictResult

logger = logging.getLogger(__name__)


@dataclass
class GateReport:
    """Rapport complet du Quality Gate."""
    video_path: str
    run_date: str = field(default_factory=lambda: datetime.now().isoformat())

    verdict_technique: VerdictResult = field(
        default_factory=lambda: VerdictResult("verdict_technique", "FAIL", ["Non exécuté"], [])
    )
    verdict_mouvement: VerdictResult = field(
        default_factory=lambda: VerdictResult("verdict_mouvement", "FAIL", ["Non exécuté"], [])
    )
    verdict_montage: VerdictResult = field(
        default_factory=lambda: VerdictResult("verdict_montage", "FAIL", ["Non exécuté"], [])
    )
    verdict_son: VerdictResult = field(
        default_factory=lambda: VerdictResult("verdict_son", "FAIL", ["Non exécuté"], [])
    )
    verdict_coherence_personnage: VerdictResult = field(
        default_factory=lambda: VerdictResult("verdict_coherence_personnage", "FAIL", ["Non exécuté"], [])
    )
    verdict_storytelling: VerdictResult = field(
        default_factory=lambda: VerdictResult("verdict_storytelling", "NEEDS_HUMAN", ["Non exécuté"], [])
    )

    human_approved: bool = False
    human_approved_by: str = ""
    human_approved_date: str = ""

    @property
    def all_verdicts(self) -> list[VerdictResult]:
        return [
            self.verdict_technique,
            self.verdict_mouvement,
            self.verdict_montage,
            self.verdict_son,
            self.verdict_coherence_personnage,
            self.verdict_storytelling,
        ]

    @property
    def automatic_verdicts_pass(self) -> bool:
        """True si les 5 verdicts automatiques passent (hors storytelling humain)."""
        auto = [
            self.verdict_technique,
            self.verdict_mouvement,
            self.verdict_montage,
            self.verdict_son,
            self.verdict_coherence_personnage,
        ]
        return all(v.status == "PASS" for v in auto)

    @property
    def can_advance_to_candidat(self) -> bool:
        """True si le fichier peut passer en TEASER_CANDIDAT (en attente validation humaine)."""
        return self.automatic_verdicts_pass

    @property
    def can_advance_to_valide(self) -> bool:
        """True si le fichier peut être marqué TEASER_VALIDE."""
        return self.automatic_verdicts_pass and self.human_approved

    @property
    def current_status(self) -> ProductionStatus:
        if self.can_advance_to_valide:
            return ProductionStatus.TEASER_VALIDE
        if self.can_advance_to_candidat:
            return ProductionStatus.TEASER_CANDIDAT
        return ProductionStatus.PROTOTYPE_TECHNIQUE

    def __str__(self) -> str:
        lines = [
            "=" * 60,
            f"QUALITY GATE — {Path(self.video_path).name}",
            f"Date : {self.run_date}",
            "=" * 60,
        ]
        for v in self.all_verdicts:
            lines.append(str(v))
        lines.append("-" * 60)
        lines.append(f"Verdicts automatiques : {'PASS' if self.automatic_verdicts_pass else 'FAIL'}")
        if self.human_approved:
            lines.append(
                f"Validation humaine : APPROVED par {self.human_approved_by} "
                f"le {self.human_approved_date}"
            )
        else:
            lines.append("Validation humaine : EN ATTENTE")
        lines.append(f"Statut résultant : {self.current_status.value}")
        lines.append("=" * 60)
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "video_path": self.video_path,
            "run_date": self.run_date,
            "verdicts": {
                v.verdict_name: {
                    "status": v.status,
                    "errors": v.errors,
                    "warnings": v.warnings,
                }
                for v in self.all_verdicts
            },
            "human_approved": self.human_approved,
            "human_approved_by": self.human_approved_by,
            "human_approved_date": self.human_approved_date,
            "final_status": self.current_status.value,
        }


class QualityGate:
    """Quality Gate à 6 verdicts — point d'entrée unique pour la validation."""

    def __init__(self, gatekeeper: ProductionGatekeeper) -> None:
        self._gk = gatekeeper

    def run(
        self,
        video_context: dict,
        character_context: dict | None = None,
        storytelling_context: dict | None = None,
    ) -> GateReport:
        """
        Exécute les 6 verdicts.

        video_context : dict avec au minimum "video_path" et les champs pour
                        VideoQAEngineer, MotionEngineer, MonteurCinema, SoundDesigner,
                        VideoGenerationEngineer.

        character_context : dict pour la vérification cohérence personnage.
                            Si absent, utilise video_context.

        storytelling_context : dict pour TrailerDesigner.
                               Doit contenir "human_watched" et "human_verdict".
                               Si absent, le verdict est NEEDS_HUMAN automatiquement.
        """
        video_path = str(video_context.get("video_path", ""))
        report = GateReport(video_path=video_path)

        # Verdict 1 — Technique (VideoQAEngineer)
        report.verdict_technique = self._gk.video_qa_engineer.validate(video_context)
        logger.info("Verdict technique : %s", report.verdict_technique.status)

        # Verdict 2 — Mouvement (MotionEngineer)
        report.verdict_mouvement = self._gk.motion_engineer.validate(video_context)
        logger.info("Verdict mouvement : %s", report.verdict_mouvement.status)

        # Verdict 3 — Montage (MonteurCinema)
        report.verdict_montage = self._gk.monteur_cinema.validate(video_context)
        logger.info("Verdict montage : %s", report.verdict_montage.status)

        # Verdict 4 — Son (SoundDesigner)
        report.verdict_son = self._gk.sound_designer.validate(video_context)
        logger.info("Verdict son : %s", report.verdict_son.status)

        # Verdict 5 — Cohérence personnage (VideoGenerationEngineer)
        ctx_char = character_context if character_context is not None else video_context
        report.verdict_coherence_personnage = self._gk.video_generation_engineer.validate(ctx_char)
        logger.info("Verdict cohérence personnage : %s", report.verdict_coherence_personnage.status)

        # Verdict 6 — Storytelling (TrailerDesigner) — NEEDS_HUMAN si pas de contexte humain
        ctx_story = storytelling_context if storytelling_context is not None else {}
        if not ctx_story.get("human_watched"):
            report.verdict_storytelling = VerdictResult(
                "verdict_storytelling",
                "NEEDS_HUMAN",
                [
                    "Visionnage humain requis. "
                    "Ludovic doit regarder le teaser sur mobile avec casque, "
                    "puis appeler QualityGate.record_human_verdict()."
                ],
                [],
            )
        else:
            report.verdict_storytelling = self._gk.trailer_designer.validate(ctx_story)
        logger.info("Verdict storytelling : %s", report.verdict_storytelling.status)

        logger.info(
            "Quality Gate terminé — statut résultant : %s",
            report.current_status.value
        )
        return report

    def record_human_verdict(
        self,
        report: GateReport,
        approved: bool,
        approved_by: str,
        notes: str = "",
    ) -> GateReport:
        """
        Enregistre la décision humaine après visionnage.
        C'est la SEULE voie vers TEASER_VALIDE.

        approved_by doit être un nom réel (ex: "Ludovic").
        Cette méthode ne peut pas être appelée depuis un agent automatique.
        """
        if not approved_by or approved_by.strip().lower() in ("claude", "codex", "agent", "ai", "bot"):
            raise ValueError(
                f"approved_by='{approved_by}' n'est pas un nom humain valide. "
                "Seul Ludovic peut approuver un teaser."
            )

        report.human_approved = approved
        report.human_approved_by = approved_by.strip()
        report.human_approved_date = datetime.now().isoformat()

        if approved:
            report.verdict_storytelling = VerdictResult(
                "verdict_storytelling",
                "PASS",
                [],
                [f"Approuvé par {approved_by}. Notes : {notes}" if notes else f"Approuvé par {approved_by}."],
            )
            logger.info(
                "Teaser approuvé par %s — TEASER_VALIDE", approved_by
            )
        else:
            report.verdict_storytelling = VerdictResult(
                "verdict_storytelling",
                "FAIL",
                [f"Rejeté par {approved_by}. Notes : {notes}" if notes else f"Rejeté par {approved_by}."],
                [],
            )
            logger.info("Teaser rejeté par %s — retour pipeline", approved_by)

        return report
