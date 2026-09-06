$ErrorActionPreference = "Stop"
$src = Join-Path $PSScriptRoot "SIH2026_PS27_RailBlock.pptx"
$pdf = Join-Path $PSScriptRoot "SIH2026_PS27_RailBlock.pdf"
if (Test-Path $pdf) { Remove-Item $pdf -Force }

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($src, $true, $false, $false)
$pres.SaveAs($pdf, 32)          # 32 = ppSaveAsPDF
$pres.Close()
$ppt.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null

$f = Get-Item $pdf
"{0}  ({1:N0} KB)" -f $f.FullName, ($f.Length / 1KB)
