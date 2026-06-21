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
import hashlib
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
# Moteurs I2V supportés par le backend gouverné
# ──────────────────────────────────────────────────────────────────────────
# Chaque moteur a un constructeur de workflow dédié (voir build_workflow).
# AnimateDiff = chemin prouvé sur plan02. FramePack / Wan2.1 = ajoutés pour la
# comparaison gouvernée (le backend les exécute ; il ne les choisit pas).
ENGINE_ANIMATEDIFF = "animatediff"
ENGINE_FRAMEPACK = "framepack"
ENGINE_WAN21 = "wan21"
SUPPORTED_ENGINES = (ENGINE_ANIMATEDIFF, ENGINE_FRAMEPACK, ENGINE_WAN21)


# ──────────────────────────────────────────────────────────────────────────
# Gouvernance : un job n'est exécutable que s'il vient d'un rôle métier
# ──────────────────────────────────────────────────────────────────────────
# Source autorisée d'un job. Le backend refuse tout job qui n'en provient pas.
GOVERNED_SOURCE = "MotionDirector"

# Paramètres que le rôle métier verrouille. Le job_hash les scelle : toute
# modification manuelle ultérieure casse le hash → le backend refuse le job.
# (Anti-« édition directe du JSON » — la régression qui avait déçu Ludovic.)
DEFAULT_LOCKED_PARAMETERS = (
    "engine", "engine_params", "checkpoint", "motion_model",
    "width", "height", "num_frames", "fps", "steps", "cfg", "denoise",
    "sampler", "scheduler",
    "use_ipadapter", "ipadapter_weight", "motion_scale",
    "prompt_positive", "prompt_negative",
)


class GovernanceError(RuntimeError):
    """Levée quand un job ne respecte pas la chaîne de gouvernance.

    Pas de fallback silencieux : un job non conforme est REFUSÉ, pas « réparé ».
    """


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

    # Moteur I2V (le rôle métier choisit ; le backend exécute la branche dédiée)
    engine: str = ENGINE_ANIMATEDIFF  # animatediff | framepack | wan21
    # Paramètres spécifiques au moteur (modèles, sampler, shift…) scellés dans
    # le job. Vide pour AnimateDiff (qui utilise les champs ci-dessous).
    engine_params: dict = field(default_factory=dict)

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

    # Identité personnage (IPAdapter) — préparé par le MotionDirector
    use_ipadapter: bool = False       # False = chemin prouvé plan02 (sans IPAdapter)
    ipadapter_weight: float = 0.0
    ipadapter_image: str = ""         # image de référence (= image source du perso)
    ipadapter_preset: str = "STANDARD (medium strength)"

    # Mouvement (métadonnée — appliquée si le nœud de scale est disponible)
    motion_scale: float = 1.0

    # Traçabilité gouvernance (d'où vient ce job)
    plan_id: str = ""
    plan_type: str = ""
    character: str = ""

    # Sceau de gouvernance (posé par le rôle métier, vérifié par le backend)
    source_generatrice: str = ""              # doit valoir GOVERNED_SOURCE
    locked_parameters: tuple = ()             # paramètres scellés par le hash
    job_hash: str = ""                        # SHA-256 des paramètres verrouillés

    # Finalisation (FFmpeg = assemblage, conforme Règle 0)
    finalize: bool = True             # upscale + normalise pour le Quality Gate
    final_width: int = 1080
    final_height: int = 1920
    final_fps: int = 25

    @staticmethod
    def from_json(path: Path) -> "VideoJob":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        # JSON ne connaît pas les tuples : on normalise locked_parameters.
        if "locked_parameters" in data and data["locked_parameters"] is not None:
            data["locked_parameters"] = tuple(data["locked_parameters"])
        return VideoJob(**data)


# ──────────────────────────────────────────────────────────────────────────
# Gouvernance — sceau et vérification (le backend est un exécutant discipliné)
# ──────────────────────────────────────────────────────────────────────────

def compute_job_hash(job: "VideoJob") -> str:
    """SHA-256 des paramètres verrouillés + source. Sceau anti-altération.

    Recalculable à l'identique par n'importe qui : si un paramètre verrouillé
    est modifié à la main après préparation, le hash ne correspond plus et
    validate_job_governance() refuse le job.
    """
    payload = {name: getattr(job, name) for name in job.locked_parameters}
    payload["_source"] = job.source_generatrice
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def validate_job_governance(job: "VideoJob") -> None:
    """Refuse tout job qui ne respecte pas la chaîne de gouvernance.

    Règles (aucun fallback silencieux — on lève GovernanceError) :
      1. le job vient du rôle métier (source_generatrice == GOVERNED_SOURCE) ;
      2. des paramètres sont verrouillés (locked_parameters non vide) ;
      3. un job_hash est présent ;
      4. le job_hash correspond aux paramètres verrouillés actuels ;
      5. le moteur demandé est supporté.
    """
    if job.source_generatrice != GOVERNED_SOURCE:
        raise GovernanceError(
            f"Job refusé : source_generatrice='{job.source_generatrice}' "
            f"(attendu '{GOVERNED_SOURCE}'). Un job doit être préparé par le "
            "rôle métier, jamais écrit à la main."
        )
    if not job.locked_parameters:
        raise GovernanceError(
            "Job refusé : aucun paramètre verrouillé. Le rôle métier doit "
            "sceller les paramètres (locked_parameters)."
        )
    if not job.job_hash:
        raise GovernanceError("Job refusé : job_hash absent.")
    expected = compute_job_hash(job)
    if expected != job.job_hash:
        raise GovernanceError(
            "Job refusé : job_hash invalide — des paramètres verrouillés ont "
            "été altérés après préparation (édition manuelle interdite).\n"
            f"  attendu={expected}\n  reçu   ={job.job_hash}"
        )
    if job.engine not in SUPPORTED_ENGINES:
        raise GovernanceError(
            f"Job refusé : moteur '{job.engine}' inconnu. "
            f"Moteurs supportés : {SUPPORTED_ENGINES}."
        )


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
    """Dispatcher : construit le graphe ComfyUI selon le moteur du job.

    Le backend exécute la branche du moteur demandé — il n'en choisit aucun.
    AnimateDiff = chemin prouvé sur plan02. FramePack / Wan2.1 = branches pour
    la comparaison gouvernée (graphes calqués sur les workflows réellement
    validés, pas inventés).
    """
    builder = _ENGINE_BUILDERS.get(job.engine)
    if builder is None:
        raise ValueError(
            f"Moteur '{job.engine}' sans constructeur de workflow. "
            f"Moteurs supportés : {tuple(_ENGINE_BUILDERS)}."
        )
    return builder(job, image_name)


def _build_animatediff_workflow(job: VideoJob, image_name: str) -> dict:
    """Construit le graphe img2vid : image → latent répété → AnimateDiff → MP4.

    Approche prudente : faible denoise pour préserver l'identité du visage
    (critère n°1 de la matrice de décision YAWatch-LUNA).

    Si job.use_ipadapter est True, l'identité du personnage est renforcée par
    IPAdapter (image de référence injectée dans le MODEL avant AnimateDiff).
    Si False, le graphe est strictement celui prouvé sur plan02.
    """
    graph = {
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
        # Source du MODEL pour AnimateDiff — remplacé par IPAdapter si activé
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

    if job.use_ipadapter:
        # IPAdapter : injecte l'identité du personnage dans le MODEL avant AnimateDiff.
        # Chaîne : checkpoint MODEL → UnifiedLoader → IPAdapter(ref image) → AnimateDiff
        graph["12"] = {"class_type": "IPAdapterUnifiedLoader",
                       "inputs": {"model": ["1", 0], "preset": job.ipadapter_preset}}
        graph["13"] = {"class_type": "IPAdapter",
                       "inputs": {"model": ["12", 0], "ipadapter": ["12", 1],
                                  "image": ["2", 0], "weight": job.ipadapter_weight,
                                  "weight_type": "standard",
                                  "start_at": 0.0, "end_at": 1.0}}
        # AnimateDiff prend désormais le MODEL enrichi par l'IPAdapter
        graph["8"]["inputs"]["model"] = ["13", 0]

    return graph


# Défauts FramePack — calqués sur le workflow PROUVÉ qui passe le Quality Gate
# (framepack_plan02_luna_api_test_001.json, SSIM 0.925 / flicker 0.16, 20 juin).
# Le rôle métier copie ces valeurs dans job.engine_params (scellées par le hash).
FRAMEPACK_DEFAULTS = {
    "framepack_model": "FramePackI2V_HY_fp8_e4m3fn.safetensors",
    "base_precision": "bf16",
    "quantization": "fp8_e4m3fn",
    "attention_mode": "sdpa",
    "vae_name": "hunyuan_video_vae_bf16.safetensors",
    "sigclip_name": "sigclip_vision_patch14_384.safetensors",
    "clip_name1": "clip_l.safetensors",
    "clip_name2": "llava_llama3_fp16.safetensors",
    "base_resolution": 640,
    "steps": 20,
    "cfg": 1.0,
    "guidance_scale": 10.0,
    "shift": 0.0,
    "latent_window_size": 9,
    "total_second_length": 5.0,
    "gpu_memory_preservation": 6.0,
    "sampler": "unipc_bh1",
    "use_teacache": True,
    "teacache_rel_l1_thresh": 0.15,
    "frame_rate": 16.0,
}

# Défauts Wan2.1 I2V 14B — version NATIVE (UNETLoader fp8_e4m3fn scaled), pas GGUF.
# Calqué sur le graphe GGUF prouvé (wan21_gguf_..._success_001.json) mais le
# chargeur GGUF est remplacé par le chargeur natif (VRAM 32 GB le permet) :
# c'est la comparaison équitable que le GGUF quantifié (SSIM 0.50) ne permettait pas.
WAN21_DEFAULTS = {
    "unet_name": "wan2.1_i2v_480p_14B_fp8_e4m3fn.safetensors",
    "weight_dtype": "default",
    "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
    "clip_vision_name": "clip_vision_h.safetensors",
    "vae_name": "wan_2.1_vae.safetensors",
    "width": 480,
    "height": 832,
    "length": 41,
    "shift": 8.0,
    "steps": 12,
    "cfg": 1.0,
    "sampler_name": "uni_pc",
    "scheduler": "simple",
    "denoise": 1.0,
    "frame_rate": 8.0,
}


def _build_framepack_workflow(job: VideoJob, image_name: str) -> dict:
    """Graphe FramePack (HunyuanVideo) — calqué sur le workflow PROUVÉ (PASS).

    Reproduit fidèlement framepack_plan02_luna_api_test_001.json. Les valeurs
    proviennent de job.engine_params (scellées par le hash de gouvernance) ;
    FRAMEPACK_DEFAULTS sert de filet si une clé manque. Les prompts viennent du
    job (préparés par le rôle métier). Tout écart de graphe est rattrapé par
    ComfyUI au submit (node_errors) — jamais un fallback silencieux.
    """
    p = {**FRAMEPACK_DEFAULTS, **(job.engine_params or {})}
    return {
        "1": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "2": {"class_type": "FramePackFindNearestBucket",
              "inputs": {"image": ["1", 0], "base_resolution": p["base_resolution"]}},
        "3": {"class_type": "ImageScale",
              "inputs": {"image": ["1", 0], "upscale_method": "lanczos",
                         "width": ["2", 0], "height": ["2", 1], "crop": "center"}},
        "4": {"class_type": "VAELoader", "inputs": {"vae_name": p["vae_name"]}},
        "5": {"class_type": "VAEEncode", "inputs": {"pixels": ["3", 0], "vae": ["4", 0]}},
        "6": {"class_type": "CLIPVisionLoader", "inputs": {"clip_name": p["sigclip_name"]}},
        "7": {"class_type": "CLIPVisionEncode",
              "inputs": {"clip_vision": ["6", 0], "image": ["3", 0], "crop": "center"}},
        "8": {"class_type": "DualCLIPLoader",
              "inputs": {"clip_name1": p["clip_name1"], "clip_name2": p["clip_name2"],
                         "type": "hunyuan_video"}},
        "9": {"class_type": "CLIPTextEncode",
              "inputs": {"clip": ["8", 0], "text": job.prompt_positive}},
        "10": {"class_type": "CLIPTextEncode",
               "inputs": {"clip": ["8", 0], "text": job.prompt_negative}},
        "11": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["10", 0]}},
        "12": {"class_type": "LoadFramePackModel",
               "inputs": {"model": p["framepack_model"], "base_precision": p["base_precision"],
                          "quantization": p["quantization"], "load_device": "offload_device",
                          "attention_mode": p["attention_mode"]}},
        "13": {"class_type": "FramePackSampler",
               "inputs": {"model": ["12", 0], "positive": ["9", 0], "negative": ["11", 0],
                          "start_latent": ["5", 0], "steps": p["steps"],
                          "use_teacache": p["use_teacache"],
                          "teacache_rel_l1_thresh": p["teacache_rel_l1_thresh"],
                          "cfg": p["cfg"], "guidance_scale": p["guidance_scale"],
                          "shift": p["shift"], "seed": job.seed,
                          "latent_window_size": p["latent_window_size"],
                          "total_second_length": p["total_second_length"],
                          "gpu_memory_preservation": p["gpu_memory_preservation"],
                          "sampler": p["sampler"], "image_embeds": ["7", 0]}},
        "14": {"class_type": "VAEDecodeTiled",
               "inputs": {"samples": ["13", 0], "vae": ["4", 0], "tile_size": 256,
                          "overlap": 64, "temporal_size": 64, "temporal_overlap": 8}},
        "15": {"class_type": "VHS_VideoCombine",
               "inputs": {"images": ["14", 0], "frame_rate": p["frame_rate"], "loop_count": 0,
                          "filename_prefix": "YAWATCH_RAW", "format": "video/h264-mp4",
                          "pingpong": False, "save_output": True}},
    }


def _build_wan21_workflow(job: VideoJob, image_name: str) -> dict:
    """Graphe Wan2.1 I2V 14B NATIF (fp16) — calqué sur le graphe GGUF prouvé.

    Identique au workflow Wan testé le 20 juin, SAUF le chargeur : UnetLoaderGGUF
    (Q5 quantifié, SSIM 0.50) est remplacé par UNETLoader natif fp16. C'est la
    comparaison équitable rendue possible par la VRAM 32 GB du nouveau GPU.
    Valeurs scellées via job.engine_params ; WAN21_DEFAULTS en filet.
    """
    p = {**WAN21_DEFAULTS, **(job.engine_params or {})}
    return {
        "1": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "2": {"class_type": "CLIPLoader",
              "inputs": {"clip_name": p["clip_name"], "type": "wan"}},
        "3": {"class_type": "CLIPTextEncode",
              "inputs": {"clip": ["2", 0], "text": job.prompt_positive}},
        "4": {"class_type": "CLIPTextEncode",
              "inputs": {"clip": ["2", 0], "text": job.prompt_negative}},
        "5": {"class_type": "CLIPVisionLoader",
              "inputs": {"clip_name": p["clip_vision_name"]}},
        "6": {"class_type": "CLIPVisionEncode",
              "inputs": {"clip_vision": ["5", 0], "image": ["1", 0], "crop": "center"}},
        "7": {"class_type": "VAELoader", "inputs": {"vae_name": p["vae_name"]}},
        "8": {"class_type": "WanImageToVideo",
              "inputs": {"positive": ["3", 0], "negative": ["4", 0], "vae": ["7", 0],
                         "width": p["width"], "height": p["height"], "length": p["length"],
                         "batch_size": 1, "start_image": ["1", 0],
                         "clip_vision_output": ["6", 0]}},
        # Chargeur NATIF (vs UnetLoaderGGUF du test GGUF) — clé du re-test équitable
        "9": {"class_type": "UNETLoader",
              "inputs": {"unet_name": p["unet_name"], "weight_dtype": p["weight_dtype"]}},
        "10": {"class_type": "ModelSamplingSD3",
               "inputs": {"model": ["9", 0], "shift": p["shift"]}},
        "11": {"class_type": "KSampler",
               "inputs": {"model": ["10", 0], "seed": job.seed, "steps": p["steps"],
                          "cfg": p["cfg"], "sampler_name": p["sampler_name"],
                          "scheduler": p["scheduler"], "positive": ["8", 0],
                          "negative": ["8", 1], "latent_image": ["8", 2],
                          "denoise": p["denoise"]}},
        "12": {"class_type": "VAEDecodeTiled",
               "inputs": {"samples": ["11", 0], "vae": ["7", 0], "tile_size": 256,
                          "overlap": 64, "temporal_size": 16, "temporal_overlap": 4}},
        "13": {"class_type": "VHS_VideoCombine",
               "inputs": {"images": ["12", 0], "frame_rate": p["frame_rate"], "loop_count": 0,
                          "filename_prefix": "YAWATCH_RAW", "format": "video/h264-mp4",
                          "pingpong": False, "save_output": True}},
    }


# Registre des constructeurs de workflow par moteur (dispatcher build_workflow).
_ENGINE_BUILDERS = {
    ENGINE_ANIMATEDIFF: _build_animatediff_workflow,
    ENGINE_FRAMEPACK: _build_framepack_workflow,
    ENGINE_WAN21: _build_wan21_workflow,
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
    """Exécute un job de bout en bout. Retourne le chemin du MP4 déposé.

    Gouvernance d'abord : un job non préparé par le rôle métier (ou altéré
    après préparation) est REFUSÉ avant toute génération.
    """
    validate_job_governance(job)
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
