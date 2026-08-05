param(
    [string]$Root = (Split-Path $PSScriptRoot -Parent),
    [string]$Archive
)

$ErrorActionPreference = 'Stop'
$rootPath = (Resolve-Path -LiteralPath $Root).Path
$selfPath = $MyInvocation.MyCommand.Path

$patterns = [ordered]@{
    'live-secret-token' = '(?i)(sk-(?:ant-|proj-)?[A-Za-z0-9_-]{16,}|AIza[0-9A-Za-z_-]{30,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,})'
    'private-key' = '-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'
    'credential-assignment' = '(?im)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|password|passwd)\b\s*[:=]\s*["'']?(?!<|\$\{|YOUR_|EXAMPLE|PLACEHOLDER|REDACTED)[A-Za-z0-9_./+=-]{12,}'
    'windows-user-path' = '(?i)[A-Z]:[\\/]+Users[\\/]+'
    'local-account-id' = '(?i)(wxid_[a-z0-9]+|codex-clipboard-[a-f0-9-]+|\.codex[\\/]+attachments|AppData[\\/]+(?:Local|Roaming)|xwechat_files)'
    'raw-corpus-file' = '(?i)(export_candidates|app_cache_fragments|selected_keep|all_scored)\.jsonl\b'
    'email-address' = '(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b'
    'cn-phone' = '(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)'
}

$textExtensions = @('.md', '.txt', '.csv', '.yaml', '.yml', '.json', '.py', '.ps1', '.toml', '.ini', '.cfg', '.js', '.ts')
$hits = [System.Collections.Generic.List[object]]::new()

function Test-Text {
    param([string]$Name, [string]$Text)

    foreach ($entry in $patterns.GetEnumerator()) {
        if ([regex]::IsMatch($Text, $entry.Value)) {
            $hits.Add([pscustomobject]@{ Category = $entry.Key; Path = $Name })
        }
    }
}

Push-Location $rootPath
try {
    $publishPaths = @(& git ls-files --cached --others --exclude-standard)
    if ($LASTEXITCODE -ne 0) { throw 'Unable to enumerate publishable files with git ls-files.' }
}
finally {
    Pop-Location
}

$files = foreach ($relativePath in $publishPaths) {
    $fullPath = Join-Path $rootPath $relativePath
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) { continue }
    $file = Get-Item -LiteralPath $fullPath
    if ($file.FullName -eq $selfPath) { continue }
    if ($textExtensions -notcontains $file.Extension.ToLowerInvariant()) { continue }
    $file
}

foreach ($file in $files) {
    $relative = $file.FullName.Substring($rootPath.Length + 1)
    Test-Text -Name $relative -Text ([IO.File]::ReadAllText($file.FullName))
}

if ($Archive) {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archivePath = (Resolve-Path -LiteralPath $Archive).Path
    $zip = [IO.Compression.ZipFile]::OpenRead($archivePath)
    try {
        foreach ($entry in $zip.Entries) {
            if ($entry.Length -eq 0 -or $entry.FullName -like '*/scripts/prepublish-audit.ps1') { continue }
            $extension = [IO.Path]::GetExtension($entry.FullName).ToLowerInvariant()
            if ($textExtensions -notcontains $extension) { continue }
            $stream = $entry.Open()
            $reader = [IO.StreamReader]::new($stream, $true)
            try {
                Test-Text -Name ("archive:" + $entry.FullName) -Text $reader.ReadToEnd()
            }
            finally {
                $reader.Dispose()
                $stream.Dispose()
            }
        }
    }
    finally {
        $zip.Dispose()
    }
}

$uniqueHits = $hits | Sort-Object Category, Path -Unique
if ($uniqueHits) {
    $uniqueHits | Format-Table -AutoSize
    Write-Error "Prepublish audit failed with $($uniqueHits.Count) sensitive-pattern hit(s). Values are intentionally not printed."
}

Write-Output "Prepublish audit passed: $($files.Count) source files checked."
if ($Archive) { Write-Output "Archive checked: $archivePath" }
