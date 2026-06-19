"""Rôle : Video QA Engineer.

Responsabilité : validation technique stricte du fichier MP4 final.
C'est le seul rôle qui peut déclarer un fichier techniquement conforme.
"""

import json
import subprocess
from pathlib import Path
from typing import Optional

from app.roles.base_role import BaseRole, VerdictResult

REQUIRED_WIDTH = 1080
REQUIRED_HEIGHT = 1920
REQUIRED_FPS = 25.0
FPS_TOLERANCE = 0.5
REQUIRED_VIDEO_CODEC = "h264"
REQUIRED_AUDIO_CODEC = "aac"
REQUIRED_PIX_FMT = "yuv420p"
MIN_FILE_SIZE_KB = 100
MIN_DURATION_S = 5.0
MAX_DURATION_S = 180.0


class VideoQAEngineer(BaseRole):
    role_name = "VideoQAEngineer"
    knowledge_doc = "QUALITY_GATE_ENGINE.md"
    verdict_name = "verdict_technique"

    def validate(self, context: dict) -> VerdictResult:
        """
        context attendu :
          - "video_path" : str|Path — fichier MP4 à valider (obligatoire)
          - "expected_duration" : float — durée attendue en secondes (optionnel)
        """
        errors: list[str] = []
        warnings: list[str] = []

        video_path: Optional[str] = str(context.get("video_path", "")) or None

        if not video_path:
            return VerdictResult(
                self.verdict_name, "FAIL",
                ["video_path manquant dans le contexte QA."], []
            )

        p = Path(video_path)
        if not p.exists():
            return VerdictResult(
                self.verdict_name, "FAIL",
                [f"Fichier introuvable : {video_path}"], []
            )

        # Taille minimale
        size_kb = p.stat().st_size / 1024
        if size_kb < MIN_FILE_SIZE_KB:
            errors.append(
                f"Fichier trop petit : {size_kb:.0f} KB "
                f"(minimum {MIN_FILE_SIZE_KB} KB). Probablement vide ou corrompu."
            )
            return VerdictResult(self.verdict_name, "FAIL", errors, warnings)

        # Inspection FFprobe
        probe = _ffprobe(video_path)
        if probe is None:
            return VerdictResult(
                self.verdict_name, "FAIL",
                [f"FFprobe ne peut pas lire le fichier : {p.name}"], []
            )

        streams_by_type: dict = {}
        for s in probe.get("streams", []):
            t = s.get("codec_type")
            if t and t not in streams_by_type:
                streams_by_type[t] = s

        # Vérifications vidéo
        v = streams_by_type.get("video")
        if not v:
            errors.append("Aucun flux vidéo détecté.")
        else:
            w = v.get("width", 0)
            h = v.get("height", 0)
            if w != REQUIRED_WIDTH or h != REQUIRED_HEIGHT:
                errors.append(
                    f"Résolution : {w}×{h} (requis {REQUIRED_WIDTH}×{REQUIRED_HEIGHT}). "
                    "Format 9:16 obligatoire pour YouTube Shorts."
                )

            codec = v.get("codec_name", "")
            if codec != REQUIRED_VIDEO_CODEC:
                errors.append(
                    f"Codec vidéo : {codec} (requis {REQUIRED_VIDEO_CODEC}). "
                    "Utiliser -c:v libx264."
                )

            pix_fmt = v.get("pix_fmt", "")
            if pix_fmt != REQUIRED_PIX_FMT:
                errors.append(
                    f"Pixel format : {pix_fmt} (requis {REQUIRED_PIX_FMT}). "
                    "Ajouter -pix_fmt yuv420p à la commande FFmpeg."
                )

            fps_str = v.get("r_frame_rate", "0/1")
            fps = _parse_fps(fps_str)
            if fps is not None and abs(fps - REQUIRED_FPS) > FPS_TOLERANCE:
                errors.append(
                    f"FPS : {fps:.2f} (requis {REQUIRED_FPS}±{FPS_TOLERANCE}). "
                    "Ajouter -r 25 à la commande FFmpeg."
                )

        # Vérifications audio
        a = streams_by_type.get("audio")
        if not a:
            errors.append(
                "Aucun flux audio détecté. "
                "Un Short sans son est inutilisable."
            )
        else:
            acodec = a.get("codec_name", "")
            if acodec != REQUIRED_AUDIO_CODEC:
                warnings.append(
                    f"Codec audio : {acodec} (recommandé {REQUIRED_AUDIO_CODEC}). "
                    "Utiliser -c:a aac -b:a 128k."
                )

        # Durée
        fmt = probe.get("format", {})
        duration = float(fmt.get("duration", 0))
        if duration < MIN_DURATION_S:
            errors.append(
                f"Durée trop courte : {duration:.1f}s (minimum {MIN_DURATION_S}s)."
            )
        if duration > MAX_DURATION_S:
            warnings.append(
                f"Durée inhabituellement longue : {duration:.1f}s. "
                "Les Shorts YouTube sont limités à 60s recommandés."
            )

        expected = context.get("expected_duration")
        if expected and duration and abs(duration - expected) > 2.0:
            warnings.append(
                f"Durée réelle {duration:.1f}s vs attendue {expected:.1f}s "
                f"(écart {abs(duration - expected):.1f}s)."
            )

        if errors:
            return VerdictResult(self.verdict_name, "FAIL", errors, warnings)
        return VerdictResult(self.verdict_name, "PASS", [], warnings)


def _ffprobe(path: str) -> Optional[dict]:
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_streams", "-show_format", path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception:
        pass
    return None


def _parse_fps(fps_str: str) -> Optional[float]:
    try:
        parts = fps_str.split("/")
        if len(parts) == 2:
            num, den = int(parts[0]), int(parts[1])
            return num / den if den != 0 else None
        return float(fps_str)
    except (ValueError, ZeroDivisionError):
        return None
