# SPDX-License-Identifier: MPL-2.0
#!/usr/bin/env python3
"""
extract_palette.py — 목업 이미지에서 색을 '코드로' 추출한다 (눈대중 hex 금지).
사용:  python3 extract_palette.py <image> [--colors 14] [--out palette.md]
출력:  콘솔 표 + palette.md + palette.json (검출색 → 색상군 → 용도)
의존:  Pillow  (pip install Pillow --break-system-packages)

왜: 비전 모델은 전처리(리사이즈/대비/그레이스케일/반전)된 이미지를 보므로 원본 hex를
    신뢰할 수 없다. 색은 이 스크립트로 뽑아 그 값을 그대로 쓴다(상태색만 R/Y/G 규약).
"""
import sys, json, colorsys, argparse
from collections import Counter
try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow 필요: pip install Pillow --break-system-packages")

def hexof(rgb): return "#%02x%02x%02x" % rgb

def hue_bucket(r,g,b):
    h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)
    if v>0.93 and s<0.08:  return "무채(흰/밝음)"
    if v<0.18:             return "무채(검정)"
    if s<0.12:             return "무채(회색)"
    hd=h*360
    if hd<15 or hd>=345:   return "빨강"
    if hd<45:              return "주황"
    if hd<70:              return "노랑"
    if hd<170:             return "초록"
    if hd<200:             return "청록"
    if hd<255:             return "파랑"
    if hd<290:             return "보라"
    return "분홍"

# 색상군 → 용도 힌트 (상태색만 R/Y/G 규약, 나머지는 추출값 그대로 사용)
BUCKET_TOKEN = {
 "빨강":"상태색이면 statusRed", "주황":"그대로 사용", "노랑":"상태색이면 statusYellow",
 "초록":"상태색이면 statusGreen", "파랑":"그대로 사용", "청록":"그대로 사용",
 "무채(흰/밝음)":"배경 — 그대로", "무채(회색)":"라인/텍스트 — 그대로", "무채(검정)":"텍스트 — 그대로",
 "보라":"그대로 사용", "분홍":"그대로 사용",
}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("image"); ap.add_argument("--colors",type=int,default=14)
    ap.add_argument("--out",default="palette.md")
    ap.add_argument("--regions",default="",help='소면적 핵심색 정밀샘플: "x,y,w,h=이름; x,y,w,h=이름"')
    a=ap.parse_args()
    im=Image.open(a.image).convert("RGB"); W,H=im.size
    q=im.quantize(colors=a.colors, method=Image.MEDIANCUT).convert("RGB")
    cnt=Counter(q.get_flattened_data() if hasattr(q,"get_flattened_data") else q.getdata())
    total=W*H
    rows=[]
    for c,n in cnt.most_common(a.colors):
        r,g,b=c; s=colorsys.rgb_to_hsv(r/255,g/255,b/255)[1]
        rows.append({"hex":hexof(c),"rgb":list(c),"pct":round(100*n/total,2),
                     "bucket":hue_bucket(r,g,b),"sat":round(s,2),
                     "use_hint":BUCKET_TOKEN.get(hue_bucket(r,g,b),"그대로 사용")})
    # 유채색을 채도*비중 순으로 별도 강조(상태색 판단용)
    chroma=sorted([x for x in rows if not x["bucket"].startswith("무채")],
                  key=lambda x:-(x["sat"]*x["pct"]))
    neutral=[x for x in rows if x["bucket"].startswith("무채")]

    print(f"# 이미지 {a.image}  ({W}x{H})\n")
    print("## 유채색 (★ 눈대중 금지, 아래 hex를 그대로 사용 · 상태색만 R/Y/G)")
    print(f"{'HEX':9} {'RGB':16} {'비중%':>6} {'채도':>5}  {'색상군':10} 용도")
    for x in chroma:
        print(f"{x['hex']:9} {str(tuple(x['rgb'])):16} {x['pct']:6.2f} {x['sat']:5.2f}  {x['bucket']:10} {x['use_hint']}")
    print("\n## 무채색 (배경/텍스트/라인)")
    for x in neutral:
        print(f"{x['hex']:9} {str(tuple(x['rgb'])):16} {x['pct']:6.2f}   {x['bucket']}  {x['use_hint']}")

    # 소면적 핵심 스와치 정밀 샘플 (범례/상태색 등 — 양자화로는 놓치는 것)
    picked=[]
    if a.regions:
        for spec in a.regions.split(";"):
            spec=spec.strip()
            if not spec: continue
            coord,_,label=spec.partition("=")
            x,y,w,h=[int(v) for v in coord.split(",")]
            crop=im.crop((x,y,x+w,y+h))
            cc=Counter(crop.get_flattened_data() if hasattr(crop,"get_flattened_data") else crop.getdata())
            best=None
            for c,_n in cc.most_common(40):
                r,g,b=c
                if r>240 and g>240 and b>240: continue          # 흰 스킵
                if max(r,g,b)-min(r,g,b)<12 and r>200: continue  # 옅은회색 스킵
                best=c; break
            best=best or cc.most_common(1)[0][0]
            picked.append({"label":label.strip() or f"{x},{y}","hex":hexof(best),
                           "rgb":list(best),"bucket":hue_bucket(*best),
                           "use_hint":BUCKET_TOKEN.get(hue_bucket(*best),"그대로 사용")})
        print("\n## 지정 영역 정밀 샘플 (소면적 핵심색)")
        print(f"{'이름':16} {'HEX':9} {'색상군':10} 용도")
        for p in picked:
            print(f"{p['label']:16} {p['hex']:9} {p['bucket']:10} {p['use_hint']}")

    # 파일 출력
    with open("palette.json","w",encoding="utf-8") as f:
        json.dump({"image":a.image,"size":[W,H],"colors":rows,"regions":picked},f,ensure_ascii=False,indent=2)
    with open(a.out,"w",encoding="utf-8") as f:
        f.write(f"# 추출 팔레트 — {a.image} ({W}x{H})\n\n> 코드 추출값. 화면 색은 아래 hex를 그대로 사용(상태색만 R/Y/G). 눈대중 hex 금지.\n\n")
        f.write("## 유채색 (토큰 매핑 대상)\n\n| HEX | 비중% | 색상군 | 용도 |\n|---|---|---|---|\n")
        for x in chroma: f.write(f"| `{x['hex']}` | {x['pct']} | {x['bucket']} | {x['use_hint']} |\n")
        f.write("\n## 무채색 (배경/텍스트/라인)\n\n| HEX | 비중% | 색상군 | 용도 |\n|---|---|---|---|\n")
        for x in neutral: f.write(f"| `{x['hex']}` | {x['pct']} | {x['bucket']} | {x['use_hint']} |\n")
    print(f"\n→ 저장: {a.out}, palette.json")

if __name__=="__main__": main()
