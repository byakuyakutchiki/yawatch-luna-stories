"""Backend de génération image-to-video via ComfyUI — YAWatch Video Factory.

────────────────────────────────────────────────────────────────────────────
GOUVERNANCE (principe de Ludovic)
────────────────────────────────────────────────────────────────────────────
Ce backend est un EXÉCUTANT, pas un décideur.

Il reçoit un "job" déjà préparé en amont (image + prompt + paramètres) et
pilote ComfyUI pour produire un MP4. Il ne choisit JAMAIS le prompt, ne valide
JAMAIS la qualité, ne change JAMAIS de statut.

Le flux de gouvernance complet (qui ne doit jamais être contourné) est :

    bibliothèques de connaissances
        → rôle métier IA (prépare le job)
            → CE BACKEND (génère le MP4)
                → Quality Gate (VM Linux)
                    → validation humaine (Ludovic)

La future application bureau YAWatch Video Factory appellera ce backend comme
couche d'exécution. L'interface ne sera qu'une façade au-dessus de l'usine ;
elle prépare un VideoJob via les rôles métier, puis délègue ici.

────────────────────────────────────────────────────────────────────────────
DESIGN (corrige les bugs de la 1re tentative)
────────────────────────────────────────────────────────────────────────────
- AUCUN readline() bloquant. Les flux ComfyUI vont dans un fichier log.
- Attente readiness via l'API HTTP /object_info (pas via les logs).
- Soumission workflow via /prompt, avec capture des node_errors si rejet.
- Suivi via /history/{prompt_id}, avec détection si le serveur meurt.
- Récupération du MP4 depuis l'historique (pas par glob aveugle).
- Fonctions séparées, paramètres clairs, chemins configurables.

Usage :
    python comfyui_backend.py --job jobs/plan02_luna_adulte.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


# ──────────────────────────────────────────────────────────────────────────
# Description d'un job de génération (ce que le rôle métier prépare en amont)
# ──────────────────────────────────────────────────────────────────────────

@dataclass
class VideoJob:
    """Tout ce qu'il faut pour générer un clip. Préparé par le rôle métier IA."""

    # Identité de sortie
    output_name: str                  # ex : "plan02_luna_adulte_portrait.mp4"
    deposit_dir: str                  # dossier de dépôt final (clips_yawatch)

    # Entrée
    image_path: str                   # image source (déjà canonique)
    prompt_positive: str
    prompt_negative: str

    # Modèles
    checkpoint: str = "DreamShaper_8_pruned.safetensors"
    motion_model: str = "mm_sd_v15_v2.ckpt"
    beta_schedule: str = "sqrt_linear (AnimateDiff)"

    # Paramètres vidéo
    width: int = 512                  # conservateur pour 8 GB VRAM
    height: int = 912                 # ratio ~9:16
    num_frames: int = 16              # fenêtre AnimateDiff standard
    fps: float = 8.0
    steps: int = 12
    cfg: float = 4.5
    denoise: float = 0.45             # faible = préserve le visage source
    sampler: str = "euler"
    scheduler: str = "normal"
    seed: int = 2406202601

    # Finalisation (FFmpeg = assemblage, conforme Règle 0)
    finalize: bool = True             # upscale + normalise pour le Quality Gate
    final_width: int = 1080
    final_height: int = 1920
    final_fps: int = 25

    @staticmethod
    def from_json(path: Path) -> "VideoJob":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return VideoJob(**data)


# ──────────────────────────────────────────────────────────────────────────
# Configuration d'environnement (chemins ComfyUI — configurables)
# ──────────────────────────────────────────────────────────────────────────

@dataclass
class ComfyEnv:
    comfy_root: str
    python_exe: str
    host: str = "127.0.0.1"
    port: int = 8188
    ffmpeg_exe: str = "ffmpeg"
    log_path: Optional[str] = None

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


# ──────────────────────────────────────────────────────────────────────────
# Serveur ComfyUI — démarrage propre, logs en fichier (jamais en pipe)
# ──────────────────────────────────────────────────────────────────────────

class ComfyUIServer:
    """Gère le cycle de vie d'un process ComfyUI sans readline() bloquant."""

    def __init__(self, env: ComfyEnv):
        self.env = env
        self._proc: Optional[subprocess.Popen] = None
        self._log_handle = None

    def start(self) -> None:
        root = Path(self.env.comfy_root)
        log_path = Path(self.env.log_path) if self.env.log_path else root / "yawatch_comfy_run.log"
        # CLEF DU FIX : stdout/stderr vers un fichier, jamais subprocess.PIPE.
        self._log_handle = open(log_path, "w", encoding="utf-8", errors="replace")
        self._proc = subprocess.Popen(
            [self.env.python_exe, "main.py",
             "--listen", self.env.host, "--port", str(self.env.port)],
            cwd=str(root),
            stdout=self._log_handle,
            stderr=subprocess.STDOUT,
        )
        print(f"[server] ComfyUI lancé (pid={self._proc.pid}), log → {log_path}")

    def wait_ready(self, timeout: float = 240.0) -> bool:
        """Attend que l'API réponde. Polling HTTP, pas de lecture de logs."""
        deadline = time.time() + timeout
        url = f"{self.env.base_url}/object_info"
        while time.time() < deadline:
            if self._proc and self._proc.poll() is not None:
                print(f"[server] ComfyUI s'est arrêté avant d'être prêt "
                      f"(code={self._proc.returncode}). Voir le log.")
                return False
            try:
                with urllib.request.urlopen(url, timeout=3) as r:
                    if r.status == 200:
                        print("[server] API prête.")
                        return True
            except (urllib.error.URLError, ConnectionError, OSError):
                time.sleep(2)
        print("[server] Timeout : API non prête.")
        return False

    def is_alive(self) -> bool:
        return self._proc is not None and self._proc.poll() is None

    def stop(self) -> None:
        if self._proc is not None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=20)
            except subprocess.TimeoutExpired:
                self._proc.kill()
            print("[server] ComfyUI arrêté proprement.")
        if self._log_handle:
            self._log_handle.close()


# ──────────────────────────────────────────────────────────────────────────
# Construction du workflow (graphe ComfyUI)
# ──────────────────────────────────────────────────────────────────────────

def build_workflow(job: VideoJob, image_name: str) -> dict:
    """Construit le graphe img2vid : image → latent répété → AnimateDiff → MP4.

    Approche prudente : faible denoise pour préserver l'identité du visage
    (critère n°1 de la matrice de décision YAWatch-LUNA).
    """
    return {
        "1": {"class_type": "CheckpointLoaderSimple",
              "inputs": {"ckpt_name": job.checkpoint}},
        "2": {"class_type": "LoadImage",
              "inputs": {"image": image_name}},
        "3": {"class_type": "ImageScale",
              "inputs": {"image": ["2", 0], "upscale_method": "lanczos",
                         "width": job.width, "height": job.height, "crop": "center"}},
        "4": {"class_type": "VAEEncode",
              "inputs": {"pixels": ["3", 0], "vae": ["1", 2]}},
        "5": {"class_type": "RepeatLatentBatch",
              "inputs": {"samples": ["4", 0], "amount": job.num_frames}},
        "6": {"class_type": "CLIPTextEncode",
              "inputs": {"clip": ["1", 1], "text": job.prompt_positive}},
        "7": {"class_type": "CLIPTextEncode",
              "inputs": {"clip": ["1", 1], "text": job.prompt_negative}},
        "8": {"class_type": "ADE_AnimateDiffLoaderGen1",
              "inputs": {"model": ["1", 0], "model_name": job.motion_model,
                         "beta_schedule": job.beta_schedule}},
        "9": {"class_type": "KSampler",
              "inputs": {"model": ["8", 0], "seed": job.seed, "steps": job.steps,
                         "cfg": job.cfg, "sampler_name": job.sampler,
                         "scheduler": job.scheduler, "positive": ["6", 0],
                         "negative": ["7", 0], "latent_image": ["5", 0],
                         "denoise": job.denoise}},
        "10": {"class_type": "VAEDecode",
               "inputs": {"samples": ["9", 0], "vae": ["1", 2]}},
        "11": {"class_type": "VHS_VideoCombine",
               "inputs": {"images": ["10", 0], "frame_rate": job.fps,
                          "loop_count": 0, "filename_prefix": "YAWATCH_RAW",
                          "format": "video/h264-mp4", "pingpong": False,
                          "save_output": True}},
    }


# ──────────────────────────────────────────────────────────────────────────
# Dialogue avec l'API ComfyUI
# ──────────────────────────────────────────────────────────────────────────

def submit_workflow(env: ComfyEnv, workflow: dict) -> str:
    """Soumet le workflow. Capture les node_errors si ComfyUI rejette le graphe."""
    body = json.dumps({"prompt": workflow, "client_id": str(uuid.uuid4())}).encode()
    req = urllib.request.Request(
        f"{env.base_url}/prompt", data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ComfyUI a rejeté le workflow (HTTP {e.code}) : {detail}")
    prompt_id = resp.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"Pas de prompt_id dans la réponse : {resp}")
    print(f"[api] Workflow soumis. prompt_id={prompt_id}")
    return prompt_id


def wait_for_result(env: ComfyEnv, server: ComfyUIServer, prompt_id: str,
                    timeout: float = 1800.0) -> dict:
    """Suit /history/{prompt_id}. Détecte si le serveur meurt en cours de route."""
    deadline = time.time() + timeout
    url = f"{env.base_url}/history/{prompt_id}"
    while time.time() < deadline:
        if not server.is_alive():
            raise RuntimeError("ComfyUI s'est arrêté pendant la génération. Voir le log.")
        try:
            with urllib.request.urlopen(url, timeout=5) as r:
                history = json.load(r)
            if prompt_id in history:
                print("[api] Génération terminée.")
                return history[prompt_id]
        except (urllib.error.URLError, ConnectionError, OSError):
            pass
        time.sleep(5)
    raise RuntimeError("Timeout : la génération n'a pas abouti dans le délai imparti.")


def extract_video_path(env: ComfyEnv, history_entry: dict) -> Path:
    """Récupère le chemin du MP4 depuis l'historique (pas par glob aveugle)."""
    outputs = history_entry.get("outputs", {})
    for node_output in outputs.values():
        for key in ("gifs", "videos", "images"):
            for item in node_output.get(key, []):
                filename = item.get("filename", "")
                if filename.lower().endswith((".mp4", ".webm")):
                    subfolder = item.get("subfolder", "")
                    out_dir = Path(env.comfy_root) / "output" / subfolder
                    candidate = out_dir / filename
                    if candidate.exists():
                        return candidate
    raise RuntimeError(f"Aucun MP4 trouvé dans l'historique : {outputs}")


# ──────────────────────────────────────────────────────────────────────────
# Finalisation FFmpeg (assemblage — conforme Règle 0)
# ──────────────────────────────────────────────────────────────────────────

def finalize_clip(env: ComfyEnv, job: VideoJob, raw_mp4: Path, final_path: Path) -> Path:
    """Upscale + normalise le clip brut pour qu'il soit conforme au Quality Gate.

    FFmpeg fait de l'ASSEMBLAGE ici (scale, fps, codec) — jamais de génération
    de mouvement. Le mouvement vient d'AnimateDiff, en amont.
    """
    vf = (f"scale={job.final_width}:{job.final_height}:"
          f"force_original_aspect_ratio=decrease,"
          f"pad={job.final_width}:{job.final_height}:(ow-iw)/2:(oh-ih)/2,"
          f"fps={job.final_fps},format=yuv420p")
    cmd = [env.ffmpeg_exe, "-y", "-i", str(raw_mp4),
           "-vf", vf, "-c:v", "libx264", "-profile:v", "baseline",
           "-level", "3.1", "-crf", "22", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", "-an", str(final_path)]
    print(f"[ffmpeg] Finalisation → {job.final_width}x{job.final_height} "
          f"@ {job.final_fps}fps")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg a échoué : {result.stderr[-800:]}")
    return final_path


# ──────────────────────────────────────────────────────────────────────────
# Orchestration d'un job complet
# ──────────────────────────────────────────────────────────────────────────

def stage_input_image(env: ComfyEnv, job: VideoJob) -> str:
    """Copie l'image source dans le dossier input de ComfyUI. Retourne le nom."""
    import shutil
    src = Path(job.image_path)
    if not src.exists():
        raise FileNotFoundError(f"Image source introuvable : {src}")
    input_dir = Path(env.comfy_root) / "input"
    input_dir.mkdir(parents=True, exist_ok=True)
    image_name = f"yawatch_{Path(job.output_name).stem}_input{src.suffix}"
    shutil.copy2(src, input_dir / image_name)
    print(f"[input] Image préparée : {image_name}")
    return image_name


def run_job(env: ComfyEnv, job: VideoJob) -> Path:
    """Exécute un job de bout en bout. Retourne le chemin du MP4 déposé."""
    server = ComfyUIServer(env)
    try:
        server.start()
        if not server.wait_ready():
            raise RuntimeError("ComfyUI non prêt — abandon.")

        image_name = stage_input_image(env, job)
        workflow = build_workflow(job, image_name)
        prompt_id = submit_workflow(env, workflow)
        history_entry = wait_for_result(env, server, prompt_id)
        raw_mp4 = extract_video_path(env, history_entry)
        print(f"[output] Clip brut : {raw_mp4} ({raw_mp4.stat().st_size // 1024} KB)")

        deposit_dir = Path(job.deposit_dir)
        deposit_dir.mkdir(parents=True, exist_ok=True)
        final_path = deposit_dir / job.output_name

        if job.finalize:
            finalize_clip(env, job, raw_mp4, final_path)
        else:
            import shutil
            shutil.copy2(raw_mp4, final_path)

        print(f"[done] MP4 déposé : {final_path} "
              f"({final_path.stat().st_size // 1024} KB)")
        return final_path
    finally:
        server.stop()


# ──────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="YAWatch Video Factory — backend de génération ComfyUI")
    parser.add_argument("--job", required=True, help="Fichier JSON décrivant le VideoJob")
    parser.add_argument("--comfy-root", default=r"C:\Users\saint\Documents\Codex\ComfyUI")
    parser.add_argument("--python-exe",
                        default=r"C:\Users\saint\Documents\Codex\ComfyUI\.venv\Scripts\python.exe")
    parser.add_argument("--ffmpeg-exe", default=r"C:\ffmpeg\ffmpeg.exe")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8188)
    args = parser.parse_args()

    env = ComfyEnv(
        comfy_root=args.comfy_root,
        python_exe=args.python_exe,
        ffmpeg_exe=args.ffmpeg_exe,
        host=args.host,
        port=args.port,
    )
    job = VideoJob.from_json(Path(args.job))

    print("=" * 70)
    print("YAWATCH VIDEO FACTORY — génération locale (objectif B)")
    print(f"Job     : {job.output_name}")
    print(f"Image   : {job.image_path}")
    print(f"Modèle  : {job.checkpoint} + {job.motion_model}")
    print(f"Sortie  : {job.width}x{job.height} → "
          f"{job.final_width}x{job.final_height} (finalize={job.finalize})")
    print("=" * 70)

    try:
        run_job(env, job)
        print("\n✅ SUCCÈS — MP4 local produit.")
        return 0
    except Exception as exc:
        print(f"\n❌ ÉCHEC : {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
