param(
    [string]$ComfyRoot = "C:\Users\saint\Documents\Codex\ComfyUI"
)

$ErrorActionPreference = "Stop"

function Test-ItemReport {
    param(
        [string]$Label,
        [string]$Path
    )

    if (Test-Path -LiteralPath $Path) {
        $item = Get-Item -LiteralPath $Path
        if ($item.PSIsContainer) {
            Write-Host "[OK] $Label -> $Path"
        } else {
            Write-Host ("[OK] {0} -> {1} ({2:N2} GB)" -f $Label, $Path, ($item.Length / 1GB))
        }
        return $true
    }

    Write-Host "[MISS] $Label -> $Path"
    return $false
}

Write-Host "=== ComfyUI ==="
Test-ItemReport "ComfyUI root" $ComfyRoot | Out-Null
Test-ItemReport "Python venv" (Join-Path $ComfyRoot ".venv\Scripts\python.exe") | Out-Null

Write-Host "`n=== Custom nodes ==="
Test-ItemReport "FramePack wrapper" (Join-Path $ComfyRoot "custom_nodes\ComfyUI-FramePackWrapper") | Out-Null
Test-ItemReport "ComfyUI-GGUF" (Join-Path $ComfyRoot "custom_nodes\ComfyUI-GGUF") | Out-Null

Write-Host "`n=== FramePack models ==="
Test-ItemReport "FramePack FP8" (Join-Path $ComfyRoot "models\diffusion_models\FramePackI2V_HY_fp8_e4m3fn.safetensors") | Out-Null
Test-ItemReport "Hunyuan VAE bf16" (Join-Path $ComfyRoot "models\vae\hunyuan_video_vae_bf16.safetensors") | Out-Null
Test-ItemReport "SigCLIP 384" (Join-Path $ComfyRoot "models\clip_vision\sigclip_vision_patch14_384.safetensors") | Out-Null
Test-ItemReport "Hunyuan support cache" (Join-Path $ComfyRoot "models\_hf_cache\HunyuanVideo_repackaged") | Out-Null

Write-Host "`n=== Wan2.1 GGUF models ==="
Test-ItemReport "Wan Q5 GGUF" (Join-Path $ComfyRoot "models\unet\wan2.1-i2v-14b-480p-Q5_K_S.gguf") | Out-Null
Test-ItemReport "Wan Q4 GGUF fallback" (Join-Path $ComfyRoot "models\unet\wan2.1-i2v-14b-480p-Q4_K_S.gguf") | Out-Null
Test-ItemReport "Wan support cache" (Join-Path $ComfyRoot "models\_hf_cache\Wan_2.1_ComfyUI_repackaged") | Out-Null

Write-Host "`n=== GPU check ==="
$python = Join-Path $ComfyRoot ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $python) {
    & $python -c "import torch; print('torch', torch.__version__); print('cuda_available', torch.cuda.is_available()); print('gpu', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'none'); print('vram_gb', round(torch.cuda.get_device_properties(0).total_memory/1024**3,2) if torch.cuda.is_available() else 0)"
}

Write-Host "`nVerifier ensuite /object_info dans ComfyUI pour les noeuds FramePack et GGUF."

