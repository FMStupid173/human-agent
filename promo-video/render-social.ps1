$ErrorActionPreference = 'Stop'
$root = Split-Path $MyInvocation.MyCommand.Path -Parent
$remotion = Join-Path $root 'node_modules\.bin\remotion.cmd'
$output = Join-Path $root 'out\xiaohongshu'

New-Item -ItemType Directory -Path $output -Force | Out-Null
Push-Location $root
try {
    & $remotion still 'src/index.ts' 'HumanAgentCover' 'out/human-agent-cover-social.png' '--frame=0'
    if ($LASTEXITCODE -ne 0) { throw 'Cover render failed.' }

    for ($frame = 0; $frame -lt 7; $frame++) {
        $number = '{0:D2}' -f ($frame + 1)
        & $remotion still 'src/index.ts' 'HumanAgentXhsCarousel' "out/xiaohongshu/human-agent-$number.png" "--frame=$frame"
        if ($LASTEXITCODE -ne 0) { throw "Carousel frame $frame failed." }
    }
}
finally {
    Pop-Location
}
