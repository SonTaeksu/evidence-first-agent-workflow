/* SPDX-License-Identifier: MPL-2.0 */
/* ============================================================================
 * extract_screen.js — 브라우저 콘솔용 (프레임워크 무관 · 폐쇄망 OK · 설치 불필요)
 *
 * SPA는 데이터가 JS 렌더 결과라 소스 파일엔 빈 <div>만 있다. 실행 중인 화면의
 * 렌더된 DOM에서 직접 뽑으므로 가장 확실하다. getComputedStyle 로 display:table
 * 기반(의미 태그 없는) 그리드까지 인식한다.
 *
 * 사용:
 *   1) 목업 SPA를 브라우저로 연다 (데이터가 다 그려진 상태).
 *   2) F12 → Console 에 이 파일 전체를 붙여넣고 Enter. (붙여넣기 경고 시: allow pasting 입력 후 Enter)
 *   3) 스펙(마크다운)이 출력되고 클립보드에 복사된다 → worklog에 붙인다.
 *   4) rendered.html 이 필요하면:  copy(document.documentElement.outerHTML)
 *
 * ★ 이 스펙만 worklog에 고정하고 원본 SPA는 모델 컨텍스트에서 뺀다(다시 읽지 말 것).
 * ============================================================================ */
(function (MAX_ROWS) {
  MAX_ROWS = MAX_ROWS || 5;
  var GRIDLIB = ["ag-root","handsontable","tabulator","dx-datagrid","el-table","ant-table",
                 "muidatagrid","slick-","rt-table","k-grid","x-grid","datagrid","nx-grid"];
  var cs = function (el) { try { return getComputedStyle(el); } catch (e) { return {}; } };
  var disp = function (el) { return (cs(el).display || "").toLowerCase(); };
  var cls = function (el) { var c=el.className; return ((c&&c.baseVal!==undefined?c.baseVal:c)||"").toString().toLowerCase(); };
  var role = function (el) { return (el.getAttribute&&el.getAttribute("role")||"").toLowerCase(); };
  var isIcon = function (el) { var c=cls(el), f=(cs(el).fontFamily||"").toLowerCase();
    return c.indexOf("material-symbols")>=0||c.indexOf("material-icons")>=0||f.indexOf("material symbols")>=0||f.indexOf("material icons")>=0; };
  function txt(el, n){
    if(!el) return "";
    if(el.nodeType===3) return el.nodeValue;
    if(el.nodeType!==1||isIcon(el)) return "";
    var s=""; for(var i=0;i<el.childNodes.length;i++) s+=txt(el.childNodes[i]);
    s=s.replace(/\s+/g," ").trim(); return n?s.slice(0,n):s;
  }
  var cleanHdr = function (t){ return t.replace(/\s*[↕↑↓⇅]\s*$/,"").trim(); };

  function isGrid(el){ if(el.tagName==="TABLE") return true; var r=role(el),c=cls(el);
    if(r==="grid"||r==="treegrid") return true;
    for(var i=0;i<GRIDLIB.length;i++) if(c.indexOf(GRIDLIB[i])>=0) return true;
    return disp(el)==="table"; }
  var isRow  = function(el){ return el.tagName==="TR"||role(el)==="row"||cls(el).split(" ")[0]==="row"||disp(el)==="table-row"; };
  var isCell = function(el){ return el.tagName==="TD"||el.tagName==="TH"||role(el)==="cell"||role(el)==="gridcell"||cls(el).indexOf("cell")>=0||disp(el)==="table-cell"; };
  var isHead = function(el){ return el.tagName==="THEAD"||disp(el)==="table-header-group"; };
  var isBody = function(el){ return el.tagName==="TBODY"||disp(el)==="table-row-group"; };
  function contains(a,b){ return a!==b && a.contains(b); }
  function descend(el,pred){ var out=[],st=[el]; while(st.length){ var x=st.pop();
    for(var i=0;i<x.children.length;i++){ var c=x.children[i]; if(pred(c)) out.push(c); st.push(c); } } return out; }
  function firstDesc(el,pred){ var st=[el]; while(st.length){ var x=st.shift();
    for(var i=0;i<x.children.length;i++){ var c=x.children[i]; if(pred(c)) return c; st.push(c); } } return null; }

  function grids(){
    var found=[], claimed=[];
    var all=document.querySelectorAll("*");
    for(var i=0;i<all.length;i++){ var el=all[i];
      if(!isGrid(el)) continue;
      var skip=false; for(var k=0;k<claimed.length;k++){ if(claimed[k].contains(el)){ skip=true; break; } }
      if(skip) continue;
      var hg=firstDesc(el,isHead), bg=firstDesc(el,isBody);
      var cols=[];
      if(hg){ var hr=firstDesc(hg,isRow); if(hr){ var hc=[]; for(var a=0;a<hr.children.length;a++) if(isCell(hr.children[a])) hc.push(hr.children[a]);
        cols=hc.map(function(c){return cleanHdr(txt(c,40));}).filter(function(t){return t!=="";}); } }
      if(!cols.length){ var hs=descend(el,function(x){return x.tagName==="TH"||role(x)==="columnheader"||/header-cell|column-header|col-header|ag-header-cell-text/.test(cls(x));});
        hs.forEach(function(h){ var t=cleanHdr(txt(h,40)); if(t&&cols.indexOf(t)<0) cols.push(t); }); }
      var scope=bg||el, rws=[];
      var rowEls=descend(scope,isRow);
      for(var r=0;r<rowEls.length && rws.length<MAX_ROWS*4;r++){ var row=rowEls[r];
        if(hg&&(row===hg||contains(hg,row))) continue;
        var cells=[]; for(var b=0;b<row.children.length;b++) if(isCell(row.children[b])) cells.push(row.children[b]);
        if(!cells.length) cells=Array.prototype.slice.call(row.children);
        var vals=cells.map(function(c){return txt(c,40);});
        if(vals.some(function(v){return v!=="";})) rws.push(vals);
      }
      if(!cols.length && rws.length){ cols=rws[0].map(cleanHdr); rws=rws.slice(1); }
      if(cols.length && rws.length && JSON.stringify(rws[0].map(cleanHdr))===JSON.stringify(cols)) rws=rws.slice(1);
      if(cols.length||rws.length){ claimed.push(el);
        found.push({node:el, id: el.id||(cls(el).split(" ")[0]||"grid"), columns:cols, rows:rws.slice(0,MAX_ROWS), est:rowEls.length}); }
    }
    return found;
  }
  function forms(){
    var out=[]; document.querySelectorAll("div,form,section,fieldset").forEach(function(el){
      var ins=el.querySelectorAll("input,select,textarea"); if(!ins.length) return;
      var childMax=0; for(var i=0;i<el.children.length;i++){ var ch=el.children[i];
        if(/^(INPUT|SELECT|TEXTAREA)$/.test(ch.tagName)) continue;
        childMax=Math.max(childMax, ch.querySelectorAll("input,select,textarea").length); }
      if(childMax===ins.length) return;
      var ctl=[]; ins.forEach(function(x){ var lbl=x.getAttribute("aria-label")||x.placeholder||x.name||x.id||(x.type||x.tagName.toLowerCase());
        ctl.push(x.tagName.toLowerCase()+(x.type?"("+x.type+")":"")+":"+lbl); });
      out.push({id: el.id||(cls(el).split(" ")[0]||"form"), controls: ctl.slice(0,20)});
    });
    var seen={},uniq=[]; out.sort(function(a,b){return b.controls.length-a.controls.length;});
    out.forEach(function(f){ var k=f.controls.join("|"); if(!seen[k]){seen[k]=1;uniq.push(f);} });
    return uniq.slice(0,6);
  }
  function buttons(gridNodes){
    var out=[]; function add(t){ t=(t||"").trim(); if(t&&t.length<=24&&out.indexOf(t)<0) out.push(t); }
    var all=document.querySelectorAll("*");
    for(var i=0;i<all.length;i++){ var el=all[i];
      if(el.tagName==="BUTTON"||role(el)==="button"||(el.tagName==="INPUT"&&/^(button|submit)$/.test(el.type))||(el.tagName==="A"&&cls(el).indexOf("btn")>=0)){
        add(el.tagName==="INPUT"?el.value:txt(el,24)); continue; }
      if((cs(el).cursor||"")==="pointer"){
        var inGrid=false; for(var g=0;g<gridNodes.length;g++){ if(gridNodes[g]===el||gridNodes[g].contains(el)){ inGrid=true; break; } }
        if(inGrid) continue;
        var childPtr=false; for(var c=0;c<el.children.length;c++){ if((cs(el.children[c]).cursor||"")==="pointer"){ childPtr=true; break; } }
        if(childPtr) continue;
        add(txt(el,24));
      }
    }
    return out.slice(0,30);
  }

  function visualBlocks(gridNodes){
    var keywords={
      kpi:["kpi","metric","stat","summary"],
      card:["card","tile"],
      chart:["chart","graph","plot"],
      matrix:["matrix","heatmap"],
      panel:["widget","dashboard","panel"]
    };
    function visualType(el){
      if(el.tagName==="CANVAS") return "chart";
      var raw=[
        el.id||"",
        cls(el),
        el.getAttribute&&el.getAttribute("data-testid")||"",
        el.getAttribute&&el.getAttribute("aria-label")||""
      ].join(" ").toLowerCase();
      var tokens=raw.split(/[^a-z0-9]+/).filter(Boolean);
      for(var kind in keywords){
        for(var i=0;i<keywords[kind].length;i++){
          if(tokens.indexOf(keywords[kind][i])>=0) return kind;
        }
      }
      return null;
    }
    var result=[], all=document.querySelectorAll("*");
    for(var i=0;i<all.length;i++){
      var el=all[i], kind=visualType(el);
      if(!kind) continue;
      var inGrid=false;
      for(var g=0;g<gridNodes.length;g++){
        if(gridNodes[g]===el||gridNodes[g].contains(el)){inGrid=true;break;}
      }
      if(inGrid) continue;
      var childMatch=false;
      for(var c=0;c<el.children.length;c++){
        if(visualType(el.children[c])){childMatch=true;break;}
      }
      if(childMatch&&el.tagName!=="CANVAS") continue;
      var value=txt(el,160);
      var hasMedia=!!el.querySelector("img,canvas,video")||el.tagName==="CANVAS";
      var hasControl=!!el.querySelector("input,select,textarea,button,[role=button],[role=textbox],[role=combobox]");
      var hasValue=/(?:^|[^A-Za-z])(?:[$€£₩]\s*)?[-+]?\d[\d,]*(?:\.\d+)?\s*%?/.test(value);
      var blockId=el.id||el.getAttribute("data-testid")||(cls(el).split(" ")[0]||kind+"-"+(result.length+1));
      result.push({
        id:blockId,
        type:kind,
        text:value,
        has_text:!!value,
        has_value:hasValue,
        has_media:hasMedia,
        has_control:hasControl,
        is_empty:!value&&!hasMedia&&!hasControl
      });
      if(result.length>=60) break;
    }
    return result;
  }

  var G=grids(), gn=G.map(function(g){return g.node;});
  var spec={
    grids:G.map(function(g){return {id:g.id,columns:g.columns,rows:g.rows,est:g.est};}),
    forms:forms(),
    buttons:buttons(gn),
    visual_blocks:visualBlocks(gn)
  };
  var L=["# 화면 스펙 (렌더된 DOM에서 추출 — worklog STEP 0용)","",
         "- 블록 요약: 그리드 "+spec.grids.length+" · 입력영역 "+spec.forms.length+" · 버튼 "+spec.buttons.length+" · 시각블록 "+spec.visual_blocks.length,""];
  if(spec.grids.length){
    L.push("## 그리드 (표) — 각 그리드는 Grid+Dataset+더미행으로 구현 (빈 Div 금지)");
    spec.grids.forEach(function(g,i){
      L.push("\n### 그리드 "+(i+1)+": `"+g.id+"`  (본문 약 "+g.est+"행)");
      L.push("- 컬럼("+g.columns.length+"): "+(g.columns.join(", ")||"⟨헤더 미검출 — 확인 필요⟩"));
      if(g.rows.length){ L.push("- 샘플 행:"); g.rows.forEach(function(r){ L.push("  - "+JSON.stringify(r)); }); }
    });
  }
  if(spec.forms.length){
    L.push("\n## 입력/검색 영역 (div_Search + 입력 컨트롤)");
    spec.forms.forEach(function(f,i){ L.push("- 영역 "+(i+1)+" `"+f.id+"`: "+f.controls.join(", ")); });
  }
  if(spec.buttons.length){ L.push("\n## 버튼/탭 (div_Button 등)"); L.push("- "+spec.buttons.join(", ")); }
  if(spec.visual_blocks.length){
    L.push("\n## 시각 블록 — KPI/Card/Chart/Matrix/Panel");
    spec.visual_blocks.forEach(function(b,i){
      L.push("- "+(i+1)+". `"+b.id+"` type="+b.type+" state="+(b.is_empty?"EMPTY":"filled")+
        " text="+b.has_text+" value="+b.has_value+" media="+b.has_media);
    });
  }
  L.push("\n> ★ 이 스펙을 worklog에 고정한 뒤, 원본 SPA는 컨텍스트에서 뺀다(다시 읽지 말 것).");
  var md=L.join("\n");
  console.log(md);
  try { copy(md); console.log("%c[복사됨] worklog에 붙여넣으세요.","color:green"); } catch(e){}
  window.__screenSpec=spec;
  return md;
})(5);
