# SPDX-License-Identifier: MPL-2.0
#!/usr/bin/env python3
r"""
extract_screen.py — 렌더된 SPA 화면에서 '블록/그리드/컬럼/샘플행'을 텍스트 스펙으로 뽑는다.
왜: 1MB SPA를 모델에 통째로 주면 (1) 컨텍스트 폭발 (2) 작은 모델은 빈 <div>만 보고
    "빈 화면"으로 끝낸다. 렌더된 DOM에서 컬럼/행을 미리 추출해 worklog에 고정하면
    두 문제가 동시에 사라진다(→ ../../prompts/GATE.md STEP 0, ../docs/source-assets-guide.md).

★ 입력은 반드시 '렌더된 DOM'이다 (SPA 원본 소스 아님).
  방법1) --from-file rendered.html   ← DevTools 콘솔 extract_screen.js 로 저장했거나,
                                        Elements 탭에서 <html> 우클릭 Copy → Copy outerHTML 로 저장한 파일
  방법2) --browser <url 또는 file>    ← 설치된 Edge/Chrome/Chromium 헤드리스로 직접 렌더(★폐쇄망 권장, 추가설치·인터넷 불필요)
  방법3) --render <url 또는 file>     ← Playwright 있으면 그걸로, 없으면 방법2로 자동 폴백
  방법4) --crawl <시작 file>          ← 시작 파일부터 <a href> 링크를 따라 여러 페이지를 순회 렌더+추출
                                        (헤드리스 필요. 같은 시작폴더 하위 로컬 HTML만, 외부/앵커/메일 제외.
                                         --depth 추적깊이, --max-pages 상한. 정적/​SPA 자동 — SPA면 --wait 만큼 대기)

사용:
  python3 extract_screen.py --from-file rendered.html [--rows 5] [--json spec.json] [--out spec.md]
  python3 extract_screen.py --browser ./mockup.html [--wait 2000] [--browser-bin "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]
  python3 extract_screen.py --crawl ./index.html --depth 1 --max-pages 20 --wait 5000 --out spec.md
  python3 extract_screen.py --render http://localhost:3000/attendance --wait 1500 [--out spec.md]
의존: 파싱은 표준 라이브러리만. --browser/--crawl 은 설치된 브라우저만 있으면 됨(무설치). --render 의 playwright 경로만 playwright 필요.
"""
import sys, json, re, argparse
from html.parser import HTMLParser

VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}
SKIP = {"script","style","noscript","template","svg","path","defs","symbol"}

class Node:
    __slots__ = ("tag","attrs","children","parent","text")
    def __init__(self, tag, attrs=None, parent=None):
        self.tag=tag; self.attrs=attrs or {}; self.children=[]; self.parent=parent; self.text=""

class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root=Node("#root"); self.cur=self.root; self._skip=0
    def handle_starttag(self, tag, attrs):
        if self._skip: 
            if tag not in VOID: self._skip+=1
            return
        if tag in SKIP: self._skip=1; return
        n=Node(tag, dict(attrs), self.cur); self.cur.children.append(n)
        if tag not in VOID: self.cur=n
    def handle_startendtag(self, tag, attrs):
        if self._skip: return
        if tag in SKIP: return
        n=Node(tag, dict(attrs), self.cur); self.cur.children.append(n)
    def handle_endtag(self, tag):
        if self._skip:
            if tag in SKIP or tag not in VOID: self._skip=max(0,self._skip-1)
            return
        p=self.cur
        while p is not None and p.tag!=tag: p=p.parent
        if p is not None and p.parent is not None: self.cur=p.parent
    def handle_data(self, data):
        if self._skip: return
        s=data.strip()
        if s: self.cur.text=(self.cur.text+" "+s).strip()

def cls(n): return " ".join(n.attrs.get("class","").split()).lower()
def idof(n): return n.attrs.get("id","")
def role(n): return n.attrs.get("role","").lower()

def _is_icon(n):
    c=cls(n); st=n.attrs.get("style","").lower()
    return ("material-symbols" in c or "material-icons" in c
            or "material symbols" in st or "material icons" in st)

def alltext(n, limit=120):
    out=[]
    def rec(x):
        if _is_icon(x): return          # 아이콘 폰트 리거처(inventory_2/search 등) 제외
        if x.text: out.append(x.text)
        for c in x.children: rec(c)
    rec(n)
    t=re.sub(r"\s+"," "," ".join(out)).strip()
    return t[:limit]

def walk(n):
    yield n
    for c in n.children:
        yield from walk(c)

def disp(n):
    m=re.search(r"display\s*:\s*([a-z-]+)", n.attrs.get("style","").lower())
    return m.group(1) if m else ""

GRIDLIB=("ag-root","handsontable","tabulator","dx-datagrid","el-table","ant-table",
         "mui-datagrid","muidatagrid","slick-","rt-table","k-grid","x-grid","datagrid","nx-grid")
_HDRCLS=("header-cell","column-header","col-header","ag-header-cell-text")

def is_grid_el(n):
    c=cls(n)
    return (n.tag=="table" or role(n) in ("grid","treegrid")
            or any(g in c for g in GRIDLIB) or disp(n)=="table")
def is_row_el(n):
    return (n.tag=="tr" or role(n)=="row" or cls(n).split()[:1]==["row"] or disp(n)=="table-row")
def is_cell_el(n):
    return (n.tag in ("td","th") or role(n) in ("cell","gridcell")
            or "cell" in cls(n) or disp(n)=="table-cell")
def is_headgrp(n): return n.tag=="thead" or disp(n)=="table-header-group"
def is_bodygrp(n): return n.tag=="tbody" or disp(n)=="table-row-group"

def _clean_hdr(t): return re.sub(r"\s*[↕↑↓⇅]\s*$","",t).strip()

def find_grids(root, max_rows):
    grids=[]; seen=set(); grid_nodes=[]
    for n in walk(root):
        if id(n) in seen: continue
        if not is_grid_el(n): continue
        # 헤더/바디 그룹 탐색
        hg=bg=None
        for x in walk(n):
            if hg is None and is_headgrp(x): hg=x
            if bg is None and is_bodygrp(x): bg=x
        # 헤더 컬럼: ① 헤더그룹의 첫 행 셀 ② th/columnheader/헤더클래스
        cols=[]
        if hg:
            for r in walk(hg):
                if is_row_el(r):
                    cols=[_clean_hdr(alltext(c2,40)) for c2 in r.children if is_cell_el(c2)]
                    cols=[c2 for c2 in cols if c2!=""]
                    break
        if not cols:
            for x in walk(n):
                if x.tag=="th" or role(x)=="columnheader" or any(k in cls(x) for k in _HDRCLS):
                    t=_clean_hdr(alltext(x,40))
                    if t and t not in cols: cols.append(t)
        # 바디 행 (헤더그룹 밖 = 바디그룹 우선, 없으면 그리드 전체)
        scope=bg if bg else n
        body_rows=[]
        for r in walk(scope):
            if hg is not None and (r is hg or _contains(hg, r)): continue
            if is_row_el(r):
                cells=[c2 for c2 in r.children if is_cell_el(c2)]
                if not cells:
                    cells=[c2 for c2 in r.children if c2.children or c2.text]
                vals=[alltext(c2,40) for c2 in cells]          # 위치 보존(빈 셀 포함)
                if any(v!="" for v in vals):
                    body_rows.append(vals)
            if len(body_rows)>=max_rows*4: break
        # 헤더 그룹이 없어 첫 행이 헤더면 분리
        if not cols and body_rows:
            cols=[_clean_hdr(v) for v in body_rows[0]]; body_rows=body_rows[1:]
        if cols and body_rows and [_clean_hdr(v) for v in body_rows[0]]==cols:
            body_rows=body_rows[1:]
        rows=body_rows[:max_rows]
        if cols or rows:
            for x in walk(n): seen.add(id(x))
            grid_nodes.append(n)
            c=cls(n)
            gid = idof(n) or (c.split()[0] if c else "grid")
            grids.append({"id":gid,"columns":cols,"sample_rows":rows,"row_estimate":len(body_rows)})
    return grids, grid_nodes

def _contains(anc, node):
    p=node.parent
    while p is not None:
        if p is anc: return True
        p=p.parent
    return False

def find_forms(root):
    forms=[]
    for n in walk(root):
        inputs=[x for x in walk(n) if x.tag in ("input","select","textarea")]
        # 가장 안쪽 공통 컨테이너일 때만: 하위 '컨테이너'(입력요소 자신 제외)가 전부를 담으면 스킵
        if len(inputs)>=1:
            child_max=0
            for ch in n.children:
                if ch.tag in ("input","select","textarea"): continue
                ci=[x for x in walk(ch) if x.tag in ("input","select","textarea")]
                child_max=max(child_max,len(ci))
            if child_max==len(inputs): continue
            if n.tag in ("html","body","#root","form") and len(inputs)<2 and child_max==0 and len(inputs)!=len([x for x in n.children if x.tag in ("input","select","textarea")]): continue
            controls=[]
            for x in inputs:
                lbl=x.attrs.get("aria-label") or x.attrs.get("placeholder") or x.attrs.get("name") or \
                    x.attrs.get("id") or (x.attrs.get("type","text") if x.tag=="input" else x.tag)
                controls.append(f"{x.tag}({x.attrs.get('type','')}):{lbl}".rstrip(":"))
            fid = idof(n) or (cls(n).split()[0] if cls(n) else "form")
            forms.append({"id":fid,"controls":controls[:20]})
    # 중복(포함관계) 제거: 가장 큰 것만
    forms.sort(key=lambda f:-len(f["controls"]))
    uniq=[]; used=set()
    for f in forms:
        key=tuple(f["controls"])
        if key in used: continue
        used.add(key); uniq.append(f)
    return uniq[:6]

def find_buttons(root, grid_nodes=()):
    btns=[]
    def add(t):
        t=t.strip()
        if t and 1<=len(t)<=24 and t not in btns: btns.append(t)
    for n in walk(root):
        # 의미 태그 버튼
        if n.tag=="button" or role(n)=="button" or \
           (n.tag=="input" and n.attrs.get("type","") in ("button","submit")) or \
           (n.tag=="a" and "btn" in cls(n)):
            add(n.attrs.get("value") if n.tag=="input" else alltext(n,30)); continue
        # 비의미: cursor:pointer 스타일 div (탭/필터칩/조회 버튼 등) — 그리드 내부는 제외
        st=n.attrs.get("style","").lower()
        if "cursor:pointer" in st.replace(" ",""):
            if any(g is n or _contains(g,n) for g in grid_nodes): continue
            # 자식에 또 다른 cursor:pointer가 있으면(상위 컨테이너) 스킵 — 잎에 가까운 것만
            if any("cursor:pointer" in (c.attrs.get("style","").lower().replace(" ","")) for c in n.children): continue
            add(alltext(n,24))
    return btns[:30]

VISUAL_KEYWORDS = {
    "kpi": ("kpi", "metric", "stat", "summary"),
    "card": ("card", "tile"),
    "chart": ("chart", "graph", "plot"),
    "matrix": ("matrix", "heatmap"),
    "panel": ("widget", "dashboard-panel", "info-panel"),
}

def _visual_type(n):
    raw = " ".join([
        idof(n),
        cls(n),
        n.attrs.get("data-testid", ""),
        n.attrs.get("aria-label", ""),
    ]).lower()
    tokens = {
        value for value in re.split(r"[^a-z0-9]+", raw)
        if value
    }
    if n.tag == "canvas":
        return "chart"
    for kind, keywords in VISUAL_KEYWORDS.items():
        if any(keyword in tokens for keyword in keywords):
            return kind
    return None

def _has_media(n):
    return any(x.tag in ("img", "canvas", "video") for x in walk(n))

def _has_control(n):
    return any(
        x.tag in ("input", "select", "textarea", "button")
        or role(x) in ("button", "textbox", "combobox", "checkbox", "radio")
        for x in walk(n)
    )

def _has_value(text):
    return bool(re.search(
        r"(?<![A-Za-z])(?:[$€£₩]\s*)?[-+]?\d[\d,]*(?:\.\d+)?\s*%?",
        text,
    ))

def find_visual_blocks(root, grid_nodes=()):
    candidates=[]
    for n in walk(root):
        kind=_visual_type(n)
        if not kind:
            continue
        if any(g is n or _contains(g,n) for g in grid_nodes):
            continue

        # Prefer the most specific matching child to avoid nested dashboard duplication.
        matching_children=[
            child for child in n.children
            if _visual_type(child) is not None
        ]
        if matching_children and n.tag != "canvas":
            continue

        text_value=alltext(n,160)
        has_media=_has_media(n)
        has_control=_has_control(n)
        has_value=_has_value(text_value)
        empty=not text_value and not has_media and not has_control
        block_id=(
            idof(n)
            or n.attrs.get("data-testid")
            or (cls(n).split()[0] if cls(n) else f"{kind}-{len(candidates)+1}")
        )
        candidates.append({
            "id": block_id,
            "type": kind,
            "text": text_value,
            "has_text": bool(text_value),
            "has_value": has_value,
            "has_media": has_media,
            "has_control": has_control,
            "is_empty": empty,
        })
    return candidates[:60]

def build_spec(html, max_rows):
    tb=TreeBuilder(); tb.feed(html)
    root=tb.root
    grids, grid_nodes = find_grids(root, max_rows)
    return {"grids":grids,
            "forms":find_forms(root),
            "buttons":find_buttons(root, grid_nodes),
            "visual_blocks":find_visual_blocks(root, grid_nodes)}

def to_md(spec, footer=True):
    L=["# 화면 스펙 (렌더된 DOM에서 추출 — worklog STEP 0용)",""]
    L.append(f"- 블록 요약: 그리드 {len(spec['grids'])} · 입력영역 {len(spec['forms'])} · 버튼 {len(spec['buttons'])} · 시각블록 {len(spec.get('visual_blocks',[]))}")
    L.append("")
    if spec["grids"]:
        L.append("## 그리드 (표) — 각 그리드는 Grid+Dataset+더미행으로 구현 (빈 Div 금지)")
        for i,g in enumerate(spec["grids"],1):
            L.append(f"\n### 그리드 {i}: `{g['id']}`  (본문 약 {g['row_estimate']}행)")
            L.append(f"- 컬럼({len(g['columns'])}): " + (", ".join(g["columns"]) if g["columns"] else "⟨헤더 미검출 — 확인 필요⟩"))
            if g["sample_rows"]:
                L.append("- 샘플 행:")
                for r in g["sample_rows"]:
                    L.append(f"  - {r}")
    if spec["forms"]:
        L.append("\n## 입력/검색 영역 (div_Search + 입력 컨트롤)")
        for i,f in enumerate(spec["forms"],1):
            L.append(f"- 영역 {i} `{f['id']}`: " + ", ".join(f["controls"]))
    if spec["buttons"]:
        L.append("\n## 버튼 (div_Button)")
        L.append("- " + ", ".join(spec["buttons"]))
    if spec.get("visual_blocks"):
        L.append("\n## 시각 블록 — KPI/Card/Chart/Matrix/Panel")
        for i,b in enumerate(spec["visual_blocks"],1):
            state="EMPTY" if b["is_empty"] else "filled"
            L.append(
                f"- {i}. `{b['id']}` type={b['type']} state={state} "
                f"text={b['has_text']} value={b['has_value']} media={b['has_media']}"
            )
    if footer:
        L.append("\n> ★ 이 스펙을 worklog에 고정한 뒤, 원본 SPA는 컨텍스트에서 뺀다(다시 읽지 말 것).")
    return "\n".join(L)

import os, shutil, subprocess

def _to_url(target):
    return target if re.match(r"^https?://", target) else "file:///"+os.path.abspath(target).replace("\\","/")

def _find_browser():
    """설치된 크로미엄계 브라우저 탐지: Edge → Chrome → Chromium (폐쇄망 윈도우는 Edge가 거의 항상 있음)."""
    pf   = os.environ.get("ProgramFiles",       r"C:\Program Files")
    pfx86= os.environ.get("ProgramFiles(x86)",  r"C:\Program Files (x86)")
    lad  = os.environ.get("LOCALAPPDATA","")
    win=[ os.path.join(pfx86, r"Microsoft\Edge\Application\msedge.exe"),
          os.path.join(pf,    r"Microsoft\Edge\Application\msedge.exe"),
          os.path.join(pf,    r"Google\Chrome\Application\chrome.exe"),
          os.path.join(pfx86, r"Google\Chrome\Application\chrome.exe"),
          (os.path.join(lad,  r"Google\Chrome\Application\chrome.exe") if lad else "") ]
    for w in win:
        if w and os.path.exists(w): return w
    for name in ("msedge","microsoft-edge","google-chrome","chrome","chromium","chromium-browser"):
        p=shutil.which(name)
        if p: return p
    return None

def render_once(target, wait_ms, bin_path=None):
    """설치된 브라우저 헤드리스로 1개 URL/파일 렌더 → DOM 문자열(실패 시 None). 크롤에서 재사용."""
    exe=bin_path or _find_browser()
    if not exe: return None
    url=_to_url(target)
    flags=["--disable-gpu","--no-sandbox","--dump-dom",
           "--run-all-compositor-stages-before-draw",
           "--virtual-time-budget=%d"%max(wait_ms,500), url]
    # 구형 --headless 우선(일부 Edge는 =new 가 창모드로 샘), 실패 시 =new 폴백
    for hl in ("--headless","--headless=new"):
        try:
            out=subprocess.run([exe,hl]+flags, capture_output=True, timeout=max(30, wait_ms//1000+30))
            html=out.stdout.decode("utf-8","replace")
            if len(html)>=200:
                sys.stderr.write("[render] %s (%s) → %d chars\n"%(os.path.basename(exe),hl,len(html)))
                return html
        except Exception:
            pass
    return None

def render_with_browser(target, wait_ms, bin_path=None):
    """단일 렌더(실패 시 종료). --browser 모드용."""
    if not (bin_path or _find_browser()):
        sys.exit("설치된 브라우저(msedge/chrome/chromium)를 못 찾음. --browser-bin 으로 exe 경로를 직접 주거나, "
                 "콘솔 extract_screen.js 로 rendered.html 을 만들어 --from-file 로 쓰세요.")
    html=render_once(target, wait_ms, bin_path)
    if html is None:
        sys.exit("헤드리스 렌더 실패. 콘솔 extract_screen.js → --from-file 폴백을 쓰세요.")
    return html

def _links_from(html, page_path, start_dir):
    """렌더된 DOM에서 <a href> 중 '같은 시작폴더 하위의 로컬 페이지'만 절대경로로 반환.
       외부(http/https)·mailto·tel·javascript·#앵커·비HTML 은 제외."""
    from urllib.parse import unquote, urlsplit
    tb=TreeBuilder(); tb.feed(html); 
    hrefs=[]
    for n in walk(tb.root):
        if n.tag=="a" and n.attrs.get("href"):
            hrefs.append(n.attrs["href"])
    base=os.path.dirname(page_path)
    out=[]
    for h in hrefs:
        h=h.strip()
        if not h or h.startswith(("#","mailto:","tel:","javascript:")): continue
        sp=urlsplit(h)
        if sp.scheme in ("http","https","data","blob") or sp.netloc: continue   # 외부
        path=unquote(sp.path)
        if not path: continue
        if not re.search(r"\.(html?|xhtml)$", path, re.I): continue             # HTML 페이지만
        absP=os.path.normpath(os.path.join(base, path))
        # 시작 폴더 밖으로 나가는 링크(상위 디렉토리 등)는 제외
        if os.path.commonpath([start_dir, absP])!=start_dir: continue
        if os.path.exists(absP): out.append(absP)
    return out

def crawl(start, wait_ms, depth, max_pages, bin_path, rows):
    """start 부터 링크를 따라 BFS 순회. 각 페이지 렌더→스펙. depth/max_pages 상한으로 폭주 방지."""
    if not (bin_path or _find_browser()):
        sys.exit("크롤은 헤드리스 렌더가 필요하다. 브라우저를 못 찾음 — --browser-bin 으로 지정하거나 단일 --from-file 을 쓰세요.")
    start=os.path.abspath(start); start_dir=os.path.dirname(start)
    from collections import deque
    q=deque([(start,0)]); seen={start}; pages=[]
    while q and len(pages)<max_pages:
        path,d=q.popleft()
        html=render_once(path, wait_ms, bin_path)
        if html is None:
            sys.stderr.write("[crawl] 렌더 실패, 건너뜀: %s\n"%path); continue
        rel=os.path.relpath(path, start_dir)
        pages.append((rel, build_spec(html, rows)))
        sys.stderr.write("[crawl] (%d/%d, depth %d) %s\n"%(len(pages),max_pages,d,rel))
        if d<depth:
            for nxt in _links_from(html, path, start_dir):
                if nxt not in seen:
                    seen.add(nxt); q.append((nxt,d+1))
    return pages

def to_md_multi(pages):
    if len(pages)==1:
        return to_md(pages[0][1])
    tg=sum(len(p[1]["grids"]) for p in pages)
    tv=sum(len(p[1].get("visual_blocks",[])) for p in pages)
    L=["# 화면 스펙 (크롤 — %d개 페이지, 렌더된 DOM에서 추출)"%len(pages),"",
       "- 전체: 페이지 %d · 그리드 %d · 시각블록 %d"%(len(pages),tg,tv),
       "- 페이지: "+", ".join(p[0] for p in pages),""]
    for rel,spec in pages:
        L.append("\n---\n\n## 페이지: `%s`"%rel)
        body=to_md(spec, footer=False).split("\n",2)[2]   # 페이지 스펙 헤더 줄 제거, 푸터 없음
        L.append(body)
    L.append("\n> ★ 이 스펙을 worklog에 고정한 뒤, 원본 SPA는 컨텍스트에서 뺀다(다시 읽지 말 것).")
    return "\n".join(L)

def render_with_playwright(target, wait_ms):
    """Playwright 있으면 그걸로, 없으면 설치된 브라우저(render_with_browser)로 자동 폴백."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.stderr.write("[render] playwright 없음 → 설치된 브라우저로 폴백\n")
        return render_with_browser(target, wait_ms)
    url=_to_url(target)
    try:
        with sync_playwright() as p:
            b=p.chromium.launch(); pg=b.new_page(); pg.goto(url, wait_until="networkidle")
            pg.wait_for_timeout(wait_ms)
            html=pg.content(); b.close()
        return html
    except Exception as e:
        sys.stderr.write("[render] playwright 브라우저 실행 실패(%s) → 설치된 브라우저로 폴백\n"%e)
        return render_with_browser(target, wait_ms)

def main():
    ap=argparse.ArgumentParser()
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--from-file", help="렌더된 outerHTML 파일 (콘솔 스니펫/DevTools로 저장)")
    g.add_argument("--render", help="렌더할 URL/파일 — Playwright 있으면 그걸로, 없으면 설치된 브라우저로 자동 폴백")
    g.add_argument("--browser", help="렌더할 URL/파일 — 설치된 Edge/Chrome/Chromium 헤드리스로 직접(폐쇄망 권장, 설치 불필요)")
    g.add_argument("--crawl", help="시작 파일부터 <a href> 링크를 따라 여러 페이지를 순회 렌더+추출(헤드리스 필요)")
    ap.add_argument("--depth", type=int, default=1, help="--crawl 링크 추적 깊이(기본 1)")
    ap.add_argument("--max-pages", type=int, default=20, help="--crawl 최대 페이지 수(기본 20)")
    ap.add_argument("--browser-bin", help="브라우저 exe 경로 직접 지정(자동 탐지 실패 시)")
    ap.add_argument("--wait", type=int, default=1500, help="렌더 대기(ms) = virtual-time-budget/timeout. SPA면 이만큼 대기, 정적이면 즉시.")
    ap.add_argument("--rows", type=int, default=5, help="그리드별 샘플 행 최대 개수")
    ap.add_argument("--json", help="스펙 JSON 저장 경로")
    ap.add_argument("--out", help="스펙 Markdown 저장 경로(미지정 시 표준출력)")
    a=ap.parse_args()
    if a.crawl:
        pages=crawl(a.crawl, a.wait, a.depth, a.max_pages, a.browser_bin, a.rows)
        if not pages: sys.exit("크롤 결과 없음.")
        md=to_md_multi(pages)
        if a.json:
            open(a.json,"w",encoding="utf-8").write(json.dumps(
                {"pages":[{"page":r,**s} for r,s in pages]}, ensure_ascii=False, indent=2))
        if a.out: open(a.out,"w",encoding="utf-8").write(md); print("[OK] %s 저장 (페이지 %d)"%(a.out,len(pages)))
        else: print(md)
        return
    if a.from_file:
        html=open(a.from_file, encoding="utf-8", errors="replace").read()
    elif a.browser:
        html=render_with_browser(a.browser, a.wait, a.browser_bin)
    else:
        html=render_with_playwright(a.render, a.wait)
    if len(html) < 200:
        print("(경고) 입력 DOM이 너무 짧다 — 렌더 전 소스를 넣었을 수 있음. '렌더된 DOM'인지 확인.", file=sys.stderr)
    spec=build_spec(html, a.rows)
    md=to_md(spec)
    if a.json: open(a.json,"w",encoding="utf-8").write(json.dumps(spec,ensure_ascii=False,indent=2))
    if a.out: open(a.out,"w",encoding="utf-8").write(md); print(f"[OK] {a.out} 저장 (그리드 {len(spec['grids'])}·입력 {len(spec['forms'])}·버튼 {len(spec['buttons'])}·시각블록 {len(spec.get('visual_blocks',[]))})")
    else: print(md)

if __name__=="__main__": main()
