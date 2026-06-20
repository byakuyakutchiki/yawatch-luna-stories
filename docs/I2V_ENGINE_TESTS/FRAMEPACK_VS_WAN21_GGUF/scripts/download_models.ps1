param(
    [ValidateSet("framepack", "wan", "all")]
    [string]$Engine = "all",
    [string]$ComfyRoot = "C:\Users\saint\Documents\Codex\ComfyUI",
    [ValidateSet("Q5_K_S", "Q4_K_S")]
    [string]$WanQuant = "Q5_K_S"
)

$ErrorActionPreference = "Stop"
$python = Join-Path $ComfyRoot ".venv\Scripts\python.exe"
$hfCli = Join-Path $ComfyRoot ".venv\Scripts\hf.exe"

if (!(Test-Path -LiteralPath $python)) {
    throw "Python ComfyUI introuvable: $python"
}
if (!(Test-Path -LiteralPath $hfCli)) {
    throw "hf.exe introuvable: $hfCli"
}

function Ensure-Dir {
    param([string]$Path)
    New-Item -ItemType Directory -Force -Path $Path | Out-Null
}

function HF-Download {
    param(
        [string]$Repo,
        [string[]]$Include,
        [string]$LocalDir
    )

    Ensure-Dir $LocalDir
    $args = @("download", $Repo, "--local-dir", $LocalDir)
    foreach ($pattern in $Include) {
        $args += @("--include", $pattern)
    }
    Write-Host "[hf] $Repo -> $LocalDir"
    & $hfCli @args
    if ($LASTEXITCODE -ne 0) {
        throw "Echec telechargement Hugging Face: $Repo"
    }
}

if ($Engine -eq "framepack" -or $Engine -eq "all") {
    HF-Download -Repo "Kijai/HunyuanVideo_comfy" -Include @(
        "FramePackI2V_HY_fp8_e4m3fn.safetensors"
    ) -LocalDir (Join-Path $ComfyRoot "models\diffusion_models")

    HF-Download -Repo "Kijai/HunyuanVideo_comfy" -Include @(
        "hunyuan_video_vae_bf16.safetensors"
    ) -LocalDir (Join-Path $ComfyRoot "models\vae")

    HF-Download -Repo "Comfy-Org/sigclip_vision_384" -Include @(
        "sigclip_vision_patch14_384.safetensors"
    ) -LocalDir (Join-Path $ComfyRoot "models\clip_vision")

    HF-Download -Repo "Comfy-Org/HunyuanVideo_repackaged" -Include @(
        "split_files/text_encoders/*",
        "split_files/clip_vision/*"
    ) -LocalDir (Join-Path $ComfyRoot "models\_hf_cache\HunyuanVideo_repackaged")
}

if ($Engine -eq "wan" -or $Engine -eq "all") {
    $wanFile = "wan2.1-i2v-14b-480p-$WanQuant.gguf"
    HF-Download -Repo "city96/Wan2.1-I2V-14B-480P-gguf" -Include @(
        $wanFile
    ) -LocalDir (Join-Path $ComfyRoot "models\unet")

    HF-Download -Repo "Comfy-Org/Wan_2.1_ComfyUI_repackaged" -Include @(
        "split_files/text_encoders/*",
        "split_files/clip_vision/*",
        "split_files/vae/*"
    ) -LocalDir (Join-Path $ComfyRoot "models\_hf_cache\Wan_2.1_ComfyUI_repackaged")
}

Write-Host "[done] Telechargement demande termine. Lancer verify_install.ps1."
