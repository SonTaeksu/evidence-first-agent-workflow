# SPDX-License-Identifier: MPL-2.0
<#
.SYNOPSIS
  extract_palette_B.ps1 - 목업 이미지에서 색을 코드로 추출(눈대중 금지). [풀기능: 자동 대표색 + 영역 샘플]
.DESCRIPTION
  이미지를 축소 후 색을 뭉쳐(양자화) 대표색을 뽑는다. 소면적 핵심색(범례 R/Y/G 등)은 -Regions로 정밀 샘플.
  윈도우 기본 System.Drawing 사용(설치 불필요). 정밀도가 더 필요하면 파이썬판 extract_palette.py 사용.
.PARAMETER Image
  이미지 파일 경로
.PARAMETER Colors
  자동 대표색 개수 (기본 14)
.PARAMETER Regions
  선택. "x,y,w,h=이름; ..." 소면적 핵심색 정밀 샘플
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File extract_palette_B.ps1 -Image mockup.png -Colors 14 -Regions "1082,44,14,14=범례Red"
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$Image,
  [int]$Colors = 14,
  [string]$Regions = ''
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

  # --- 축소 후 자동 대표색(양자화 step=24) ---
  $maxSide = 160
  $scale = [Math]::Min(1.0, $maxSide / [Math]::Max($bmp.Width, $bmp.Height))
  $nw = [Math]::Max(1,[int]($bmp.Width*$scale)); $nh = [Math]::Max(1,[int]($bmp.Height*$scale))
  $small = New-Object System.Drawing.Bitmap $nw, $nh
  $gr = [System.Drawing.Graphics]::FromImage($small)
  $gr.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $gr.DrawImage($bmp, 0, 0, $nw, $nh); $gr.Dispose()

  $step = 24; $counts = @{}; $total = $nw*$nh
  for ($iy=0; $iy -lt $nh; $iy++) {
    for ($ix=0; $ix -lt $nw; $ix++) {
      $p = $small.GetPixel($ix,$iy)
      $qr=[Math]::Min(255,[int]([Math]::Round($p.R/$step))*$step)
      $qg=[Math]::Min(255,[int]([Math]::Round($p.G/$step))*$step)
      $qb=[Math]::Min(255,[int]([Math]::Round($p.B/$step))*$step)
      $k = "$qr,$qg,$qb"
      if ($counts.ContainsKey($k)) { $counts[$k]++ } else { $counts[$k]=1 }
    }
  }
  $small.Dispose()

  $rows = $counts.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First $Colors | ForEach-Object {
    $rgb = $_.Key -split ','; $c=[System.Drawing.Color]::FromArgb([int]$rgb[0],[int]$rgb[1],[int]$rgb[2])
    $bk = Get-Bucket $c
    [pscustomobject]@{ Hex=(Hex $c); Rgb="($($c.R),$($c.G),$($c.B))"; Pct=[Math]::Round(100.0*$_.Value/$total,2);
                        Bucket=$bk; Sat=[Math]::Round($c.GetSaturation(),2); Use=$HINT[$bk] }
  }
  $chroma  = $rows | Where-Object { -not $_.Bucket.StartsWith('무채') } | Sort-Object { -($_.Sat*$_.Pct) }
  $neutral = $rows | Where-Object { $_.Bucket.StartsWith('무채') }

  Write-Host ""
  Write-Host "## 유채색 (★ 눈대중 금지, 아래 hex 그대로 사용 · 상태색만 R/Y/G)"
  Write-Host ("{0,-9} {1,-16} {2,6} {3,5}  {4,-12} {5}" -f 'HEX','RGB','비중%','채도','색상군','용도')
  foreach ($x in $chroma) { Write-Host ("{0,-9} {1,-16} {2,6} {3,5}  {4,-12} {5}" -f $x.Hex,$x.Rgb,$x.Pct,$x.Sat,$x.Bucket,$x.Use) }
  Write-Host ""
  Write-Host "## 무채색 (배경/텍스트/라인)"
  foreach ($x in $neutral) { Write-Host ("{0,-9} {1,-16} {2,6}   {3}  {4}" -f $x.Hex,$x.Rgb,$x.Pct,$x.Bucket,$x.Use) }

  # --- 선택: 소면적 핵심색 정밀 샘플 ---
  if ($Regions) {
    Write-Host ""
    Write-Host "## 지정 영역 정밀 샘플 (소면적 핵심색)"
    Write-Host ("{0,-16} {1,-9} {2,-12} {3}" -f '이름','HEX','색상군','용도')
    foreach ($spec in ($Regions -split ';')) {
      $spec=$spec.Trim(); if (-not $spec) { continue }
      $parts=$spec -split '='; $coord=$parts[0].Trim(); $label= if ($parts.Count -gt 1){$parts[1].Trim()}else{$coord}
      $xywh=$coord -split ','; $x=[int]$xywh[0]; $y=[int]$xywh[1]; $w=[int]$xywh[2]; $h=[int]$xywh[3]
      $rc=@{}
      for ($iy=$y; $iy -lt [Math]::Min($y+$h,$bmp.Height); $iy++) {
        for ($ix=$x; $ix -lt [Math]::Min($x+$w,$bmp.Width); $ix++) {
          $p=$bmp.GetPixel($ix,$iy); $k="$($p.R),$($p.G),$($p.B)"
          if ($rc.ContainsKey($k)){$rc[$k]++}else{$rc[$k]=1}
        }
      }
      $best=$null
      foreach ($k in ($rc.GetEnumerator()|Sort-Object Value -Descending|ForEach-Object{$_.Key})) {
        $rgb=$k -split ','; $r=[int]$rgb[0]; $g=[int]$rgb[1]; $b=[int]$rgb[2]
        if ($r -gt 240 -and $g -gt 240 -and $b -gt 240){continue}
        $mx=[Math]::Max($r,[Math]::Max($g,$b)); $mn=[Math]::Min($r,[Math]::Min($g,$b))
        if (($mx-$mn) -lt 12 -and $r -gt 200){continue}
        $best=[System.Drawing.Color]::FromArgb($r,$g,$b); break
      }
      if (-not $best){ $k=($rc.GetEnumerator()|Sort-Object Value -Descending|Select-Object -First 1).Key; $rgb=$k -split ','; $best=[System.Drawing.Color]::FromArgb([int]$rgb[0],[int]$rgb[1],[int]$rgb[2]) }
      $bk=Get-Bucket $best
      Write-Host ("{0,-16} {1,-9} {2,-12} {3}" -f $label,(Hex $best),$bk,$HINT[$bk])
    }
  }
  Write-Host ""
  Write-Host "규칙: 추출 hex를 XCSS에 그대로 사용. 상태색만 statusRed/statusYellow/statusGreen 클래스로. (50-color-tokens.md)"
}
finally { $bmp.Dispose() }
