# SPDX-License-Identifier: MPL-2.0
<#
.SYNOPSIS
  extract_palette_A.ps1 - 목업 이미지에서 '지정 영역'의 색을 코드로 추출(눈대중 금지). [가벼움]
.DESCRIPTION
  범례 R/Y/G, 버튼색, 헤더색 같은 핵심색을 좌표로 정밀 샘플한다. 윈도우 기본 System.Drawing 사용(설치 불필요).
  전체 자동 추출은 extract_palette_B.ps1(풀기능) 또는 파이썬판 extract_palette.py 사용.
.PARAMETER Image
  이미지 파일 경로 (png/jpg/bmp 등)
.PARAMETER Regions
  "x,y,w,h=이름; x,y,w,h=이름"  (세미콜론 구분)
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File extract_palette_A.ps1 -Image mockup.png -Regions "1082,44,14,14=범례Red; 1158,44,14,14=범례Yellow"
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$Image,
  [Parameter(Mandatory=$true)][string]$Regions
)
Add-Type -AssemblyName System.Drawing

function Get-Bucket([System.Drawing.Color]$c) {
  $h=$c.GetHue(); $s=$c.GetSaturation(); $v=$c.GetBrightness()
  if ($v -gt 0.93 -and $s -lt 0.08) { return '무채(흰/밝음)' }
  if ($v -lt 0.18)                  { return '무채(검정)' }
  if ($s -lt 0.12)                  { return '무채(회색)' }
  if ($h -lt 15 -or $h -ge 345)     { return '빨강' }
  if ($h -lt 45)                    { return '주황' }
  if ($h -lt 70)                    { return '노랑' }
  if ($h -lt 170)                   { return '초록' }
  if ($h -lt 200)                   { return '청록' }
  if ($h -lt 255)                   { return '파랑' }
  if ($h -lt 290)                   { return '보라' }
  return '분홍'
}
$HINT = @{
  '빨강'='상태색이면 statusRed'; '주황'='그대로 사용'; '노랑'='상태색이면 statusYellow';
  '초록'='상태색이면 statusGreen'; '청록'='그대로 사용'; '파랑'='그대로 사용';
  '보라'='그대로 사용'; '분홍'='그대로 사용';
  '무채(흰/밝음)'='배경 - 그대로'; '무채(회색)'='라인/텍스트 - 그대로'; '무채(검정)'='텍스트 - 그대로'
}
function Hex([System.Drawing.Color]$c){ '#{0:x2}{1:x2}{2:x2}' -f $c.R,$c.G,$c.B }

if (-not (Test-Path -LiteralPath $Image)) { Write-Error "이미지 없음: $Image"; exit 2 }
$bmp = New-Object System.Drawing.Bitmap((Resolve-Path -LiteralPath $Image).Path)
try {
  Write-Host ("# 이미지 {0}  ({1}x{2})" -f $Image, $bmp.Width, $bmp.Height)
  Write-Host ""
  Write-Host "## 지정 영역 정밀 샘플 (소면적 핵심색 - 눈대중 금지, 아래 hex 그대로 사용)"
  Write-Host ("{0,-16} {1,-9} {2,-12} {3}" -f '이름','HEX','색상군','용도')
  foreach ($spec in ($Regions -split ';')) {
    $spec = $spec.Trim(); if (-not $spec) { continue }
    $parts = $spec -split '='; $coord = $parts[0].Trim(); $label = if ($parts.Count -gt 1) { $parts[1].Trim() } else { $coord }
    $xywh = $coord -split ','; $x=[int]$xywh[0]; $y=[int]$xywh[1]; $w=[int]$xywh[2]; $h=[int]$xywh[3]
    $counts = @{}
    for ($iy=$y; $iy -lt [Math]::Min($y+$h,$bmp.Height); $iy++) {
      for ($ix=$x; $ix -lt [Math]::Min($x+$w,$bmp.Width); $ix++) {
        $p = $bmp.GetPixel($ix,$iy); $k = "$($p.R),$($p.G),$($p.B)"
        if ($counts.ContainsKey($k)) { $counts[$k]++ } else { $counts[$k]=1 }
      }
    }
    $best=$null
    foreach ($k in ($counts.GetEnumerator() | Sort-Object Value -Descending | ForEach-Object { $_.Key })) {
      $rgb = $k -split ','; $r=[int]$rgb[0]; $g=[int]$rgb[1]; $b=[int]$rgb[2]
      if ($r -gt 240 -and $g -gt 240 -and $b -gt 240) { continue }                     # 흰 스킵
      $mx=[Math]::Max($r,[Math]::Max($g,$b)); $mn=[Math]::Min($r,[Math]::Min($g,$b))
      if (($mx-$mn) -lt 12 -and $r -gt 200) { continue }                                # 옅은 회색 스킵
      $best = [System.Drawing.Color]::FromArgb($r,$g,$b); break
    }
    if (-not $best) {
      $k=($counts.GetEnumerator()|Sort-Object Value -Descending|Select-Object -First 1).Key
      $rgb=$k -split ','; $best=[System.Drawing.Color]::FromArgb([int]$rgb[0],[int]$rgb[1],[int]$rgb[2])
    }
    $bk = Get-Bucket $best
    Write-Host ("{0,-16} {1,-9} {2,-12} {3}" -f $label, (Hex $best), $bk, $HINT[$bk])
  }
  Write-Host ""
  Write-Host "규칙: 추출 hex를 XCSS에 그대로 사용. 상태색만 statusRed/statusYellow/statusGreen 클래스로. (50-color-tokens.md)"
}
finally { $bmp.Dispose() }
