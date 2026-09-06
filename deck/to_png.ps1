$ErrorActionPreference = "Stop"
$src = Join-Path $PSScriptRoot "SIH2026_PS27_RailBlock.pptx"
$out = Join-Path $PSScriptRoot "preview"
if (Test-Path $out) { Remove-Item $out -Recurse -Force }
New-Item -ItemType Directory -Path $out | Out-Null

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($src, $true, $false, $false)
$pres.SaveCopyAs((Join-Path $out "deck.png"), 18)   # 18 = ppSaveAsPNG
$pres.Close()
$ppt.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null

# PowerPoint drops the slides into a "deck" subfolder - flatten it
$sub = Join-Path $out "deck"
if (Test-Path $sub) {
    Get-ChildItem $sub -Filter *.PNG | Move-Item -Destination $out -Force
    Remove-Item $sub -Recurse -Force
}
Get-ChildItem $out -Filter *.PNG | ForEach-Object { $_.Name }
