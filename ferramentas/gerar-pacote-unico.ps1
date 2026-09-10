$ErrorActionPreference = 'Stop'

$raizDoPacote = Split-Path -Parent $PSScriptRoot
$saida = Join-Path $raizDoPacote 'PACOTE-UNICO-PARA-CHATGPT-E-CLAUDE.md'
$arquivos = @(
    (Join-Path $raizDoPacote 'AGENTS.md')
)
$arquivos += Get-ChildItem -LiteralPath (Join-Path $raizDoPacote 'instrucoes') -Filter '*.md' -File | Sort-Object Name | Select-Object -ExpandProperty FullName
$arquivos += Join-Path $raizDoPacote 'prompts\PROMPT-PORTATIL-ABERTURA-E-ORGANIZACAO-DE-CASO.md'

$partes = @(
    '# Pacote único de instruções da SA Advocacia'
    ''
    'Este arquivo reúne as regras necessárias para uso no ChatGPT, Claude e outras inteligências artificiais que aceitem arquivos Markdown. Leia todo o conteúdo antes de atuar.'
)

foreach ($arquivo in $arquivos) {
    if (-not (Test-Path -LiteralPath $arquivo -PathType Leaf)) {
        throw "Arquivo obrigatório não encontrado: $arquivo"
    }

    $nomeRelativo = [System.IO.Path]::GetRelativePath($raizDoPacote, $arquivo).Replace('\', '/')
    $conteudo = Get-Content -LiteralPath $arquivo -Raw -Encoding UTF8
    $partes += ''
    $partes += "<!-- INÍCIO DO ARQUIVO: $nomeRelativo -->"
    $partes += $conteudo.TrimEnd()
    $partes += "<!-- FIM DO ARQUIVO: $nomeRelativo -->"
}

$textoFinal = ($partes -join "`r`n") + "`r`n"
[System.IO.File]::WriteAllText($saida, $textoFinal, [System.Text.UTF8Encoding]::new($false))
Write-Host "Pacote criado: $saida"
