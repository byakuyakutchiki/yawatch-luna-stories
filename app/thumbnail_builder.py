"""Génération de miniatures YouTube (1280×720) — PIL ou placeholder."""

import logging
import textwrap
from pathlib import Path
from typing import Optional

from app.utils import ensure_dir, get_logger

logger = get_logger(__name__)

THUMB_W, THUMB_H = 1280, 720
ASSETS = Path(__file__).resolve().parent.parent / "assets" / "thumbnails"


class ThumbnailBuilder:
    def __init__(self):
        self._pil_available = self._check_pil()
        ensure_dir(ASSETS)
        self.output_dir = Path(__file__).resolve().parent.parent / "outputs" / "thumbnails"
        ensure_dir(self.output_dir)

    def _check_pil(self) -> bool:
        try:
            from PIL import Image  # noqa: F401
            return True
        except ImportError:
            logger.info("Pillow non installé — thumbnails en mode placeholder")
            return False

    def generate(
        self,
        background_image: Optional[Path],
        title: str,
        episode_id: str,
    ) -> Path:
        output = self.output_dir / f"thumbnail_{episode_id}.jpg"

        if self._pil_available and background_image and background_image.exists():
            return self._generate_pil(background_image, title, output)
        return self._generate_placeholder(title, episode_id, output)

    def _generate_pil(self, bg_path: Path, title: str, output: Path) -> Path:
        from PIL import Image, ImageDraw, ImageFont

        # Fond
        bg = Image.open(bg_path).convert("RGB").resize((THUMB_W, THUMB_H), Image.LANCZOS)

        # Calque sombre
        from PIL import ImageEnhance
        bg = ImageEnhance.Brightness(bg).enhance(0.45)

        draw = ImageDraw.Draw(bg)

        # Police
        font = self._load_font(size=56)
        font_small = self._load_font(size=28)

        # Titre wrappé
        lines = textwrap.wrap(title, width=28)
        y = THUMB_H - 60 - len(lines) * 70
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            x = (THUMB_W - (bbox[2] - bbox[0])) // 2
            # Contour
            for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                draw.text((x + dx, y + dy), line, font=font, fill="black")
            draw.text((x, y), line, font=font, fill="white")
            y += 70

        # Badge YAWatch en haut à gauche
        draw.text((20, 20), "🧸 YAWatch Luna", font=font_small, fill="#B07FD4")

        bg.save(output, "JPEG", quality=88)
        logger.info("Thumbnail générée: %s", output.name)
        return output

    def _generate_placeholder(self, title: str, episode_id: str, output: Path) -> Path:
        """Crée une image de placeholder noir avec le titre."""
        try:
            from PIL import Image, ImageDraw, ImageFont
            img = Image.new("RGB", (THUMB_W, THUMB_H), color=(10, 10, 20))
            draw = ImageDraw.Draw(img)
            font = self._load_font(size=52)
            lines = textwrap.wrap(title, width=30)
            y = THUMB_H // 2 - len(lines) * 35
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                x = (THUMB_W - (bbox[2] - bbox[0])) // 2
                draw.text((x, y), line, font=font, fill="#B07FD4")
                y += 70
            draw.text((20, 20), "YAWatch Luna — prototype", font=self._load_font(24), fill="#555555")
            img.save(output, "JPEG", quality=85)
        except Exception as e:
            logger.warning("Placeholder thumbnail impossible: %s", e)
            output.write_text(f"# THUMBNAIL PLACEHOLDER\n# title: {title}\n# id: {episode_id}\n")
        logger.info("Thumbnail placeholder: %s", output.name)
        return output

    def _load_font(self, size: int = 48):
        from PIL import ImageFont
        candidates = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
        for path in candidates:
            if Path(path).exists():
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    pass
        return ImageFont.load_default()
