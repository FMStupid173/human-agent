param(
    [string]$Voice = 'zh-CN-XiaoxiaoNeural',
    [string]$Rate = '+0%'
)

$ErrorActionPreference = 'Stop'
$root = Split-Path $MyInvocation.MyCommand.Path -Parent
$packageRoot = Join-Path $root 'tools\edge_tts_pkg'
$exe = Join-Path $packageRoot 'bin\edge-tts.exe'
$text = Join-Path $root 'narration.zh-CN.txt'
$public = Join-Path $root 'public'

if (-not (Test-Path -LiteralPath $exe)) {
    throw 'Install edge-tts into promo-video/tools/edge_tts_pkg first.'
}

New-Item -ItemType Directory -Path $public -Force | Out-Null
$env:PYTHONPATH = $packageRoot
& $exe `
    --file $text `
    --voice $Voice `
    --rate $Rate `
    --write-media (Join-Path $public 'voiceover.mp3') `
    --write-subtitles (Join-Path $public 'voiceover.srt') `
    --proxy 'http://127.0.0.1:7897'

if ($LASTEXITCODE -ne 0) { throw "edge-tts failed with exit code $LASTEXITCODE" }
