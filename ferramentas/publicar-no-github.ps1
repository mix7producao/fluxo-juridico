$ErrorActionPreference = 'Stop'

$raizDoPacote = Split-Path -Parent $PSScriptRoot

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'O Git não está instalado. Instale o Git para Windows e tente novamente.'
}

Set-Location -LiteralPath $raizDoPacote

if (-not (Test-Path -LiteralPath (Join-Path $raizDoPacote '.git') -PathType Container)) {
    & git init -b main
    if ($LASTEXITCODE -ne 0) { throw 'Não foi possível iniciar o repositório local.' }
}

& (Join-Path $PSScriptRoot 'gerar-pacote-unico.ps1')
if ($LASTEXITCODE -ne 0) { throw 'Não foi possível atualizar o pacote único.' }

& git add --all
if ($LASTEXITCODE -ne 0) { throw 'Não foi possível preparar os arquivos para publicação.' }

$arquivosPreparados = @(& git diff --cached --name-only)
$extensoesBloqueadas = @(
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', '.rar', '.7z',
    '.mp3', '.wav', '.m4a', '.ogg', '.mp4', '.mov', '.avi',
    '.jpg', '.jpeg', '.png', '.webp', '.heic'
)
$arquivosBloqueados = @(
    $arquivosPreparados | Where-Object {
        $extensoesBloqueadas -contains [System.IO.Path]::GetExtension($_).ToLowerInvariant()
    }
)

if ($arquivosBloqueados.Count -gt 0) {
    Write-Host 'A publicação foi interrompida porque existem arquivos que podem conter provas ou dados de clientes:'
    $arquivosBloqueados | ForEach-Object { Write-Host "  $_" }
    throw 'Retire esses arquivos do pacote antes de publicar. Não envie material de cliente ao GitHub.'
}

$alteracoes = & git status --porcelain
if ($alteracoes) {
    & git commit -m 'Atualiza instruções de organização de casos jurídicos'
    if ($LASTEXITCODE -ne 0) { throw 'Não foi possível registrar a versão local.' }
}

$origemAtual = & git remote get-url origin 2>$null
if (-not $origemAtual) {
    $url = Read-Host 'Cole o endereço HTTPS do repositório privado criado no GitHub'
    if ($url -notmatch '^https://github\.com/[^/]+/[^/]+(?:\.git)?$') {
        throw 'O endereço informado não parece ser um repositório HTTPS válido do GitHub.'
    }
    & git remote add origin $url
    if ($LASTEXITCODE -ne 0) { throw 'Não foi possível registrar o endereço do GitHub.' }
}

& git push -u origin main
if ($LASTEXITCODE -ne 0) {
    throw 'O GitHub não recebeu os arquivos. Confira o acesso à conta e tente novamente.'
}

Write-Host 'As instruções foram publicadas no repositório privado.'
