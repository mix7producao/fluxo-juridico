$ErrorActionPreference = 'Stop'

$raizDoPacote = Split-Path -Parent $PSScriptRoot
$origem = Join-Path $raizDoPacote 'habilidades\organizar-caso-juridico'

if (-not (Test-Path -LiteralPath (Join-Path $origem 'SKILL.md') -PathType Leaf)) {
    throw 'A pasta da habilidade está incompleta. Baixe novamente o pacote inteiro.'
}

$perfilDoUsuario = [Environment]::GetFolderPath('UserProfile')
$destinos = @(
    (Join-Path $perfilDoUsuario '.codex\skills\organizar-caso-juridico'),
    (Join-Path $perfilDoUsuario '.claude\skills\organizar-caso-juridico')
)

foreach ($destino in $destinos) {
    New-Item -ItemType Directory -Path $destino -Force | Out-Null
    Get-ChildItem -LiteralPath $origem -Force | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $destino -Recurse -Force
    }

    if (-not (Test-Path -LiteralPath (Join-Path $destino 'SKILL.md') -PathType Leaf)) {
        throw "Não foi possível conferir a instalação em: $destino"
    }

    Write-Host "Instalado em: $destino"
}

Write-Host 'Codex: use $organizar-caso-juridico.'
Write-Host 'Claude Code: use /organizar-caso-juridico.'
