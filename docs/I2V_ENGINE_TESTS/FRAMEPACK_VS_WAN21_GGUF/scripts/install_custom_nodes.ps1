param(
    [string]$ComfyRoot = "C:\Users\saint\Documents\Codex\ComfyUI"
)

$ErrorActionPreference = "Stop"
$customNodes = Join-Path $ComfyRoot "custom_nodes"

if (!(Test-Path -LiteralPath $customNodes)) {
    throw "Dossier custom_nodes introuvable: $customNodes"
}

function Install-GitRepo {
    param(
        [string]$Url,
        [string]$Name
    )

    $target = Join-Path $customNodes $Name
    if (Test-Path -LiteralPath $target) {
        Write-Host "[skip] $Name deja present: $target"
        git -C $target status --short
        return
    }

    Write-Host "[clone] $Url -> $target"
    git clone $Url $target
}

Install-GitRepo -Url "https://github.com/kijai/ComfyUI-FramePackWrapper.git" -Name "ComfyUI-FramePackWrapper"
Install-GitRepo -Url "https://github.com/city96/ComfyUI-GGUF.git" -Name "ComfyUI-GGUF"

Write-Host "[done] Custom nodes installes. Redemarrer ComfyUI avant verification /object_info."

