"""Génération de voix — supporte OpenAI TTS si la clé est disponible."""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class VoiceGenerator:
    """TTS avec OpenAI si clé présente, sinon placeholder."""

    LUNA_VOICE = "nova"       # voix OpenAI : douce, mystérieuse
    YAWATCH_VOICE = "onyx"    # voix OpenAI : froide, grave

    def __init__(self, openai_key: Optional[str] = None):
        self._key = openai_key
        self._client = None
        if openai_key:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=openai_key)
                logger.info("OpenAI TTS disponible")
            except ImportError:
                logger.warning("openai non installé — mode placeholder activé")

    def text_to_speech(
        self,
        text: str,
        output_path: Path,
        voice: str = LUNA_VOICE,
        speed: float = 0.95,
    ) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if self._client:
            return self._openai_tts(text, output_path, voice, speed)
        return self._placeholder(text, output_path, voice)

    def _openai_tts(self, text: str, output_path: Path, voice: str, speed: float) -> Path:
        try:
            response = self._client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                speed=speed,
            )
            response.stream_to_file(output_path)
            logger.info("Audio généré: %s", output_path.name)
            return output_path
        except Exception as e:
            logger.error("Erreur TTS OpenAI: %s — fallback placeholder", e)
            return self._placeholder(text, output_path, voice)

    def _placeholder(self, text: str, output_path: Path, voice: str) -> Path:
        output_path.write_text(
            f"# PLACEHOLDER AUDIO\n# voice: {voice}\n# text: {text[:200]}\n",
            encoding="utf-8",
        )
        logger.debug("Placeholder audio créé: %s", output_path.name)
        return output_path
