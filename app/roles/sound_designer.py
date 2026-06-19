"""Rôle : Sound Designer.

Responsabilité : valider que l'audio existe, que les niveaux sont corrects,
que la voix narrateur est un fichier canon validé (pas une génération test).
"""

import subprocess
import json
from pathlib import Path
from typing import Optional

from app.roles.base_role import BaseRole, VerdictResult

# Niveaux de référence YAWatch-LUNA (voir FFMPEG_PROFESSIONAL_VIDEO_PIPELINE.md)
NARRATION_REF_DB = 0.0
MUSIC_TARGET_DB = -18.0
AMBIANCE_TARGET_DB = -24.0
MIN_AUDIO_BITRATE_KBPS = 96
TARGET_SAMPLE_RATE = 44100

CANON_NARRATION_MARKERS = frozenset({
    "canon_narrateur", "canon_luna", "canon_narration",
    "validated_", "_approved", "_canon",
})

TEST_NARRATION_MARKERS = frozenset({
    "test_", "draft_", "tmp_", "temp_", "essai_", "sample_",
    "placeholder", "tts_test",
})


class SoundDesigner(BaseRole):
    role_name = "SoundDesigner"
    knowledge_doc = "FFMPEG_PROFESSIONAL_VIDEO_PIPELINE.md"
    verdict_name = "verdict_son"

    def validate(self, context: dict) -> VerdictResult:
        """
        context attendu :
          - "audio_path" : str|Path — fichier audio principal (voix narrateur)
          - "music_path" : str|Path — motif musical (optionnel)
          - "assembled_path" : str|Path — MP4 assemblé (pour vérifier l'audio intégré)
          - "has_sfx" : bool — SFX présents dans le mix
          - "narration_validated" : bool — voix narrateur a été validée par Ludovic
        """
        errors: list[str] = []
        warnings: list[str] = []

        audio_path: Optional[str] = _str(context.get("audio_path"))
        music_path: Optional[str] = _str(context.get("music_path"))
        assembled_path: Optional[str] = _str(context.get("assembled_path"))
        narration_validated: bool = context.get("narration_validated", False)
        has_sfx: bool = context.get("has_sfx", False)

        # Règle 1 : audio principal obligatoire
        if not audio_path:
            errors.append(
                "Aucun fichier audio (voix narrateur) fourni. "
                "Un Short YAWatch-LUNA sans voix narrateur ne peut pas être assemblé."
            )
        elif not Path(audio_path).exists():
            errors.append(f"Fichier audio introuvable : {audio_path}")
        else:
            # Règle 2 : le fichier audio n'est pas un test/placeholder
            audio_name = Path(audio_path).stem.lower()
            for marker in TEST_NARRATION_MARKERS:
                if marker in audio_name:
                    errors.append(
                        f"Fichier audio suspect (nom de test détecté) : "
                        f"{Path(audio_path).name}. "
                        "Utiliser uniquement CANON_NARRATEUR validé par Ludovic."
                    )
                    break

            # Règle 3 : la voix narrateur doit avoir été validée
            if not narration_validated:
                warnings.append(
                    "narration_validated=False — la voix narrateur n'a pas été "
                    "explicitement validée par Ludovic. "
                    "Voir BIBLE_VOIX_ELEVENLABS_V1.md — protocole CANON_NARRATEUR."
                )

            # Règle 4 : format audio correct
            info = _get_audio_info(audio_path)
            if info:
                if info.get("codec_name") not in ("mp3", "aac", "wav", "flac", "pcm_s16le"):
                    warnings.append(
                        f"Codec audio : {info.get('codec_name')} — "
                        "préférer MP3 320kbps ou WAV 44100Hz 16bit."
                    )
                sr = int(info.get("sample_rate", 0))
                if sr and sr != TARGET_SAMPLE_RATE:
                    warnings.append(
                        f"Sample rate : {sr} Hz (attendu {TARGET_SAMPLE_RATE} Hz). "
                        "Risque de désynchronisation après export FFmpeg."
                    )

        # Règle 5 : musique absente = warning (pas erreur, acceptable pour prototype)
        if not music_path:
            warnings.append(
                "Aucun motif musical fourni. "
                "Le teaser final doit inclure le motif musical YAWatch-LUNA "
                "validé (voir SONIC_IDENTITY.md)."
            )
        elif not Path(music_path).exists():
            warnings.append(f"Fichier musique introuvable : {music_path}")

        # Règle 6 : vérifier l'audio dans le MP4 assemblé
        if assembled_path and Path(assembled_path).exists():
            has_audio = _check_mp4_has_audio(assembled_path)
            if not has_audio:
                errors.append(
                    f"Le MP4 assemblé n'a pas de piste audio : "
                    f"{Path(assembled_path).name}. "
                    "Un Short sans son est inutilisable."
                )

        # Règle 7 : SFX absent = warning pour teaser
        if not has_sfx:
            warnings.append(
                "Aucun SFX déclaré dans le mix. "
                "Le jeton noir (plan 9 teaser) requiert un SFX d'impact. "
                "Voir SONIC_IDENTITY.md — Bible SFX à créer."
            )

        if errors:
            return VerdictResult(self.verdict_name, "FAIL", errors, warnings)
        return VerdictResult(self.verdict_name, "PASS", [], warnings)


def _str(value) -> Optional[str]:
    return str(value) if value else None


def _get_audio_info(path: str) -> Optional[dict]:
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-select_streams", "a:0",
             "-show_entries", "stream=codec_name,sample_rate,bit_rate",
             "-print_format", "json", path],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            streams = data.get("streams", [])
            return streams[0] if streams else None
    except Exception:
        pass
    return None


def _check_mp4_has_audio(path: str) -> bool:
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-select_streams", "a",
             "-show_entries", "stream=codec_type",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0 and "audio" in result.stdout
    except Exception:
        return False
