#!/usr/bin/env python3
"""
각 크루즈 상품별 OG 태그 정적 HTML 생성 → /c/[ref].html
카카오톡 크롤러가 JS 없이도 제목/이미지 읽을 수 있게 함
"""

import json
import glob
import os

BASE_URL = "https://www.cruiselink.co.kr"
DATA_DIR = os.path.join(os.path.dirname(__file__), "../assets/data")
OUT_DIR  = os.path.join(os.path.dirname(__file__), "../c")

os.makedirs(OUT_DIR, exist_ok=True)

TEMPLATE = """<!DOCTYPE html><html lang="ko"><head>
<meta charset="UTF-8">
<title>{title} - 크루즈링크</title>
<meta property="og:type" content="website">
<meta property="og:site_name" content="크루즈링크">
<meta property="og:title" content="{title} - 크루즈링크">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{image}">
<meta property="og:url" content="{BASE_URL}/c/{ref}.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} - 크루즈링크">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{image}">
<meta http-equiv="refresh" content="0;url={BASE_URL}/cruise-view.html?ref={ref}">
<link rel="canonical" href="{BASE_URL}/cruise-view.html?ref={ref}">
</head><body>
<script>location.replace('{BASE_URL}/cruise-view.html?ref={ref}');</script>
<p><a href="{BASE_URL}/cruise-view.html?ref={ref}">{title} 상세 보기</a></p>
</body></html>"""

def make_desc(c):
    parts = []
    nights = c.get("nights")
    ship   = c.get("shipTitle","")
    route  = c.get("portRoute","")
    price  = c.get("priceInside") or c.get("priceOutside") or c.get("priceBalcony")
    currency = c.get("currency","USD")
    if ship:   parts.append(ship)
    if nights: parts.append(f"{nights}박")
    if route:  parts.append(route[:40])
    if price:  parts.append(f"{currency} {price:,}~")
    return " | ".join(parts) or "크루즈링크에서 최적의 크루즈 여행을 찾아보세요."

def make_title(c):
    t = c.get("title","")
    if not t:
        nights = c.get("nights","")
        dest   = c.get("destination","")
        ship   = c.get("shipTitle","")
        t = f"{ship} {nights}박 크루즈" if ship else f"{dest} {nights}박 크루즈"
    return t.strip()

def make_image(c):
    img = c.get("image","")
    if img: return img
    return f"{BASE_URL}/assets/images/og-image.jpg"

count = 0
skipped = 0

for filepath in sorted(glob.glob(os.path.join(DATA_DIR, "cruises-*.json"))):
    if "manifest" in filepath or "mini" in filepath:
        continue
    with open(filepath, encoding="utf-8") as f:
        cruises = json.load(f)

    for c in cruises:
        ref = c.get("ref","").strip()
        if not ref:
            skipped += 1
            continue

        title = make_title(c)
        desc  = make_desc(c)
        image = make_image(c)

        html = TEMPLATE.format(
            title=title.replace('"','&quot;'),
            desc=desc.replace('"','&quot;'),
            image=image,
            ref=ref,
            BASE_URL=BASE_URL
        )

        out_path = os.path.join(OUT_DIR, f"{ref}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1

print(f"✅ 생성 완료: {count}개 / 건너뜀: {skipped}개")
print(f"📂 출력 경로: {OUT_DIR}")
