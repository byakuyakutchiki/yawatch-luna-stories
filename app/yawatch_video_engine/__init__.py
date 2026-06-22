"""YAWatch Video Engine MVP package.

This package exposes a local API-first architecture for producing narrative
shots for YAWatch-LUNA. Heavy I2V engines are adapter plugins; the core engine
keeps the cinematic intent, run folders, metadata, and quality review stable.
"""

__all__ = ["generate_shot"]

from .engine import generate_shot
