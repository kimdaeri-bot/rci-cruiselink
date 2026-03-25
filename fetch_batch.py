#!/usr/bin/env python3
"""
배치 방식으로 선박 데이터 수집 (진행 상황 출력 개선)
"""

import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

BASE_DIR = Path(__file__).parent
SHIPS_DATA_PATH = BASE_DIR / "assets/data/ships-detail.json"
SHIPS_HTML_DIR = BASE_DIR / "guide/ships"

WIDGETY_BASE_URL = "https://www.widgety.co.uk/api"
WIDGETY_APP_ID = "fdb0159a2ae2c59f9270ac8e42676e6eb0fb7c36"
WIDGETY_TOKEN = "03428626b23f5728f96bb58ff9bcf4bcb04f8ea258b07ed9fa69d8dd94b46b40"


def fetch_ship_data(slug):
    url = f"{WIDGETY_BASE_URL}/ships/{slug}.json?app_id={WIDGETY_APP_ID}&token={WIDGETY_TOKEN}"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            if response.status == 200:
                return json.loads(response.read().decode('utf-8'))
    except:
        pass
    return None


def extract_ship_details(api_data):
    ship = api_data.get('ship', {})
    return {
        'slug': ship.get('slug', ''),
        'title': ship.get('title', ''),
        'introductionEn': ship.get('introduction', ''),
        'diningIntroEn': ship.get('dining_introduction', ''),
        'entertainmentIntroEn': ship.get('entertainment_introduction', ''),
        'healthIntroEn': ship.get('health_introduction', ''),
        'kidsIntroEn': ship.get('kids_introduction', ''),
        'accommodationIntroEn': ship.get('accommodation_introduction', ''),
        'accommodations': ship.get('accommodations', []),
        'dining': ship.get('dining', []),
        'entertainment': ship.get('entertainment', []),
        'health': ship.get('health', []),
        'kids': ship.get('kids', []),
        'deckplans': ship.get('deckplans', [])
    }


def main():
    batch_size = int(sys.argv[1]) if len(sys.argv) > 1 else 50

    # 기존 데이터 로드
    if SHIPS_DATA_PATH.exists():
        with open(SHIPS_DATA_PATH, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # 모든 선박 slug
    all_slugs = []
    for item in SHIPS_HTML_DIR.iterdir():
        if item.is_dir() and (item / "index.html").exists():
            all_slugs.append(item.name)
    all_slugs.sort()

    existing_slugs = [ship['slug'] for ship in existing_data]
    missing_slugs = [slug for slug in all_slugs if slug not in existing_slugs]

    if not missing_slugs:
        print("✅ 모든 선박 데이터가 이미 있습니다.")
        return

    # 배치 크기만큼만 처리
    batch = missing_slugs[:batch_size]
    print(f"🔄 {len(batch)}개 선박 데이터 수집 중... (전체: {len(missing_slugs)}개 남음)\n")

    success = 0
    fail = 0
    new_ships = []

    for i, slug in enumerate(batch, 1):
        sys.stdout.write(f"[{i}/{len(batch)}] {slug}... ")
        sys.stdout.flush()

        api_data = fetch_ship_data(slug)
        if api_data:
            new_ships.append(extract_ship_details(api_data))
            success += 1
            print("✅")
        else:
            fail += 1
            print("❌")

        if i < len(batch):
            time.sleep(0.8)

    print(f"\n✅ 성공: {success}개 | ❌ 실패: {fail}개")

    if new_ships:
        all_ships = existing_data + new_ships
        with open(SHIPS_DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(all_ships, f, ensure_ascii=False, indent=2)
        print(f"💾 저장 완료: 총 {len(all_ships)}개 선박")


if __name__ == "__main__":
    main()
