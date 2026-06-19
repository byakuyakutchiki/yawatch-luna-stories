"""Base commune à tous les rôles métier du moteur vidéo YAWatch-LUNA."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


@dataclass
class RuleViolation:
    rule: str
    detail: str
    blocking: bool = True  # False = warning seulement


@dataclass
class VerdictResult:
    verdict_name: str
    status: Literal["PASS", "FAIL", "NEEDS_HUMAN"]
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status == "PASS"

    @property
    def blocks(self) -> bool:
        return self.status in ("FAIL", "NEEDS_HUMAN")

    def __str__(self) -> str:
        icon = {"PASS": "✓", "FAIL": "✗", "NEEDS_HUMAN": "👁"}.get(self.status, "?")
        lines = [f"{icon} {self.verdict_name}: {self.status}"]
        for e in self.errors:
            lines.append(f"    ERREUR: {e}")
        for w in self.warnings:
            lines.append(f"    AVERT: {w}")
        return "\n".join(lines)


class BaseRole:
    """Rôle métier abstrait — chaque rôle implémente validate()."""

    role_name: str = "BaseRole"
    knowledge_doc: str = ""  # filename in docs/AI_VIDEO_ENGINE_KNOWLEDGE/
    verdict_name: str = "verdict_base"

    KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent.parent / "docs" / "AI_VIDEO_ENGINE_KNOWLEDGE"

    def is_knowledge_loaded(self) -> bool:
        """Vérifie que le document de connaissance du rôle existe sur disque."""
        if not self.knowledge_doc:
            return True
        return (self.KNOWLEDGE_DIR / self.knowledge_doc).exists()

    def validate(self, context: dict) -> VerdictResult:
        """Valide le contexte selon les règles du rôle. À implémenter."""
        raise NotImplementedError(f"{self.role_name}.validate() non implémenté")

    def describe(self) -> str:
        return f"[{self.role_name}] knowledge_doc={self.knowledge_doc}"
