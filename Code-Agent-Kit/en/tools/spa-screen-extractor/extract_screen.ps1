# SPDX-License-Identifier: MPL-2.0
<#
  extract_screen.ps1 — 렌더된 outerHTML 파일에서 '블록/그리드/컬럼/샘플행'을 스펙으로 뽑는다.
  (파이썬 extract_screen.py 의 PowerShell판. 기능은 유사, 표/입력/버튼 위주.)

  ★ 입력은 '렌더된 DOM'이다 (SPA 원본 소스 아님). 둘 중 하나:
    -File rendered.html   ← 콘솔 copy(document.documentElement.outerHTML) 또는 DevTools Copy outerHTML 로 저장한 파일
    -Browser .\mockup.html ← 설치된 Edge/Chrome/Chromium 헤드리스로 직접 렌더(★폐쇄망 권장, 추가설치·인터넷 불필요)

  사용:
    powershell -ExecutionPolicy Bypass -File extract_screen.ps1 -File rendered.html [-Rows 5] [-Out spec.md]
    powershell -ExecutionPolicy Bypass -File extract_screen.ps1 -Browser .\mockup.html [-Wait 2000] [-BrowserBin "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]

  구현: DOM 파싱은 윈도우 기본 MSHTML COM(설치 불필요, 실패 시 정규식 폴백). -Browser 는 설치된 브라우저를 헤드리스(--headless=new --dump-dom)로 호출.
  주의: 이 리눅스 환경에선 실행 테스트 불가(정적 점검만). 윈도우에서 한 번 돌려 확정할 것.
#>
param(
  [string]$File,
  [string]$Browser,
  [string]$BrowserBin,
  [int]$Wait = 1500,
  [int]$Rows = 5,
  [string]$Out
)
$ErrorActionPreference = "Stop"

function Find-Browser {
  $c = @(
    (Join-Path ${env:ProgramFiles(x86)} "Microsoft\Edge\Application\msedge.exe"),
    (Join-Path $env:ProgramFiles         "Microsoft\Edge\Application\msedge.exe"),
    (Join-Path $env:ProgramFiles         "Google\Chrome\Application\chrome.exe"),
    (Join-Path ${env:ProgramFiles(x86)}  "Google\Chrome\Application\chrome.exe"),
    (Join-Path $env:LOCALAPPDATA         "Google\Chrome\Application\chrome.exe")
  )
  foreach($p in $c){ if($p -and (Test-Path $p)){ return $p } }
  foreach($n in @("msedge","chrome","chromium")){ $cmd=Get-Command $n -ErrorAction SilentlyContinue; if($cmd){ return $cmd.Source } }
  return $null
}
function Render-Browser([string]$target,[int]$waitMs,[string]$bin){
  $exe = if($bin){ $bin } else { Find-Browser }
  if(-not $exe){ Write-Error "설치된 브라우저(msedge/chrome)를 못 찾음. -BrowserBin 으로 exe 경로를 직접 주거나, 콘솔 extract_screen.js → -File 폴백을 쓰세요."; exit 2 }
  $url = if($target -match '^https?://'){ $target } else { "file:///" + ((Resolve-Path $target).Path -replace '\\','/') }
  $vtb = [Math]::Max($waitMs,500)
  # ★ 구형 --headless 우선: 일부 Edge 버전은 --headless=new 가 창 모드로 새어 --dump-dom 이 stdout 으로 안 나온다.
  #   (사용자 환경에서 --headless 는 성공, --headless=new 는 창이 뜨고 0바이트로 확인됨)
  foreach($hl in @("--headless","--headless=new")){
    $tmp = [System.IO.Path]::GetTempFileName()
    $argv = @($hl,"--disable-gpu","--no-sandbox","--dump-dom","--run-all-compositor-stages-before-draw","--virtual-time-budget=$vtb",$url)
    try {
      # stdout 을 파일로 리다이렉트(파이프 인코딩/창모드 이슈 회피). RedirectStandardOutput 은 stdout 만 받는다.
      $p = Start-Process -FilePath $exe -ArgumentList $argv -NoNewWindow -PassThru -RedirectStandardOutput $tmp -RedirectStandardError ([System.IO.Path]::GetTempFileName())
      $p.WaitForExit([Math]::Max(30000, $vtb + 30000)) | Out-Null
      if(-not $p.HasExited){ try { $p.Kill() } catch {} }
      $h = if(Test-Path $tmp){ Get-Content -Raw -Encoding UTF8 $tmp } else { "" }
      if($h -and $h.Length -ge 200){ Write-Host "[render] $([System.IO.Path]::GetFileName($exe)) ($hl) -> $($h.Length) chars"; Remove-Item $tmp -EA SilentlyContinue; return $h }
    } catch { }
    Remove-Item $tmp -EA SilentlyContinue
  }
  Write-Error "헤드리스 렌더 실패. 콘솔 extract_screen.js -> -File 폴백을 쓰세요."; exit 2
}

if ($Browser) {
  $html = Render-Browser $Browser $Wait $BrowserBin
} elseif ($File) {
  if (-not (Test-Path $File)) { Write-Error "파일 없음: $File"; exit 2 }
  $html = Get-Content -Raw -Encoding UTF8 $File
} else {
  Write-Error "-File(렌더된 outerHTML) 또는 -Browser(직접 렌더) 중 하나는 필수."; exit 2
}
if ($html.Length -lt 200) { Write-Warning "입력 DOM이 너무 짧다 — 렌더 전 소스일 수 있음. '렌더된 DOM'인지 확인." }

function Clean([string]$s){ if($null -eq $s){return ""}; ($s -replace '\s+',' ').Trim() }

$grids  = @()
$forms  = @()
$buttons= @()

$useCom = $true
try {
  $doc = New-Object -ComObject "HTMLFile"
  try { $doc.IHTMLDocument2_write($html) } catch { $doc.write([ref]$html) }
  $doc.close()
} catch { $useCom = $false }

if ($useCom) {
  $GRIDLIB = @("ag-root","handsontable","tabulator","dx-datagrid","el-table","ant-table","muidatagrid","slick-","rt-table","k-grid","x-grid","datagrid","nx-grid")
  $claimed = @()

  function ClassOf($el){ try { ($el.className).ToString().ToLower() } catch { "" } }
  function RoleOf($el){ try { ($el.getAttribute("role")).ToString().ToLower() } catch { "" } }
  function DispOf($el){ try { ($el.style.display).ToString().ToLower() } catch { "" } }
  function IsGrid($el){
    if($el.tagName -eq "TABLE"){ return $true }
    $r = RoleOf $el; if($r -eq "grid" -or $r -eq "treegrid"){ return $true }
    $c = ClassOf $el; foreach($g in $GRIDLIB){ if($c -match [regex]::Escape($g)){ return $true } }
    if((DispOf $el) -eq "table"){ return $true }
    return $false
  }
  function IsRow($el){ $r=RoleOf $el; $c=ClassOf $el; $d=DispOf $el
    return ($el.tagName -eq "TR" -or $r -eq "row" -or $c -match "(^|\s)row(\s|$)" -or $d -eq "table-row") }
  function IsCell($el){ $r=RoleOf $el; $c=ClassOf $el; $d=DispOf $el
    return ($el.tagName -eq "TD" -or $el.tagName -eq "TH" -or $r -match "cell|gridcell" -or $c -match "cell" -or $d -eq "table-cell") }
  function CleanHdr($t){ ($t -replace '\s*[↕↑↓⇅]\s*$','').Trim() }
  function ContainsSafe($a,$b){ try { return [bool]$a.contains($b) } catch { return $false } }

  $all = $doc.getElementsByTagName("*")
  foreach($el in $all){
    if(-not (IsGrid $el)){ continue }
    $skip=$false; foreach($cl in $claimed){ try{ if($cl.contains($el)){ $skip=$true; break } }catch{} }
    if($skip){ continue }

    # 헤더 그룹(thead/table-header-group) 첫 행 우선, 없으면 th/columnheader
    $cols=@()
    $hg=$null
    foreach($x in $el.getElementsByTagName("*")){ $d=DispOf $x; if($x.tagName -eq "THEAD" -or $d -eq "table-header-group"){ $hg=$x; break } }
    if($hg){
      foreach($r in $hg.getElementsByTagName("*")){ if(IsRow $r){
        foreach($cell in $r.children){ if(IsCell $cell){ $t=CleanHdr (Clean $cell.innerText); if($t){ $cols += $t } } }
        break } }
    }
    if($cols.Count -eq 0){
      foreach($h in $el.getElementsByTagName("*")){
        $r = RoleOf $h; $c = ClassOf $h
        if($h.tagName -eq "TH" -or $r -eq "columnheader" -or $c -match "header-cell|column-header|col-header|ag-header-cell-text"){
          $t = CleanHdr (Clean $h.innerText); if($t -and ($cols -notcontains $t)){ $cols += $t }
        }
      }
    }
    # 바디 행 (헤더그룹 안은 제외)
    $rws=@(); $n=0
    foreach($tr in $el.getElementsByTagName("*")){
      if($n -ge $Rows){ break }
      if($hg -and ($tr -eq $hg -or (ContainsSafe $hg $tr))){ continue }
      if(IsRow $tr){
        $vals=@()
        foreach($cell in $tr.children){ if(IsCell $cell){ $vals += (Clean $cell.innerText) } }  # 위치 보존
        if(($vals | Where-Object { $_ -ne "" }).Count -gt 0 -and (($vals -join "|") -ne ($cols -join "|"))){ $rws += ,$vals; $n++ }
      }
    }
    if($cols.Count -eq 0 -and $rws.Count -gt 0){ $cols = $rws[0]; $rws = if($rws.Count -gt 1){ $rws[1..($rws.Count-1)] } else { @() } }
    if($cols.Count -gt 0 -or $rws.Count -gt 0){
      $claimed += $el
      $id = $el.id; if(-not $id){ $id = (ClassOf $el).Split(" ")[0]; if(-not $id){ $id="grid" } }
      $grids += [pscustomobject]@{ id=$id; columns=$cols; rows=$rws }
    }
  }

  # 입력/검색 영역
  foreach($el in $doc.getElementsByTagName("*")){
    if($el.tagName -notin @("DIV","FORM","SECTION","FIELDSET")){ continue }
    $ins=@(); foreach($x in $el.getElementsByTagName("*")){ if($x.tagName -in @("INPUT","SELECT","TEXTAREA")){ $ins += $x } }
    if($ins.Count -lt 1){ continue }
    $childMax=0
    foreach($ch in $el.children){
      if($ch.tagName -in @("INPUT","SELECT","TEXTAREA")){ continue }
      $ci=0; foreach($x in $ch.getElementsByTagName("*")){ if($x.tagName -in @("INPUT","SELECT","TEXTAREA")){ $ci++ } }
      if($ci -gt $childMax){ $childMax=$ci }
    }
    if($childMax -eq $ins.Count){ continue }
    $ctl=@(); foreach($x in $ins){
      $lbl = $x.getAttribute("aria-label"); if(-not $lbl){ $lbl=$x.getAttribute("placeholder") }
      if(-not $lbl){ $lbl=$x.name }; if(-not $lbl){ $lbl=$x.id }; if(-not $lbl){ $lbl=$x.type }
      $ctl += ($x.tagName.ToLower()+":"+$lbl)
    }
    $fid=$el.id; if(-not $fid){ $fid=(ClassOf $el).Split(" ")[0]; if(-not $fid){ $fid="form" } }
    $forms += [pscustomobject]@{ id=$fid; controls=($ctl | Select-Object -First 20) }
  }
  # 포함 중복 제거(같은 컨트롤 조합)
  $seen=@{}; $uniq=@()
  foreach($f in ($forms | Sort-Object { -$_.controls.Count })){
    $k=($f.controls -join "|"); if(-not $seen.ContainsKey($k)){ $seen[$k]=1; $uniq+=$f } }
  $forms = $uniq | Select-Object -First 6

  # 버튼
  foreach($b in $doc.getElementsByTagName("*")){
    $r=RoleOf $b; $c=ClassOf $b
    $isBtn = ($b.tagName -eq "BUTTON") -or ($r -eq "button") -or
             ($b.tagName -eq "INPUT" -and $b.type -in @("button","submit")) -or
             ($b.tagName -eq "A" -and $c -match "btn")
    if($isBtn){ $t = if($b.tagName -eq "INPUT"){ $b.value } else { Clean $b.innerText }
      if($t -and ($buttons -notcontains $t)){ $buttons += $t } }
  }
  $buttons = $buttons | Select-Object -First 25
}
else {
  # 폴백: 정규식으로 <table>만 (COM 불가 환경)
  Write-Warning "MSHTML COM 사용 불가 — 정규식 폴백(표만 추출). ag-grid 등 div 그리드는 콘솔 스니펫(extract_screen.js)을 쓰세요."
  $tables = [regex]::Matches($html, '(?is)<table[^>]*>(.*?)</table>')
  foreach($tm in $tables){
    $body=$tm.Groups[1].Value
    $cols=@(); foreach($th in [regex]::Matches($body,'(?is)<th[^>]*>(.*?)</th>')){ $cols += (Clean ($th.Groups[1].Value -replace '<[^>]+>','')) }
    $rws=@(); $n=0
    foreach($tr in [regex]::Matches($body,'(?is)<tr[^>]*>(.*?)</tr>')){
      if($n -ge $Rows){ break }
      $vals=@(); foreach($td in [regex]::Matches($tr.Groups[1].Value,'(?is)<td[^>]*>(.*?)</td>')){ $v=Clean ($td.Groups[1].Value -replace '<[^>]+>',''); if($v -ne ""){ $vals+=$v } }
      if($vals.Count -gt 0){ $rws += ,$vals; $n++ }
    }
    if($cols.Count -eq 0 -and $rws.Count -gt 0){ $cols=$rws[0]; $rws=$rws[1..($rws.Count-1)] }
    if($cols.Count -gt 0 -or $rws.Count -gt 0){ $grids += [pscustomobject]@{ id="table"; columns=$cols; rows=$rws } }
  }
}

# 출력(마크다운)
$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine("# 화면 스펙 (렌더된 DOM에서 추출 — worklog STEP 0용)")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("- 블록 요약: 그리드 $($grids.Count) · 입력영역 $($forms.Count) · 버튼 $($buttons.Count)")
[void]$sb.AppendLine("")
if($grids.Count){
  [void]$sb.AppendLine("## 그리드 (표) — 각 그리드는 Grid+Dataset+더미행으로 구현 (빈 Div 금지)")
  $i=0; foreach($g in $grids){ $i++
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("### 그리드 ${i}: ``$($g.id)``")
    $ch = if($g.columns.Count){ ($g.columns -join ", ") } else { "⟨헤더 미검출 — 확인 필요⟩" }
    [void]$sb.AppendLine("- 컬럼($($g.columns.Count)): $ch")
    if($g.rows.Count){ [void]$sb.AppendLine("- 샘플 행:"); foreach($r in $g.rows){ [void]$sb.AppendLine("  - [" + (($r | ForEach-Object { "'$_'" }) -join ", ") + "]") } }
  }
}
if($forms.Count){
  [void]$sb.AppendLine(""); [void]$sb.AppendLine("## 입력/검색 영역 (div_Search + 입력 컨트롤)")
  $i=0; foreach($f in $forms){ $i++; [void]$sb.AppendLine("- 영역 ${i} ``$($f.id)``: " + ($f.controls -join ", ")) }
}
if($buttons.Count){
  [void]$sb.AppendLine(""); [void]$sb.AppendLine("## 버튼 (div_Button)"); [void]$sb.AppendLine("- " + ($buttons -join ", "))
}
[void]$sb.AppendLine(""); [void]$sb.AppendLine("> ★ 이 스펙을 worklog에 고정한 뒤, 원본 SPA는 컨텍스트에서 뺀다(다시 읽지 말 것).")

$md = $sb.ToString()
if($Out){ [System.IO.File]::WriteAllText($Out,$md,[System.Text.Encoding]::UTF8); Write-Host "[OK] $Out 저장 (그리드 $($grids.Count)·입력 $($forms.Count)·버튼 $($buttons.Count))" }
else { Write-Output $md }
