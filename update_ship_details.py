#!/usr/bin/env python3
"""
선박 상세 페이지 업데이트 스크립트
ships-detail.json의 데이터를 사용하여 선박 HTML 페이지에 다이닝/엔터테인먼트/스파/키즈/덱플랜/객실 섹션 추가
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

# 경로 설정
BASE_DIR = Path(__file__).parent
SHIPS_DATA_PATH = BASE_DIR / "assets/data/ships-detail.json"
SHIPS_HTML_DIR = BASE_DIR / "guide/ships"

# CSS 추가
FACILITY_CSS = """
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
.deckplan-item p{font-size:.82rem;color:var(--gray-600);margin:4px 0 0;text-align:center}"""


def truncate_text(text: str, max_length: int = 150) -> str:
    """텍스트를 지정된 길이로 자르기"""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'


def generate_facility_card(item: Dict) -> str:
    """시설 카드 HTML 생성"""
    name = item.get('name', '').strip()
    description = truncate_text(item.get('description', '').strip())
    image_url = item.get('image', '').strip()

    if not name:
        return ''

    return f"""  <div class="facility-card">
    <img src="{image_url}" alt="{name}" loading="lazy" onerror="this.style.display='none'">
    <div class="facility-info">
      <h3>{name}</h3>
      <p>{description}</p>
    </div>
  </div>"""


def generate_cabin_card(item: Dict) -> str:
    """객실 카드 HTML 생성"""
    name = item.get('name', '').strip()
    image_url = item.get('image', '').strip()

    if not name:
        return ''

    return f"""  <div class="cabin-card">
    <img src="{image_url}" alt="{name}" loading="lazy" onerror="this.style.display='none'">
    <div class="cabin-card-name">{name}</div>
  </div>"""


def generate_deckplan_item(item: Dict) -> str:
    """덱플랜 아이템 HTML 생성"""
    name = item.get('name', '').strip()
    image_url = item.get('image', '').strip()

    if not image_url:
        return ''

    return f"""  <div class="deckplan-item">
    <img src="{image_url}" alt="{name}" loading="lazy">
    <p>{name}</p>
  </div>"""


def generate_sections_html(ship_data: Dict) -> str:
    """선박 상세 섹션 HTML 생성"""
    sections = []

    # 1. 선박 소개 (introductionEn을 한국어로 번역 필요 - 일단 영문 그대로)
    intro_en = ship_data.get('introductionEn', '').strip()
    if intro_en:
        # 간단한 번역 로직 (실제로는 번역 API 사용 권장)
        intro_text = intro_en  # TODO: 한국어 번역

    # 2. 다이닝 섹션
    dining = ship_data.get('dining', [])
    if dining:
        dining_intro = ship_data.get('diningIntroEn', '').strip()
        cards = '\n'.join([generate_facility_card(item) for item in dining if generate_facility_card(item)])
        if cards:
            sections.append(f"""
<h2 id="dining">🍽️ 다이닝</h2>
<p>{dining_intro if dining_intro else '선내 다양한 레스토랑과 다이닝 시설을 만나보세요.'}</p>
<div class="facility-grid">
{cards}
</div>""")

    # 3. 엔터테인먼트 섹션
    entertainment = ship_data.get('entertainment', [])
    if entertainment:
        ent_intro = ship_data.get('entertainmentIntroEn', '').strip()
        cards = '\n'.join([generate_facility_card(item) for item in entertainment if generate_facility_card(item)])
        if cards:
            sections.append(f"""
<h2 id="entertainment">🎭 엔터테인먼트</h2>
<p>{ent_intro if ent_intro else '다양한 공연과 엔터테인먼트를 즐겨보세요.'}</p>
<div class="facility-grid">
{cards}
</div>""")

    # 4. 스파 & 웰니스 섹션
    health = ship_data.get('health', [])
    if health:
        health_intro = ship_data.get('healthIntroEn', '').strip()
        cards = '\n'.join([generate_facility_card(item) for item in health if generate_facility_card(item)])
        if cards:
            sections.append(f"""
<h2 id="health">💆 스파 & 웰니스</h2>
<p>{health_intro if health_intro else '프리미엄 스파와 웰니스 시설에서 휴식을 취하세요.'}</p>
<div class="facility-grid">
{cards}
</div>""")

    # 5. 키즈 클럽 섹션
    kids = ship_data.get('kids', [])
    if kids:
        kids_intro = ship_data.get('kidsIntroEn', '').strip()
        cards = '\n'.join([generate_facility_card(item) for item in kids if generate_facility_card(item)])
        if cards:
            sections.append(f"""
<h2 id="kids">👧 키즈 클럽</h2>
<p>{kids_intro if kids_intro else '어린이를 위한 다양한 프로그램과 시설이 준비되어 있습니다.'}</p>
<div class="facility-grid">
{cards}
</div>""")

    # 6. 객실 등급 섹션
    accommodations = ship_data.get('accommodations', [])
    if accommodations:
        acc_intro = ship_data.get('accommodationIntroEn', '').strip()
        cards = '\n'.join([generate_cabin_card(item) for item in accommodations if generate_cabin_card(item)])
        if cards:
            sections.append(f"""
<h2 id="cabins">🛏️ 객실 등급</h2>
<p>{acc_intro if acc_intro else '다양한 객실 타입 중 원하는 등급을 선택하세요.'}</p>
<div class="cabin-grid">
{cards}
</div>""")

    # 7. 덱 플랜 섹션
    deckplans = ship_data.get('deckplans', [])
    if deckplans:
        items = '\n'.join([generate_deckplan_item(item) for item in deckplans if generate_deckplan_item(item)])
        if items:
            sections.append(f"""
<h2 id="deckplan">📐 덱 플랜</h2>
<p>선박의 각 층별 구조와 시설 위치를 확인하세요.</p>
<div class="deckplan-list">
{items}
</div>""")

    return '\n'.join(sections)


def update_toc(html_content: str, has_dining: bool, has_entertainment: bool,
               has_health: bool, has_kids: bool, has_cabins: bool, has_deckplan: bool) -> str:
    """TOC 업데이트"""
    toc_items = []

    if has_dining:
        toc_items.append('<li><a href="#dining">🍽️ 다이닝</a></li>')
    if has_entertainment:
        toc_items.append('<li><a href="#entertainment">🎭 엔터테인먼트</a></li>')
    if has_health:
        toc_items.append('<li><a href="#health">💆 스파 & 웰니스</a></li>')
    if has_kids:
        toc_items.append('<li><a href="#kids">👧 키즈 클럽</a></li>')
    if has_cabins:
        toc_items.append('<li><a href="#cabins">🛏️ 객실 등급</a></li>')
    if has_deckplan:
        toc_items.append('<li><a href="#deckplan">📐 덱 플랜</a></li>')

    if not toc_items:
        return html_content

    # TOC의 <li><a href="#book"> 직전에 삽입
    new_toc = '\n        '.join(toc_items)
    pattern = r'(\s+<li><a href="#book">예약 안내</a></li>)'
    replacement = f'\n        {new_toc}\n        <li><a href="#book">예약 안내</a></li>'

    return re.sub(pattern, replacement, html_content, count=1)


def is_tab_structure(html_content: str) -> bool:
    """탭 구조 페이지인지 확인 (MSC, NCL 등)"""
    return 'ship-tabs' in html_content or 'showTab(' in html_content


def update_ship_page(ship_slug: str, ship_data: Dict) -> bool:
    """선박 페이지 업데이트"""
    html_path = SHIPS_HTML_DIR / ship_slug / "index.html"

    if not html_path.exists():
        print(f"❌ 파일 없음: {ship_slug}")
        return False

    try:
        # HTML 읽기
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 탭 구조 페이지는 스킵 (이미 데이터가 있음)
        if is_tab_structure(html_content):
            print(f"⏭️  탭 구조 (스킵): {ship_slug}")
            return False

        # 이미 업데이트된 경우 스킵
        if 'facility-grid' in html_content and 'id="dining"' in html_content:
            print(f"⏭️  이미 업데이트됨: {ship_slug}")
            return False

        # 섹션 HTML 생성
        sections_html = generate_sections_html(ship_data)

        if not sections_html.strip():
            print(f"⚠️  데이터 없음: {ship_slug}")
            return False

        # <h2 id="book"> 직전에 섹션 삽입
        book_pattern = r'(\s*<h2 id="book">예약 안내</h2>)'
        if not re.search(book_pattern, html_content):
            print(f"❌ <h2 id='book'> 없음: {ship_slug}")
            return False

        html_content = re.sub(
            book_pattern,
            f'\n{sections_html}\n\n    <h2 id="book">예약 안내</h2>',
            html_content,
            count=1
        )

        # CSS 추가 (</style> 직전)
        if 'facility-grid' not in html_content:
            css_pattern = r'(\s*</style>)'
            html_content = re.sub(
                css_pattern,
                f'\n    {FACILITY_CSS}\n  </style>',
                html_content,
                count=1
            )

        # TOC 업데이트
        has_sections = {
            'has_dining': bool(ship_data.get('dining')),
            'has_entertainment': bool(ship_data.get('entertainment')),
            'has_health': bool(ship_data.get('health')),
            'has_kids': bool(ship_data.get('kids')),
            'has_cabins': bool(ship_data.get('accommodations')),
            'has_deckplan': bool(ship_data.get('deckplans'))
        }
        html_content = update_toc(html_content, **has_sections)

        # 파일 저장
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ 업데이트 완료: {ship_slug}")
        return True

    except Exception as e:
        print(f"❌ 오류 ({ship_slug}): {e}")
        return False


def main():
    """메인 실행 함수"""
    print("🚢 선박 상세 페이지 업데이트 시작...\n")

    # ships-detail.json 로드
    if not SHIPS_DATA_PATH.exists():
        print(f"❌ 파일 없음: {SHIPS_DATA_PATH}")
        return

    with open(SHIPS_DATA_PATH, 'r', encoding='utf-8') as f:
        ships_data = json.load(f)

    print(f"📊 총 {len(ships_data)}개 선박 데이터 로드\n")

    # 각 선박 페이지 업데이트
    updated_count = 0
    skipped_count = 0
    error_count = 0

    for ship in ships_data:
        slug = ship.get('slug', '').strip()
        if not slug:
            continue

        result = update_ship_page(slug, ship)
        if result:
            updated_count += 1
        elif result is False and os.path.exists(SHIPS_HTML_DIR / slug / "index.html"):
            skipped_count += 1
        else:
            error_count += 1

    print(f"\n{'='*50}")
    print(f"✅ 업데이트 완료: {updated_count}개")
    print(f"⏭️  스킵: {skipped_count}개")
    print(f"❌ 오류: {error_count}개")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
