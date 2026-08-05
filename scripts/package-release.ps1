param(
    [string]$ProjectRoot = (Split-Path $PSScriptRoot -Parent),
    [string]$OutputDirectory = (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
)

$ErrorActionPreference = 'Stop'
$projectPath = (Resolve-Path -LiteralPath $ProjectRoot).Path
$outputPath = (Resolve-Path -LiteralPath $OutputDirectory).Path
$version = (Get-Content -LiteralPath (Join-Path $projectPath 'VERSION') -Raw).Trim()
$archivePath = Join-Path $outputPath ("human-agent-v{0}.zip" -f $version)
$rootName = Split-Path $projectPath -Leaf

& (Join-Path $projectPath 'scripts\prepublish-audit.ps1') -Root $projectPath

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
if ([IO.File]::Exists($archivePath)) { [IO.File]::Delete($archivePath) }

$zip = [System.IO.Compression.ZipFile]::Open($archivePath, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    $files = Get-ChildItem -LiteralPath $projectPath -Recurse -File | Where-Object {
        $_.FullName -notmatch '[\\/]\.git[\\/]' -and
        $_.FullName -notmatch '[\\/]calibrator[\\/]runs[\\/]' -and
        $_.FullName -notmatch '[\\/]calibrator[\\/]config\.local\.json$' -and
        $_.FullName -notmatch '[\\/](?:raw|private|exports|data)[\\/]' -and
        $_.Name -notmatch '^\.env(?:\..+)?$' -and
        $_.Name -notmatch '^(?:credentials.*\.json|secrets(?:\..*)?)$' -and
        $_.FullName -notmatch '[\\/]__pycache__[\\/]' -and
        $_.FullName -notmatch '[\\/]promo-video[\\/](?:node_modules|out)[\\/]' -and
        $_.Extension -notin '.pyc', '.zip', '.jsonl', '.pem', '.key', '.p12', '.pfx', '.db', '.sqlite', '.sqlite3'
    }
    foreach ($file in $files) {
        $relative = $file.FullName.Substring($projectPath.Length + 1).Replace('\', '/')
        $entryName = "$rootName/$relative"
        [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $file.FullName, $entryName, [IO.Compression.CompressionLevel]::Optimal) | Out-Null
    }
}
finally {
    $zip.Dispose()
}

& (Join-Path $projectPath 'scripts\prepublish-audit.ps1') -Root $projectPath -Archive $archivePath
$hash = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLowerInvariant()
[IO.File]::WriteAllText("$archivePath.sha256", "$hash  $(Split-Path $archivePath -Leaf)`n", [Text.UTF8Encoding]::new($false))
Write-Output "Release archive: $archivePath"
Write-Output "SHA256: $hash"
