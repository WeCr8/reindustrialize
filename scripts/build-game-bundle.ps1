param([string]$Version = "0.7.0-alpha")
$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$DistRoot = Join-Path $RepoRoot "dist"
$BundleName = "reindustrialize-$Version-windows-web"
$BundleRoot = Join-Path $DistRoot $BundleName
$ZipPath = Join-Path $DistRoot "$BundleName.zip"

New-Item -ItemType Directory -Force -Path $DistRoot | Out-Null
$resolvedDist = (Resolve-Path $DistRoot).Path
if (-not $BundleRoot.StartsWith($resolvedDist, [System.StringComparison]::OrdinalIgnoreCase)) { throw "Unsafe bundle target: $BundleRoot" }
if (-not $ZipPath.StartsWith($resolvedDist, [System.StringComparison]::OrdinalIgnoreCase)) { throw "Unsafe archive target: $ZipPath" }
if (Test-Path -LiteralPath $BundleRoot) { Remove-Item -LiteralPath $BundleRoot -Recurse -Force }
if (Test-Path -LiteralPath $ZipPath) { Remove-Item -LiteralPath $ZipPath -Force }

foreach ($folder in @("game", "docs", "manifests", "media")) { New-Item -ItemType Directory -Force -Path (Join-Path $BundleRoot $folder) | Out-Null }
Copy-Item -LiteralPath (Join-Path $RepoRoot "apps\wecr8-info\prototypes\shop-floor-viewer.html") -Destination (Join-Path $BundleRoot "game\REINDUSTRIALIZE.html")
Copy-Item -LiteralPath (Join-Path $RepoRoot "GROWTH_ROADMAP_AND_RELEASE_STATUS.md") -Destination (Join-Path $BundleRoot "docs")
Copy-Item -LiteralPath (Join-Path $RepoRoot "STORY_AUDIO_VISUAL_CHECKLIST.md") -Destination (Join-Path $BundleRoot "docs")
Copy-Item -LiteralPath (Join-Path $RepoRoot "FINAL_E2E_STATUS.md") -Destination (Join-Path $BundleRoot "docs")
Copy-Item -LiteralPath (Join-Path $RepoRoot "docs\CAMPAIGN_CONTENT_CONTRACT.md") -Destination (Join-Path $BundleRoot "docs")
Copy-Item -LiteralPath (Join-Path $RepoRoot "docs\PROGRESSION_SCALE.md") -Destination (Join-Path $BundleRoot "docs")
foreach ($name in @("release-roadmap.json", "chapter-progression.json", "facilities.json", "story-production.json", "shop-tour.json", "production-task-tutorials.json")) { Copy-Item -LiteralPath (Join-Path $RepoRoot "data\$name") -Destination (Join-Path $BundleRoot "manifests") }
$video = Join-Path $RepoRoot "videos\gameplay-longform\reindustrialize-full-gameplay-garage-to-job-shop-v3.mp4"
if (Test-Path -LiteralPath $video) { Copy-Item -LiteralPath $video -Destination (Join-Path $BundleRoot "media") }

@"
# REINDUSTRIALIZE $Version

This bundle contains the verified First Playable Alpha: founder/company creation through Garage graduation and Job Shop arrival.

Run `LAUNCH_GAME.ps1` or open `game/REINDUSTRIALIZE.html` in Chrome or Edge. Voice playback may require one click because browsers protect autoplay.

Current status: completable opening campaign slice; not final six-chapter Version 1.0. See `docs/GROWTH_ROADMAP_AND_RELEASE_STATUS.md`.

No API keys, `.env` files, database credentials, or service secrets are included.
"@ | Set-Content -LiteralPath (Join-Path $BundleRoot "README.md") -Encoding utf8

@"
`$game = Join-Path `$PSScriptRoot 'game\REINDUSTRIALIZE.html'
Start-Process `$game
"@ | Set-Content -LiteralPath (Join-Path $BundleRoot "LAUNCH_GAME.ps1") -Encoding utf8

$files = Get-ChildItem -LiteralPath $BundleRoot -Recurse -File
$manifest = [ordered]@{
  bundleVersion = $Version
  createdUtc = (Get-Date).ToUniversalTime().ToString("o")
  releaseStatus = "completable_slice"
  finalCampaignComplete = $false
  campaignScope = "Garage Bay through Job Shop arrival"
  includedSecrets = $false
  files = @($files | ForEach-Object { $_.FullName.Substring($BundleRoot.Length + 1).Replace('\','/') })
}
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $BundleRoot "BUNDLE_MANIFEST.json") -Encoding utf8

$hashLines = Get-ChildItem -LiteralPath $BundleRoot -Recurse -File | Sort-Object FullName | ForEach-Object {
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
  $relative = $_.FullName.Substring($BundleRoot.Length + 1).Replace('\','/')
  "$hash  $relative"
}
$hashLines | Set-Content -LiteralPath (Join-Path $BundleRoot "SHA256SUMS.txt") -Encoding ascii
Compress-Archive -LiteralPath $BundleRoot -DestinationPath $ZipPath -CompressionLevel Optimal
$zip = Get-Item -LiteralPath $ZipPath
Write-Output "PASS: bundle $($zip.FullName) ($([math]::Round($zip.Length/1MB,1)) MB)"
