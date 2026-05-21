"""Fonctions utilitaires communes"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_text(content: str, filepath: Path) -> bool:
    try:
        ensure_dir(filepath.parent)
        filepath.write_text(content, encoding="utf-8")
        return True
    except OSError as e:
        logger.error("Erreur sauvegarde %s: %s", filepath, e)
        return False


def load_text(filepath: Path) -> str:
    try:
        return filepath.read_text(encoding="utf-8")
    except OSError as e:
        logger.error("Erreur chargement %s: %s", filepath, e)
        return ""


def save_json(data: Dict[str, Any], filepath: Path) -> bool:
    try:
        ensure_dir(filepath.parent)
        filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except OSError as e:
        logger.error("Erreur sauvegarde JSON %s: %s", filepath, e)
        return False


def load_json(filepath: Path) -> Optional[Dict[str, Any]]:
    """Charge un fichier JSON. Retourne None si absent ou invalide."""
    try:
        return json.loads(filepath.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        logger.error("JSON invalide dans %s: %s", filepath, e)
        return None


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def clean_text(text: str) -> str:
    return text.strip().replace("\n\n\n", "\n\n")


def get_logger(name: str) -> logging.Logger:
    """Alias pratique pour les modules DeepSeek."""
    return logging.getLogger(name)
