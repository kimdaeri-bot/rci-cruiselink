#!/usr/bin/env python3
"""
선박 상세 데이터 정규화 + 페이지 재생성
1. ships-detail.json: images[] 구조 → image 평탄화
2. 영문 descEn → 한국어 descKo 생성 (키워드 기반)
3. guide/ships/ 페이지 전체 재생성
"""
import json, os, re

BASE = "/Users/kim/.openclaw/workspace/cruiselink-v2"
DETAIL_FILE = f"{BASE}/assets/data/ships-detail.json"
SHIPS_DIR = f"{BASE}/guide/ships"

# ── 한국어 설명 생성 (시설명 + 영문 설명 키워드 기반) ──────────────────
KO_TEMPLATES = {
    # 다이닝
    'steakhouse': '정통 스테이크하우스로, 엄선된 최고급 소고기 스테이크와 신선한 해산물을 제공합니다.',
    'sushi': '선상 최고의 스시 레스토랑으로, 신선한 사시미와 롤을 즐길 수 있는 아시안 다이닝 공간입니다.',
    'italian': '이탈리안 정통 요리를 즐길 수 있는 레스토랑으로, 파스타와 피자 등 클래식 메뉴를 선보입니다.',
    'buffet': '다채로운 세계 요리를 뷔페 형식으로 즐길 수 있는 캐주얼 레스토랑입니다.',
    'main dining': '다양한 코스 요리를 즐길 수 있는 메인 다이닝룸으로, 매일 바뀌는 메뉴를 선보입니다.',
    'dining room': '정찬 코스를 즐길 수 있는 메인 레스토랑입니다.',
    'specialty': '독특한 컨셉의 스페셜티 레스토랑으로, 특별한 식사 경험을 제공합니다.',
    'french': '프렌치 퀴진을 선보이는 고급 레스토랑으로, 우아한 분위기에서 다이닝을 즐기세요.',
    'seafood': '신선한 해산물 요리를 전문으로 하는 레스토랑입니다.',
    'asian': '다채로운 아시안 퀴진을 선보이는 레스토랑으로, 동남아부터 일식까지 다양한 메뉴를 즐기세요.',
    'tapas': '스페인 타파스와 지중해 요리를 즐길 수 있는 캐주얼 다이닝 공간입니다.',
    "chef's table": "셰프가 직접 안내하는 프라이빗 다이닝 경험으로, 선상 최고급 미식 여행을 선사합니다.",
    'cafe': '하루 종일 가볍게 즐길 수 있는 카페로, 음료와 간식을 제공합니다.',
    'pizza': '갓 구운 피자와 이탈리안 음식을 즐길 수 있는 캐주얼 공간입니다.',
    'burger': '신선한 패티로 만든 버거와 아메리칸 푸드를 즐길 수 있는 레스토랑입니다.',
    'room service': '객실에서 편안하게 즐기는 룸서비스로, 언제든지 원하는 음식을 주문할 수 있습니다.',
    'bar': '선내 다양한 바 중 하나로, 칵테일과 음료를 즐길 수 있는 공간입니다.',
    'lounge': '편안한 분위기의 라운지에서 음료를 즐기며 여유로운 시간을 보내세요.',
    'pub': '영국 스타일의 퍼브로, 생맥주와 라이브 음악을 즐길 수 있습니다.',
    # 엔터테인먼트
    'theatre': '브로드웨이 스타일의 대형 공연장으로, 세계적 수준의 쇼와 공연을 즐길 수 있습니다.',
    'theater': '브로드웨이 스타일의 대형 공연장으로, 세계적 수준의 쇼와 공연을 즐길 수 있습니다.',
    'casino': '라스베이거스 스타일의 카지노로, 슬롯머신과 테이블 게임을 즐길 수 있습니다.',
    'pool': '선내 수영장으로, 일광욕과 수영을 즐길 수 있는 최고의 휴식 공간입니다.',
    'waterslide': '스릴 넘치는 워터슬라이드로, 온 가족이 함께 즐길 수 있는 수상 어트랙션입니다.',
    'water park': '다양한 워터 어트랙션이 갖춰진 선내 워터파크입니다.',
    'rock climbing': '14미터 높이의 락클라이밍 월로, 초보자부터 전문가까지 즐길 수 있습니다.',
    'flowrider': '서핑 시뮬레이터 플로라이더에서 파도를 타는 짜릿한 경험을 즐겨보세요.',
    'ice skating': '선상 아이스링크에서 무료로 아이스스케이팅을 즐길 수 있습니다.',
    'ice': '선상 아이스링크에서 스케이팅과 아이스쇼를 즐길 수 있습니다.',
    'climbing': '신체활동을 즐길 수 있는 클라이밍 시설입니다.',
    'arcade': '다양한 아케이드 게임을 즐길 수 있는 게임룸입니다.',
    'disco': '신나는 음악과 함께 춤을 즐길 수 있는 디스코장입니다.',
    'nightclub': '밤 문화를 즐길 수 있는 선상 나이트클럽입니다.',
    'shopping': '면세 쇼핑을 즐길 수 있는 선상 쇼핑몰로, 명품 브랜드와 기념품을 구매할 수 있습니다.',
    'library': '독서와 카드 게임을 즐길 수 있는 조용한 공간입니다.',
    'photo': '전문 사진작가가 촬영한 아름다운 사진을 간직하세요.',
    'cinema': '최신 영화를 감상할 수 있는 선상 영화관입니다.',
    'mini golf': '탁 트인 바다를 바라보며 미니 골프를 즐길 수 있습니다.',
    'golf': '바다 전망을 즐기며 골프 퍼팅을 즐길 수 있는 공간입니다.',
    # 스파/피트니스
    'spa': '세계 최고 수준의 선상 스파로, 다양한 마사지와 뷰티 트리트먼트를 받으세요.',
    'fitness': '최첨단 장비를 갖춘 선상 피트니스 센터로, 전문 트레이너의 클래스도 이용할 수 있습니다.',
    'gym': '최신 운동기구가 갖춰진 선상 헬스장으로, 바다 전망을 즐기며 운동하세요.',
    'solarium': '성인 전용 솔라리움에서 조용하고 평화로운 휴식을 즐기세요.',
    'sauna': '사우나와 스팀룸에서 심신의 피로를 풀고 활력을 되찾으세요.',
    'beauty': '전문 뷰티 살롱에서 헤어와 네일 트리트먼트를 받으세요.',
    'thermal': '테라피 효과의 온열 시설에서 몸과 마음의 긴장을 풀어보세요.',
    'whirlpool': '따뜻한 월풀에서 여유로운 시간을 즐기세요.',
    'jogging': '갑판 조깅 트랙에서 신선한 바다 공기를 마시며 달려보세요.',
    'sports': '농구, 배구 등 다양한 스포츠를 즐길 수 있는 스포츠 코트입니다.',
    'tennis': '테니스 코트에서 바다를 바라보며 테니스를 즐길 수 있습니다.',
    # 키즈
    'baby': '전문 보육 스태프가 케어하는 영아 클럽으로, 0-3세 아이들을 위한 프로그램을 제공합니다.',
    'toddler': '유아를 위한 전용 공간으로, 안전하고 즐거운 활동을 제공합니다.',
    'kids club': '전문 스태프가 운영하는 키즈클럽으로, 다양한 활동과 프로그램을 즐길 수 있습니다.',
    'teen': '10대 청소년을 위한 전용 공간으로, 게임과 소셜 활동을 즐길 수 있습니다.',
    'adventure ocean': '수상작 어린이 프로그램으로, 연령별 맞춤 활동을 제공합니다.',
    'splash': '아이들을 위한 물놀이 공간으로, 안전한 워터 어트랙션을 즐길 수 있습니다.',
    'youth': '어린이와 청소년을 위한 전용 클럽으로, 다양한 교육적 활동을 제공합니다.',
    'family': '온 가족이 함께 즐길 수 있는 가족 프로그램과 액티비티를 제공합니다.',
    'nursery': '전문 보육 스태프가 상주하는 영유아 전용 공간입니다.',
    'lego': 'LEGO와 함께하는 창의적인 체험 활동으로, 아이들의 상상력을 키워줍니다.',
    'mini club': '어린이를 위한 미니 클럽으로, 또래 친구들과 다양한 활동을 즐길 수 있습니다.',
    'junior club': '7-11세 어린이를 위한 전용 프로그램을 제공하는 주니어 클럽입니다.',
}

def make_ko_desc(name, desc_en):
    """이름과 영문 설명으로 한국어 설명 생성"""
    name_lower = name.lower()
    desc_lower = (desc_en or '').lower()
    combined = name_lower + ' ' + desc_lower

    # 긴 키워드 우선 (정확도 높임)
    sorted_keys = sorted(KO_TEMPLATES.keys(), key=lambda x: -len(x))
    for kw in sorted_keys:
        if kw in combined:
            return KO_TEMPLATES[kw]

    # 매칭 안 되면 빈 문자열 (숨김)
    return ''

def normalize_image(item):
    """images[] 구조 → image 문자열로 정규화"""
    if 'image' in item:
        return item['image']
    images = item.get('images', [])
    if images and isinstance(images, list) and isinstance(images[0], dict):
        return images[0].get('href', '')
    return ''

def normalize_detail(d):
    """ships-detail 항목 정규화"""
    for section in ['dining', 'entertainment', 'health', 'kids', 'accommodations']:
        items = d.get(section, [])
        new_items = []
        for item in items:
            if isinstance(item, dict):
                img = normalize_image(item)
                name = item.get('name', '')
                desc_en = item.get('descEn', '')
                desc_ko = make_ko_desc(name, desc_en)
                new_items.append({'name': name, 'image': img, 'descKo': desc_ko})
        d[section] = new_items

    # deckplans 정규화
    dps = d.get('deckplans', [])
    new_dps = []
    for dp in dps:
        if isinstance(dp, dict):
            img = normalize_image(dp)
            name = dp.get('name', '')
            new_dps.append({'name': name, 'image': img})
    d['deckplans'] = new_dps
    return d

# ── CSS ─────────────────────────────────────────────────────────────────
EXTRA_CSS = """
    .facility-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:16px 0}
    @media(max-width:768px){.facility-grid{grid-template-columns:repeat(2,1fr)}}
    @media(max-width:480px){.facility-grid{grid-template-columns:1fr}}
    .facility-card{border:1px solid var(--gray-200);border-radius:var(--radius);overflow:hidden;background:#fff}
    .facility-card img{width:100%;height:160px;object-fit:cover;display:block}
    .facility-card .no-img{width:100%;height:160px;background:var(--gray-100);display:flex;align-items:center;justify-content:center;font-size:2rem}
    .facility-info{padding:12px}
    .facility-info h3{font-size:.9rem;font-weight:700;color:var(--navy);margin:0 0 6px}
    .facility-info p{font-size:.82rem;color:var(--gray-700);margin:0;line-height:1.6;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
    .cabin-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0}
    @media(max-width:768px){.cabin-grid{grid-template-columns:repeat(2,1fr)}}
    .cabin-card{border:1px solid var(--gray-200);border-radius:var(--radius);overflow:hidden;background:#fff}
    .cabin-card img{width:100%;height:120px;object-fit:cover;display:block}
    .cabin-card .no-img{width:100%;height:120px;background:var(--gray-100);display:flex;align-items:center;justify-content:center;font-size:1.5rem}
    .cabin-card-name{padding:8px;font-size:.8rem;font-weight:700;color:var(--navy);text-align:center}
    .deckplan-list{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:16px 0}
    @media(max-width:600px){.deckplan-list{grid-template-columns:1fr}}
    .deckplan-item img{width:100%;border-radius:8px;border:1px solid var(--gray-200);display:block}
    .deckplan-item .no-img{width:100%;height:200px;background:var(--gray-100);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:2rem}
    .deckplan-item p{font-size:.82rem;color:var(--gray-600);margin:4px 0 0;text-align:center}
"""

def make_facility_section(section_id, emoji, title_ko, items):
    if not items:
        return ''
    cards = ''
    for item in items:
        name = item.get('name', '')
        img = item.get('image', '')
        desc = item.get('descKo', '')
        if img:
            img_html = f'<img src="{img}" alt="{name}" loading="lazy" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'">\n    <div class="no-img" style="display:none">🚢</div>'
        else:
            img_html = '<div class="no-img">🚢</div>'
        desc_html = f'<p>{desc}</p>' if desc else ''
        cards += f'\n  <div class="facility-card">\n    {img_html}\n    <div class="facility-info"><h3>{name}</h3>{desc_html}</div>\n  </div>'
    return f'\n    <h2 id="{section_id}">{emoji} {title_ko}</h2>\n    <div class="facility-grid">{cards}\n    </div>\n'

def make_cabin_section(accommodations):
    if not accommodations:
        return ''
    cards = ''
    for item in accommodations:
        name = item.get('name', '')
        img = item.get('image', '')
        if img:
            img_html = f'<img src="{img}" alt="{name}" loading="lazy" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'">\n    <div class="no-img" style="display:none">🛏️</div>'
        else:
            img_html = '<div class="no-img">🛏️</div>'
        cards += f'\n  <div class="cabin-card">\n    {img_html}\n    <div class="cabin-card-name">{name}</div>\n  </div>'
    return f'\n    <h2 id="cabins">🛏️ 객실 등급</h2>\n    <div class="cabin-grid">{cards}\n    </div>\n'

def make_deckplan_section(deckplans):
    if not deckplans:
        return ''
    items = ''
    for dp in deckplans:
        name = dp.get('name', '')
        img = dp.get('image', '')
        if img:
            img_html = f'<img src="{img}" alt="{name}" loading="lazy" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'">\n    <div class="no-img" style="display:none">🗺️</div>'
        else:
            img_html = '<div class="no-img">🗺️</div>'
        items += f'\n  <div class="deckplan-item">\n    {img_html}\n    <p>{name}</p>\n  </div>'
    return f'\n    <h2 id="deckplan">📐 덱 플랜</h2>\n    <div class="deckplan-list">{items}\n    </div>\n'

def build_toc_items(detail):
    items = []
    if detail.get('dining'):
        items.append('<li><a href="#dining">🍽️ 다이닝</a></li>')
    if detail.get('entertainment'):
        items.append('<li><a href="#entertainment">🎭 엔터테인먼트</a></li>')
    if detail.get('health'):
        items.append('<li><a href="#health">💆 스파 &amp; 웰니스</a></li>')
    if detail.get('kids'):
        items.append('<li><a href="#kids">👧 키즈 클럽</a></li>')
    if detail.get('accommodations'):
        items.append('<li><a href="#cabins">🛏️ 객실 등급</a></li>')
    if detail.get('deckplans'):
        items.append('<li><a href="#deckplan">📐 덱 플랜</a></li>')
    return '\n        '.join(items)

def rebuild_page(html_path, detail):
    """기존 페이지에서 facility 섹션 제거 후 재삽입"""
    with open(html_path, encoding='utf-8') as f:
        html = f.read()

    # 기존 facility CSS 제거
    html = re.sub(r'\n    \.facility-grid\{.*?\.deckplan-item p\{[^}]+\}\n', '\n', html, flags=re.DOTALL)

    # 기존 facility/cabin/deckplan 섹션 제거 (h2#dining 부터 h2#book 직전까지)
    html = re.sub(
        r'\n    <h2 id="dining">.*?(?=\n    <h2 id="book">)',
        '\n',
        html,
        flags=re.DOTALL
    )

    # 기존 TOC 항목 제거 (dining/entertainment/health/kids/cabins/deckplan)
    html = re.sub(
        r'<li><a href="#(dining|entertainment|health|kids|cabins|deckplan)">[^<]+</a></li>\n\s*',
        '',
        html
    )

    # CSS 추가
    html = html.replace('  </style>', EXTRA_CSS + '  </style>', 1)

    # 섹션 생성 및 삽입
    sections = ''
    sections += make_facility_section('dining', '🍽️', '다이닝', detail.get('dining', []))
    sections += make_facility_section('entertainment', '🎭', '엔터테인먼트', detail.get('entertainment', []))
    sections += make_facility_section('health', '💆', '스파 &amp; 웰니스', detail.get('health', []))
    sections += make_facility_section('kids', '👧', '키즈 클럽', detail.get('kids', []))
    sections += make_cabin_section(detail.get('accommodations', []))
    sections += make_deckplan_section(detail.get('deckplans', []))

    html = html.replace('\n    <h2 id="book">예약 안내</h2>', sections + '\n    <h2 id="book">예약 안내</h2>', 1)

    # TOC 재삽입
    toc_items = build_toc_items(detail)
    if toc_items:
        html = html.replace(
            '<li><a href="#book">예약 안내</a></li>',
            toc_items + '\n        <li><a href="#book">예약 안내</a></li>',
            1
        )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


# ── 메인 실행 ───────────────────────────────────────────────────────────
print("Loading ships-detail.json...")
with open(DETAIL_FILE, encoding='utf-8') as f:
    data = json.load(f)

print(f"Normalizing {len(data)} ships...")
normalized = []
for d in data:
    normalized.append(normalize_detail(d))

# 저장
with open(DETAIL_FILE, 'w', encoding='utf-8') as f:
    json.dump(normalized, f, ensure_ascii=False, indent=2)
print("ships-detail.json saved.")

# 페이지 재생성
detail_map = {d['slug']: d for d in normalized}
all_slugs = [
    s for s in os.listdir(SHIPS_DIR)
    if os.path.isdir(os.path.join(SHIPS_DIR, s))
]

updated = 0
skipped = 0
for slug in sorted(all_slugs):
    html_path = os.path.join(SHIPS_DIR, slug, 'index.html')
    if not os.path.exists(html_path):
        continue
    if slug not in detail_map:
        skipped += 1
        continue
    try:
        rebuild_page(html_path, detail_map[slug])
        updated += 1
        print(f"  ✓ {slug}")
    except Exception as e:
        print(f"  ✗ {slug}: {e}")

print(f"\nDone: {updated} updated, {skipped} skipped")
print("SCRIPT DONE")
