#!/usr/bin/env python3
"""
Widgety API에서 선박 데이터 수집 스크립트
"""

import json
import os
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional

# 경로 설정
BASE_DIR = Path(__file__).parent
SHIPS_DATA_PATH = BASE_DIR / "assets/data/ships-detail.json"
SHIPS_HTML_DIR = BASE_DIR / "guide/ships"

# Widgety API 설정
WIDGETY_BASE_URL = "https://www.widgety.co.uk/api"
WIDGETY_APP_ID = "fdb0159a2ae2c59f9270ac8e42676e6eb0fb7c36"
WIDGETY_TOKEN = "03428626b23f5728f96bb58ff9bcf4bcb04f8ea258b07ed9fa69d8dd94b46b40"


def fetch_ship_data(slug: str) -> Optional[Dict]:
    """Widgety API에서 선박 데이터 가져오기"""
    url = f"{WIDGETY_BASE_URL}/ships/{slug}.json?app_id={WIDGETY_APP_ID}&token={WIDGETY_TOKEN}"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data
            else:
                print(f"  ❌ HTTP {response.status}: {slug}")
                return None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"  ⚠️  404 Not Found: {slug}")
        else:
            print(f"  ❌ HTTP Error {e.code}: {slug}")
        return None
    except urllib.error.URLError as e:
        print(f"  ❌ URL Error: {slug} - {e}")
        return None
    except Exception as e:
        print(f"  ❌ Error: {slug} - {e}")
        return None


def extract_ship_details(api_data: Dict) -> Dict:
    """API 응답에서 필요한 데이터 추출"""
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


def get_all_ship_slugs() -> List[str]:
    """guide/ships/ 폴더에서 모든 선박 slug 가져오기"""
    if not SHIPS_HTML_DIR.exists():
        return []

    slugs = []
    for item in SHIPS_HTML_DIR.iterdir():
        if item.is_dir() and (item / "index.html").exists():
            slugs.append(item.name)

    return sorted(slugs)


def get_existing_slugs() -> List[str]:
    """ships-detail.json에 이미 있는 slug 목록"""
    if not SHIPS_DATA_PATH.exists():
        return []

    with open(SHIPS_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return [ship['slug'] for ship in data]


def main():
    """메인 실행 함수"""
    print("🚢 Widgety API에서 선박 데이터 수집 시작...\n")

    # 기존 데이터 로드
    if SHIPS_DATA_PATH.exists():
        with open(SHIPS_DATA_PATH, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        print(f"📊 기존 데이터: {len(existing_data)}개 선박")
    else:
        existing_data = []
        print("📊 ships-detail.json 파일이 없습니다. 새로 생성합니다.")

    # 모든 선박 slug 가져오기
    all_slugs = get_all_ship_slugs()
    existing_slugs = get_existing_slugs()

    print(f"📊 전체 선박: {len(all_slugs)}개")
    print(f"📊 기존 데이터: {len(existing_slugs)}개")

    # 수집해야 할 선박 목록
    missing_slugs = [slug for slug in all_slugs if slug not in existing_slugs]
    print(f"📊 수집 필요: {len(missing_slugs)}개\n")

    if not missing_slugs:
        print("✅ 모든 선박 데이터가 이미 있습니다.")
        return

    # 샘플만 먼저 테스트 (첫 5개)
    print("🔍 샘플 테스트: 첫 5개 선박만 수집합니다...\n")
    test_slugs = missing_slugs[:5]

    success_count = 0
    fail_count = 0
    new_ships = []

    for i, slug in enumerate(test_slugs, 1):
        print(f"[{i}/{len(test_slugs)}] {slug}")

        # API 호출
        api_data = fetch_ship_data(slug)

        if api_data:
            ship_details = extract_ship_details(api_data)
            new_ships.append(ship_details)
            success_count += 1
            print(f"  ✅ 성공")
        else:
            fail_count += 1

        # Rate limit: 1초 대기
        if i < len(test_slugs):
            time.sleep(1)

    print(f"\n{'='*50}")
    print(f"✅ 성공: {success_count}개")
    print(f"❌ 실패: {fail_count}개")
    print(f"{'='*50}\n")

    if new_ships:
        # 기존 데이터와 병합
        all_ships = existing_data + new_ships

        # ships-detail.json에 저장
        with open(SHIPS_DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(all_ships, f, ensure_ascii=False, indent=2)

        print(f"✅ {len(new_ships)}개 선박 데이터를 ships-detail.json에 추가했습니다.")
        print(f"📊 총 {len(all_ships)}개 선박 데이터")


if __name__ == "__main__":
    main()
