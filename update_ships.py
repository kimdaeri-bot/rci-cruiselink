#!/usr/bin/env python3
"""선박 상세 페이지 업데이터"""
import json, os, re, time, urllib.request

BASE = "/Users/kim/.openclaw/workspace/cruiselink-v2"
DETAIL_FILE = f"{BASE}/assets/data/ships-detail.json"
SHIPS_DIR = f"{BASE}/guide/ships"
API_BASE = "https://www.widgety.co.uk/api"
API_AUTH = "app_id=fdb0159a2ae2c59f9270ac8e42676e6eb0fb7c36&token=03428626b23f5728f96bb58ff9bcf4bcb04f8ea258b07ed9fa69d8dd94b46b40"

EXTRA_CSS = """
    .facility-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:16px 0}
    @media(max-width:768px){.facility-grid{grid-template-columns:repeat(2,1fr)}}
    @media(max-width:480px){.facility-grid{grid-template-columns:1fr}}
    .facility-card{border:1px solid var(--gray-200);border-radius:var(--radius);overflow:hidden;background:#fff}
    .facility-card img{width:100%;height:160px;object-fit:cover}
    .facility-info{padding:12px}
    .facility-info h3{font-size:.9rem;font-weight:700;color:var(--navy);margin:0 0 6px}
    .facility-info p{font-size:.82rem;color:var(--gray-700);margin:0;line-height:1.6;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
    .cabin-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0}
    @media(max-width:768px){.cabin-grid{grid-template-columns:repeat(2,1fr)}}
    .cabin-card{border:1px solid var(--gray-200);border-radius:var(--radius);overflow:hidden;background:#fff}
    .cabin-card img{width:100%;height:120px;object-fit:cover}
    .cabin-card-name{padding:8px;font-size:.8rem;font-weight:700;color:var(--navy);text-align:center}
    .deckplan-list{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:16px 0}
    @media(max-width:600px){.deckplan-list{grid-template-columns:1fr}}
    .deckplan-item img{width:100%;border-radius:8px;border:1px solid var(--gray-200)}
    .deckplan-item p{font-size:.82rem;color:var(--gray-600);margin:4px 0 0;text-align:center}
"""

def make_facility_section(section_id, emoji, title_ko, items):
    if not items:
        return ""
    cards = ""
    for item in items:
        name = item.get("name", "")
        img = item.get("image", "")
        desc = item.get("descEn", "")
        if desc:
            desc = desc[:200]
        card_desc = f"<p>{desc}</p>" if desc else ""
        img_tag = f'<img src="{img}" alt="{name}" loading="lazy" onerror="this.style.display=\'none\'">' if img else ""
        cards += f"""
  <div class="facility-card">
    {img_tag}
    <div class="facility-info"><h3>{name}</h3>{card_desc}</div>
  </div>"""
    return f"""
    <h2 id="{section_id}">{emoji} {title_ko}</h2>
    <div class="facility-grid">{cards}
    </div>
"""

def make_cabin_section(accommodations):
    if not accommodations:
        return ""
    cards = ""
    for item in accommodations:
        name = item.get("name", "")
        img = item.get("image", "")
        img_tag = f'<img src="{img}" alt="{name}" loading="lazy" onerror="this.style.display=\'none\'">' if img else ""
        cards += f"""
  <div class="cabin-card">
    {img_tag}
    <div class="cabin-card-name">{name}</div>
  </div>"""
    return f"""
    <h2 id="cabins">🛏️ 객실 등급</h2>
    <div class="cabin-grid">{cards}
    </div>
"""

def make_deckplan_section(deckplans):
    if not deckplans:
        return ""
    items = ""
    for item in deckplans:
        name = item.get("name", "")
        img = item.get("image", "")
        items += f"""
  <div class="deckplan-item">
    <img src="{img}" alt="{name}" loading="lazy">
    <p>{name}</p>
  </div>"""
    return f"""
    <h2 id="deckplan">📐 덱 플랜</h2>
    <div class="deckplan-list">{items}
    </div>
"""

def build_toc_items(detail):
    items = []
    if detail.get("dining"):
        items.append('<li><a href="#dining">🍽️ 다이닝</a></li>')
    if detail.get("entertainment"):
        items.append('<li><a href="#entertainment">🎭 엔터테인먼트</a></li>')
    if detail.get("health"):
        items.append('<li><a href="#health">💆 스파 &amp; 웰니스</a></li>')
    if detail.get("kids"):
        items.append('<li><a href="#kids">👧 키즈 클럽</a></li>')
    if detail.get("accommodations"):
        items.append('<li><a href="#cabins">🛏️ 객실 등급</a></li>')
    if detail.get("deckplans"):
        items.append('<li><a href="#deckplan">📐 덱 플랜</a></li>')
    return "\n        ".join(items)

def fetch_ship_detail(slug):
    url = f"{API_BASE}/ships/{slug}.json?{API_AUTH}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            return data
    except Exception as e:
        print(f"  API error for {slug}: {e}")
        return None

def update_page(html_path, detail):
    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    # CSS 이미 추가됐으면 스킵
    if "facility-grid" in html:
        return False

    # CSS 추가 (</style> 직전)
    html = html.replace("  </style>", EXTRA_CSS + "  </style>", 1)

    # 섹션 HTML 생성
    sections = ""
    sections += make_facility_section("dining", "🍽️", "다이닝", detail.get("dining", []))
    sections += make_facility_section("entertainment", "🎭", "엔터테인먼트", detail.get("entertainment", []))
    sections += make_facility_section("health", "💆", "스파 &amp; 웰니스", detail.get("health", []))
    sections += make_facility_section("kids", "👧", "키즈 클럽", detail.get("kids", []))
    sections += make_cabin_section(detail.get("accommodations", []))
    sections += make_deckplan_section(detail.get("deckplans", []))

    # book 섹션 직전에 삽입
    if '\n    <h2 id="book">예약 안내</h2>' in html:
        html = html.replace('\n    <h2 id="book">예약 안내</h2>', sections + '\n    <h2 id="book">예약 안내</h2>', 1)

    # TOC 업데이트
    toc_items = build_toc_items(detail)
    if toc_items:
        html = html.replace(
            '<li><a href="#book">예약 안내</a></li>',
            toc_items + '\n        <li><a href="#book">예약 안내</a></li>',
            1
        )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    return True


# Load existing detail data
with open(DETAIL_FILE) as f:
    details = json.load(f)
detail_map = {d["slug"]: d for d in details}

# Get all ship slugs from guide/ships/
all_slugs = sorted([
    d for d in os.listdir(SHIPS_DIR)
    if os.path.isdir(os.path.join(SHIPS_DIR, d))
])

print(f"Total ship pages: {len(all_slugs)}")
print(f"Existing detail data: {len(detail_map)}")

# Step 1: Update pages with existing data
updated = 0
for slug in all_slugs:
    if slug in detail_map:
        html_path = os.path.join(SHIPS_DIR, slug, "index.html")
        if os.path.exists(html_path):
            if update_page(html_path, detail_map[slug]):
                print(f"  [1] Updated: {slug}")
                updated += 1

print(f"\nStep 1 complete: {updated} pages updated with existing data")

# Step 2: Fetch missing ship data from Widgety API
missing = [s for s in all_slugs if s not in detail_map]
print(f"\nFetching {len(missing)} missing ships from Widgety API...")

new_count = 0
for i, slug in enumerate(missing):
    print(f"  [{i+1}/{len(missing)}] {slug}", flush=True)
    data = fetch_ship_detail(slug)
    if data:
        # Normalize: MSC/NCL style (accommodations/dining/entertainment/health/kids arrays)
        # vs RCI/others style (accomodation_types/dining_options/entertainment_types/etc)
        def norm_items(arr):
            """Convert Widgety list items to {name, image, descEn} format"""
            if not arr or not isinstance(arr, list):
                return []
            result = []
            for item in arr:
                if isinstance(item, dict):
                    images = item.get("images", [])
                    img = images[0]["href"] if images and isinstance(images[0], dict) else ""
                    desc = item.get("description", item.get("descEn", ""))
                    # Strip HTML tags from desc
                    import re as _re
                    desc = _re.sub(r'<[^>]+>', '', desc).strip()[:200]
                    result.append({"name": item.get("name", ""), "image": img, "descEn": desc})
                elif isinstance(item, str):
                    pass  # skip string items
            return result

        # Try both field names
        accommodations = data.get("accommodations") or norm_items(data.get("accomodation_types", []))
        dining = data.get("dining") if isinstance(data.get("dining"), list) else norm_items(data.get("dining_options", []))
        entertainment = data.get("entertainment") if isinstance(data.get("entertainment"), list) else norm_items(data.get("entertainment_types", []))
        health = data.get("health") if isinstance(data.get("health"), list) else norm_items(data.get("health_fitness_types", []))
        kids = data.get("kids") if isinstance(data.get("kids"), list) else norm_items(data.get("kid_teen_types", []))
        deckplans = data.get("deckplans") if isinstance(data.get("deckplans"), list) else norm_items(data.get("deckplans", []))

        detail = {
            "slug": slug,
            "title": data.get("title", data.get("name", slug)),
            "introductionEn": data.get("introduction", ""),
            "accommodations": accommodations,
            "dining": dining,
            "entertainment": entertainment,
            "health": health,
            "kids": kids,
            "deckplans": deckplans,
        }
        detail_map[slug] = detail
        new_count += 1

        html_path = os.path.join(SHIPS_DIR, slug, "index.html")
        if os.path.exists(html_path):
            if update_page(html_path, detail):
                print(f"    -> page updated")

    time.sleep(1.2)

# Save updated detail data
all_details = list(detail_map.values())
with open(DETAIL_FILE, "w", encoding="utf-8") as f:
    json.dump(all_details, f, ensure_ascii=False, indent=2)

print(f"\nStep 2 complete: {new_count} new ships fetched")
print(f"Total detail data: {len(all_details)}")
print("SCRIPT DONE")
