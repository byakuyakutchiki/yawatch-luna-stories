"""Chargement configuration YAML + .env"""

import logging
import os
from pathlib import Path
from typing import Any, Optional

import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class ConfigLoader:
    def __init__(self, config_path: Optional[Path] = None):
        if config_path is None:
            config_path = PROJECT_ROOT / "config" / "settings.yaml"
        load_dotenv(PROJECT_ROOT / ".env")
        self._config = self._load_yaml(config_path)
        self._inject_env()

    def _load_yaml(self, path: Path) -> dict:
        try:
            with open(path, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            raise FileNotFoundError(f"Config introuvable: {path}")
        except yaml.YAMLError as e:
            raise ValueError(f"YAML invalide: {e}")

    def _inject_env(self):
        if key := os.getenv("OPENAI_API_KEY"):
            self._config["openai_api_key"] = key

    def get(self, key: str, default: Any = None) -> Any:
        """Accès par clé pointée: 'content.script_duration'"""
        value = self._config
        for part in key.split("."):
            if not isinstance(value, dict):
                return default
            value = value.get(part, default)
            if value is default:
                return default
        return value

    def get_path(self, key: str) -> Path:
        """Retourne un chemin absolu ancré sur PROJECT_ROOT."""
        raw = self.get(key)
        if raw is None:
            raise ValueError(f"Chemin non trouvé dans la config: {key}")
        p = Path(raw)
        return p if p.is_absolute() else PROJECT_ROOT / p

    @property
    def openai_key(self) -> Optional[str]:
        return self._config.get("openai_api_key")
