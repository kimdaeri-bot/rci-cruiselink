#!/usr/bin/env python3
"""기항지 투어 가이드 페이지 생성기"""
import html
from pathlib import Path

BASE = Path(__file__).parent.parent
OUT = BASE / "guide" / "tours"
OUT.mkdir(parents=True, exist_ok=True)

TOURS = {
    "barcelona": {
        "nameKo": "바르셀로나", "country": "스페인", "emoji": "🇪🇸",
        "cover": "https://images.unsplash.com/photo-1523531294919-4bcd7c65e216?w=1200&q=80",
        "port_slug": "barcelona",
        "half": {
            "title": "반일(4~5시간) 추천 코스",
            "steps": [
                ("09:00", "크루즈 터미널 출발", "택시 또는 셔틀버스로 시내 이동 (15~20분)"),
                ("09:30", "사그라다 파밀리아", "가우디의 성당 내·외부 관람 1.5시간. 사전 예매 필수"),
                ("11:00", "카사 바트요 외관", "가우디 대표작 외관 사진 촬영 (내부는 선택)"),
                ("11:30", "그라시아 거리 산책", "바르셀로나 최고급 거리, 카페에서 커피 한 잔"),
                ("12:30", "람블라스 거리", "보케리아 시장에서 하몽·과일 간식"),
                ("13:30", "터미널 복귀", "택시로 20분"),
            ]
        },
        "full": {
            "title": "종일(8~9시간) 추천 코스",
            "steps": [
                ("09:00", "크루즈 터미널 출발", "택시 이동"),
                ("09:30", "사그라다 파밀리아", "내부+탑 관람 2시간"),
                ("11:30", "구엘 공원", "가우디 모자이크 광장, 오션뷰 (택시 15분)"),
                ("13:00", "그라시아 지구 점심", "현지 타파스 레스토랑, €15~25"),
                ("14:30", "카사 바트요·카사 밀라", "가우디 건축물 두 곳 선택 관람"),
                ("16:30", "고딕 지구 골목", "대성당, 바르셀로나 역사의 핵심"),
                ("17:30", "바르셀로네타 해변", "지중해 바다에 발 담그기"),
                ("18:30", "터미널 복귀", "택시 25분"),
            ]
        },
        "tours": [
            ("🏛️", "가우디 건축 투어", "사그라다 파밀리아+구엘 공원+카사 바트요", "€60~90", "4~5시간"),
            ("🚴", "E-바이크 시티 투어", "바르셀로나 주요 명소 자전거 투어", "€35~50", "3시간"),
            ("⛵", "지중해 세일링", "항구 출발 카탈루냐 해안 세일링", "€50~80", "3시간"),
            ("🍷", "카탈루냐 와이너리 투어", "페네데스 와인 산지 방문+시음", "€80~120", "5시간"),
            ("🏙️", "FC 바르셀로나 캄프누", "축구 팬이라면 필수, 투어 또는 경기 관람", "€35~200", "2~3시간"),
        ],
        "tips": [
            "사그라다 파밀리아: 공식 홈페이지 sagradafamilia.org에서 사전 예매 (현장 불가 수준)",
            "교통: 택시 앱 Cabify·Bolt 사용 시 일반 택시보다 저렴",
            "팁 문화: 스페인은 팁 필수 아님, 10% 정도 선택",
            "소매치기: 람블라스·보케리아 시장은 각별히 주의",
            "언어: 카탈루냐어·스페인어 사용, 관광지는 영어 가능",
        ]
    },
    "civitavecchia": {
        "nameKo": "로마 (치비타베키아)", "country": "이탈리아", "emoji": "🇮🇹",
        "cover": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=1200&q=80",
        "port_slug": "civitavecchia",
        "half": {
            "title": "반일(4~5시간) 로마 핵심 코스",
            "steps": [
                ("08:30", "치비타베키아역 출발", "기차 탑승, Roma Termini역까지 약 75분"),
                ("10:00", "콜로세움·포럼 로마눔", "고대 로마 핵심, 입장권 사전 예매 필수 (1.5시간)"),
                ("11:30", "카피톨리나 언덕", "로마 전망+무세이 카피톨리니"),
                ("12:30", "트레비 분수", "동전 던지기+점심 (근처 레스토랑)"),
                ("13:30", "치비타베키아행 기차", "Termini역 출발"),
                ("15:00", "터미널 복귀", ""),
            ]
        },
        "full": {
            "title": "종일(9~10시간) 로마+바티칸 코스",
            "steps": [
                ("07:30", "치비타베키아역 출발", "첫 기차 탑승 (일찍 출발할수록 여유)"),
                ("09:00", "바티칸 박물관·시스티나 성당", "미켈란젤로 천장화, 사전 예매 필수 (2.5시간)"),
                ("11:30", "성 베드로 대성당", "무료 입장, 쿠폴라 전망 추천"),
                ("13:00", "나보나 광장 근처 점심", "카르보나라 피자 필수"),
                ("14:30", "판테온", "2,000년 된 로마 신전, 무료 (예약 권장)"),
                ("15:30", "트레비 분수→스페인 광장", "로마 인증 사진 코스"),
                ("17:00", "치비타베키아행 기차", "Termini역 출발"),
                ("18:30", "터미널 복귀", ""),
            ]
        },
        "tours": [
            ("🏛️", "콜로세움+포럼 가이드 투어", "영어 가이드 포함 2.5시간 심층 투어", "€50~80", "2.5시간"),
            ("⛪", "바티칸 조기 입장 투어", "개관 전 입장, 군중 없는 시스티나 성당", "€80~130", "3시간"),
            ("🍕", "로마 쿠킹 클래스", "파스타·젤라또 직접 만들기", "€70~100", "3시간"),
            ("🛵", "스쿠터 투어", "로마 시내를 스쿠터로 질주 (면허 불필요 사이드카)", "€60~90", "3시간"),
            ("🌙", "야경 투어 (저녁 기항 시)", "트레비·콜로세움 야경 워킹 투어", "€40~60", "2.5시간"),
        ],
        "tips": [
            "콜로세움 기차역: Termini→Colosseo (Metro B선, 2정거장)",
            "바티칸→로마 시내 이동: 도보+Metro A선 이용",
            "로마 3대 파스타: 카르보나라, 카초 에 페페, 아마트리치아나",
            "물: 로마 거리 분수(Nasoni) 물은 수돗물이지만 먹을 수 있음",
            "여름 복장: 교회 입장 시 어깨·무릎 노출 금지 (스카프 준비)",
        ]
    },
    "naples": {
        "nameKo": "나폴리", "country": "이탈리아", "emoji": "🇮🇹",
        "cover": "https://images.unsplash.com/photo-1534113414509-0eec2bfb493f?w=1200&q=80",
        "port_slug": "naples",
        "half": {
            "title": "반일(4~5시간) — 폼페이 집중",
            "steps": [
                ("09:00", "나폴리 항구 출발", "Circumvesuviana 기차 탑승 (나폴리 중앙역 출발)"),
                ("09:50", "폼페이 유적 도착", "유네스코 세계유산 폼페이 입장"),
                ("10:00", "폼페이 유적 탐방", "포럼, 빌라 데이 미스테리, 목욕탕, 창고 (2.5시간)"),
                ("12:30", "폼페이역 출발", "나폴리 귀환"),
                ("13:30", "나폴리 피자", "다 미켈레(Da Michele) 또는 소르비요(Sorbillo)에서 정통 피자"),
                ("14:30", "터미널 복귀", ""),
            ]
        },
        "full": {
            "title": "종일(9시간) — 폼페이+카프리 섬",
            "steps": [
                ("08:00", "카프리 섬 페리 출발", "나폴리 항구→카프리 섬 50분"),
                ("09:00", "카프리 섬 도착", "아나카프리 케이블카+블루 그로토 투어 3시간"),
                ("12:00", "카프리 점심", "해산물 파스타, 카프리 레몬 리몬첼로"),
                ("13:30", "카프리→나폴리 페리", ""),
                ("14:30", "나폴리 시내", "카스텔 누오보, 스파카나폴리 골목"),
                ("16:00", "나폴리 피자", "원조 마르게리타 피자"),
                ("17:00", "터미널 복귀", ""),
            ]
        },
        "tours": [
            ("🌋", "폼페이+베수비오 화산 투어", "폼페이 가이드+화산 트레킹", "€60~90", "6시간"),
            ("🏝️", "카프리 섬 보트 투어", "블루 그로토+섬 일주 스피드보트", "€80~120", "5시간"),
            ("🍋", "소렌토+아말피 해안", "절벽 드라이브+소렌토 레몬 리큐어", "€70~100", "8시간"),
            ("🍕", "나폴리 피자 투어", "3대 피자 가게 맛집 투어+역사 설명", "€40~60", "3시간"),
            ("🎣", "베수비오 와이너리", "화산토 와인 시음+포도밭 투어", "€60~80", "4시간"),
        ],
        "tips": [
            "카프리 블루 그로토: 파도가 높으면 입장 불가 — 날씨 확인 필수",
            "Circumvesuviana 기차: 폼페이까지 €3.5, 1시간 간격 운행",
            "나폴리 피자 맛집: L'Antica Pizzeria da Michele (마르게리타만 판매), Sorbillo",
            "나폴리 시내: 소매치기·오토바이 날치기 조심 — 가방은 앞으로",
            "아말피 해안 미니버스: 좁은 절벽 도로 — 멀미 심한 분 주의",
        ]
    },
    "athens": {
        "nameKo": "아테네", "country": "그리스", "emoji": "🇬🇷",
        "cover": "https://images.unsplash.com/photo-1555993539-1732b0258235?w=1200&q=80",
        "port_slug": "athens",
        "half": {
            "title": "반일(5시간) — 아크로폴리스 집중",
            "steps": [
                ("09:00", "피레우스 항구 출발", "Metro Line 1 → Monastiraki역 하차 (25분)"),
                ("09:30", "아크로폴리스 입장", "파르테논 신전, 에렉테이온, 프로필라이아 관람 (2시간)"),
                ("11:30", "아크로폴리스 박물관", "원본 조각품 전시, 세계 최고 수준 (1시간)"),
                ("12:30", "플라카 지구 점심", "그리스 전통 타베르나 (무사카, 수블라키)"),
                ("13:30", "모나스티라키 시장", "기념품 쇼핑"),
                ("14:30", "Metro로 피레우스 복귀", ""),
            ]
        },
        "full": {
            "title": "종일(9시간) — 아테네 전체 + 케이프 수니온",
            "steps": [
                ("08:30", "피레우스 출발", "Metro 이동"),
                ("09:00", "아크로폴리스+박물관", "3시간 심층 관람"),
                ("12:00", "아테네 국립 고고학 박물관", "세계 최대 그리스 유물, 1시간"),
                ("13:30", "신타그마 광장 점심", "아테네 중심부 레스토랑"),
                ("15:00", "케이프 수니온 버스 투어", "포세이돈 신전+에게해 절경 (왕복 3시간)"),
                ("18:00", "피레우스 복귀", ""),
            ]
        },
        "tours": [
            ("🏛️", "아크로폴리스 공인 가이드 투어", "역사 전문 가이드와 함께 심층 탐방", "€40~60", "3시간"),
            ("🌅", "케이프 수니온 선셋 투어", "포세이돈 신전에서 에게해 일몰", "€50~70", "4시간"),
            ("🚌", "아테네 시티 투어 버스", "홉온홉오프 버스, 주요 명소 순환", "€20~30", "종일"),
            ("⛴️", "사로니크 군도 크루즈", "아이기나·포로스·이드라 섬 당일 크루즈", "€60~80", "9시간"),
            ("🍷", "아테네 푸드 투어", "플라카·케라미코스 지역 길거리 음식", "€50~70", "3시간"),
        ],
        "tips": [
            "복합 입장권(€30): 아크로폴리스+고대 아고라+로마 아고라+케라미코스 등 7개 포함",
            "아크로폴리스 최적 방문 시간: 오전 8~9시 또는 오후 5시 이후 (혼잡 최소)",
            "7~8월 아테네 40도+: 물 2L 이상 필수, 파라솔 챙기기",
            "그리스 음식 추천: 호리아티키(그리스 샐러드), 티로피타(치즈 파이), 루쿠마데스(꿀 도넛)",
            "피레우스→아테네 Metro: 약 €1.5, 지하철 1호선 30분 간격",
        ]
    },
    "santorini": {
        "nameKo": "산토리니", "country": "그리스", "emoji": "🇬🇷",
        "cover": "https://images.unsplash.com/photo-1570077188670-517b7c37d52e?w=1200&q=80",
        "port_slug": "santorini",
        "half": {
            "title": "반일(4~5시간) — 피라+이아 핵심",
            "steps": [
                ("09:00", "텐더 보트 하선", "피라 항구 앞바다 정박 → 텐더 보트 20분"),
                ("09:30", "피라 케이블카 탑승", "절벽 위 피라 시내로 이동 (당나귀 탑승 가능)"),
                ("09:45", "피라 시내 산책", "칼데라 뷰 카페, 사진 촬영"),
                ("10:30", "버스로 이아(Oia) 이동", "피라→이아 버스 30분 (€2.5)"),
                ("11:00", "이아 마을 탐방", "파란 지붕+하얀 벽 사진 명소, 기념품"),
                ("13:00", "피라 복귀+점심", "칼데라 뷰 레스토랑"),
                ("14:00", "텐더 보트 귀환", ""),
            ]
        },
        "full": {
            "title": "종일(8시간) — 섬 전체+화산 투어",
            "steps": [
                ("08:30", "텐더 보트 하선", ""),
                ("09:00", "케이블카→피라 시내", "카페에서 아침"),
                ("10:00", "이아(Oia) 마을", "2시간 자유 탐방, 쇼핑"),
                ("12:00", "피라 복귀+점심", "칼데라 뷰 레스토랑에서 그리스 음식"),
                ("13:30", "화산 보트 투어", "네아 카메니 화산 트레킹+온천 수영 (3시간)"),
                ("16:30", "레드 비치", "화산 지형 독특한 검은 모래 해변"),
                ("17:30", "텐더 보트 귀환", ""),
            ]
        },
        "tours": [
            ("🌅", "칼데라 석양 세일링", "카타마란 세일링+와인+일몰", "€70~100", "4시간"),
            ("🌋", "화산+온천 보트 투어", "화산 트레킹+유황 온천 수영", "€30~50", "3시간"),
            ("🍷", "산토리니 와이너리 투어", "3개 와이너리 방문+시음", "€60~90", "4시간"),
            ("🏄", "ATV 섬 일주", "ATV 렌트로 산토리니 주요 포인트 탐방", "€30~50", "3~4시간"),
            ("📸", "포토 투어", "이아·이메로비글리 인스타 명소 전문 촬영", "€80~120", "2시간"),
        ],
        "tips": [
            "텐더 보트: 크루즈 성수기 하선 대기 1시간 가능 — 조기 번호표 확보 필수",
            "피라↔이아 버스: €2.5, 30분 간격 / 택시 €15~20",
            "여름 산토리니는 세계 최고 혼잡 — 이아는 오전 9시 이전 방문 권장",
            "선셋 뷰: 이아 마을 서쪽 언덕 (유료 레스토랑 없어도 길가에서 볼 수 있음)",
            "식수 비쌈 (산 위 섬) — 물은 항구에서 구매 후 올라가기",
        ]
    },
    "dubrovnik": {
        "nameKo": "두브로브니크", "country": "크로아티아", "emoji": "🇭🇷",
        "cover": "https://images.unsplash.com/photo-1539650116574-75c0c6d83f0c?w=1200&q=80",
        "port_slug": "dubrovnik",
        "half": {
            "title": "반일(4시간) — 구시가지 성벽",
            "steps": [
                ("09:00", "크루즈 터미널 출발", "버스 1A/1B번 → 필레 게이트 (10분)"),
                ("09:20", "구시가지 필레 게이트 입장", ""),
                ("09:30", "성벽 투어", "2km 성벽 위 걷기, 아드리아해+오렌지 지붕 전망 (2시간)"),
                ("11:30", "플라자 거리 산책", "구시가지 중심 대리석 거리"),
                ("12:00", "골목 레스토랑 점심", "해산물+크로아티아 와인"),
                ("13:00", "터미널 복귀", "버스 10분"),
            ]
        },
        "full": {
            "title": "종일(8시간) — 성벽+왕좌의게임+로크룸 섬",
            "steps": [
                ("08:30", "크루즈 터미널 출발", "혼잡 피해 일찍 출발"),
                ("09:00", "성벽 투어", "오전 일찍 혼잡 최소 (2시간)"),
                ("11:00", "왕좌의 게임 촬영지 투어", "킹스랜딩 명소 도보 투어 (가이드 권장)"),
                ("12:30", "점심", "구시가지 내 해산물 레스토랑"),
                ("14:00", "로크룸 섬 페리", "자연보호구역 섬, 수영+공작새 (왕복 €20)"),
                ("16:00", "구시가지 복귀+쇼핑", "라벤더 제품, 크로아티아 와인"),
                ("17:30", "터미널 복귀", ""),
            ]
        },
        "tours": [
            ("⚔️", "왕좌의 게임 투어", "킹스랜딩 촬영지 전문 가이드 투어", "€30~50", "2시간"),
            ("🚡", "스르지 산 케이블카+전망", "두브로브니크 전경 파노라마", "€20~30", "1시간"),
            ("⛵", "로크룸 섬+블루 케이브 보트", "인근 섬과 동굴 탐험", "€60~90", "4시간"),
            ("🏄", "카약 구시가지 투어", "바다에서 성벽 바라보는 카약", "€50~70", "3시간"),
            ("🍷", "펠레샤츠 와인 투어", "크로아티아 최고 와인 산지 방문", "€80~120", "6시간"),
        ],
        "tips": [
            "성벽 입장료: €35 (단독), 두브로브니크 카드 구매 시 할인",
            "여름 7~8월은 하루 수만 명 방문 — 오전 8시 전 성벽 입장 권장",
            "구시가지 내 레스토랑 가격 비쌈 — 성벽 밖 골목 식당 이용 추천",
            "케이블카: 왕복 €25, 정상에서 두브로브니크 전경 최고",
            "버스 1A/1B: 항구→구시가지, €2.5. 택시 €15~20",
        ]
    },
    "tokyo": {
        "nameKo": "도쿄", "country": "일본", "emoji": "🇯🇵",
        "cover": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1200&q=80",
        "port_slug": "tokyo",
        "half": {
            "title": "반일(5시간) — 아사쿠사+시부야",
            "steps": [
                ("09:00", "요코하마 항구 출발", "JR 게이힌토호쿠선→아키하바라 환승→아사쿠사 (약 1시간)"),
                ("10:00", "아사쿠사 센소지", "도쿄 최고 사원, 나카미세 거리 기념품"),
                ("11:00", "스카이트리 외관+전망", "634m 전망대 (시간 여유 있으면 입장)"),
                ("12:00", "이동+점심", "라멘·스시·덮밥"),
                ("13:00", "시부야 스크램블 교차로", "세계 최대 교차로, 인증 사진"),
                ("13:30", "출발 귀환", "JR으로 요코하마 복귀 1시간"),
            ]
        },
        "full": {
            "title": "종일(10시간) — 도쿄 풀코스",
            "steps": [
                ("08:00", "요코하마 항구 출발", "JR 이동"),
                ("09:00", "아사쿠사+센소지", "전통 도쿄, 1시간"),
                ("10:30", "우에노 공원+박물관", "국립 박물관 or 우에노 동물원"),
                ("12:00", "아키하바라 점심", "애니·전자제품 쇼핑 거리"),
                ("13:30", "하라주쿠+다케시타 거리", "크레페, 패션, 원숭이 굴"),
                ("15:00", "오모테산도", "명품 거리+스타벅스 리저브"),
                ("16:30", "시부야 스크램블+쇼핑", "돈키호테, 시부야 109"),
                ("18:00", "요코하마 복귀", "JR 약 45분"),
            ]
        },
        "tours": [
            ("🍣", "도쿄 스시 오마카세 투어", "築地 시장+스시 셰프 오마카세", "¥15,000~25,000", "3시간"),
            ("🏯", "황궁+아사쿠사 역사 투어", "공인 가이드와 전통 도쿄 탐방", "€50~80", "4시간"),
            ("🌸", "닌자·사무라이 체험", "닌자 의상+표창 던지기 체험", "¥5,000~8,000", "1.5시간"),
            ("🎮", "아키하바라 게임·애니 투어", "전자상가+만화 카페+게임센터", "€30~50", "3시간"),
            ("🍜", "라멘 투어", "이치란·후쿠오카·삿포로 스타일 라멘 비교", "€40~60", "3시간"),
        ],
        "tips": [
            "Suica(스이카) 카드: 편의점에서 충전, JR+지하철+버스+편의점 모두 사용 가능",
            "포켓 와이파이 또는 eSIM 필수 (일본 공항/항구에서 렌트 가능)",
            "도쿄 음식 평균: 라멘 ¥800~1,200, 스시 한 접시 ¥100~300, 편의점 도시락 ¥600",
            "현금 문화: 일본은 아직 현금 사용 많음 — JPY 준비 필수",
            "지하철 막차: 보통 자정~새벽 1시, 크루즈 복귀 시간 고려해 여유 있게",
        ]
    },
    "busan": {
        "nameKo": "부산", "country": "한국", "emoji": "🇰🇷",
        "cover": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=1200&q=80",
        "port_slug": "busan",
        "half": {
            "title": "반일(4시간) — 자갈치+감천",
            "steps": [
                ("09:00", "부산 국제여객터미널 출발", "도보+버스로 자갈치 시장 이동 (10분)"),
                ("09:15", "자갈치 시장", "부산 수산물 시장 구경, 회·해산물 조식"),
                ("10:00", "국제시장", "부산 최대 재래시장, 먹거리 골목"),
                ("11:00", "감천문화마을", "버스로 20분, 알록달록 벽화 마을"),
                ("12:30", "점심", "돼지국밥 또는 밀면 (부산 특식)"),
                ("13:30", "터미널 복귀", ""),
            ]
        },
        "full": {
            "title": "종일(9시간) — 부산 완전 탐방",
            "steps": [
                ("09:00", "터미널 출발", ""),
                ("09:30", "해운대 해수욕장", "지하철 2호선 해운대역, 바다 산책"),
                ("10:30", "동백섬+APEC 하우스", "해운대 옆 섬, 산책로"),
                ("11:30", "광안리 해수욕장", "광안대교 뷰, 해변 카페"),
                ("13:00", "수변 최고 해산물 점심", "기장군 대게·랍스터 or 해운대 회"),
                ("14:30", "용두산 공원+부산타워", "지하철 이동, 시내 전망"),
                ("16:00", "자갈치 시장+국제시장", "장보기·기념품"),
                ("17:30", "터미널 복귀", ""),
            ]
        },
        "tours": [
            ("🐟", "자갈치 시장 먹방 투어", "신선회+해산물 구이+파전+막걸리", "₩30,000~50,000", "2시간"),
            ("🎨", "감천문화마을 포토 투어", "벽화 포인트+인생 사진+로컬 카페", "₩20,000~30,000", "2시간"),
            ("🌊", "해운대+광안리 반나절", "부산 2대 해수욕장+광안대교", "₩40,000~60,000", "4시간"),
            ("🏯", "부산 역사 투어", "임시수도 기념관+유엔기념공원+범어사", "₩50,000~80,000", "5시간"),
            ("🍖", "돼지국밥+밀면 맛집 투어", "부산 2대 소울푸드 투어", "₩30,000~40,000", "2시간"),
        ],
        "tips": [
            "부산 지하철 1일권: ₩5,500, 주요 관광지 모두 연결 (해운대, 남포동, 서면)",
            "자갈치 시장: 오전 일찍 방문 시 가장 신선, 회 시가 협상 가능",
            "감천문화마을 방문 예의: 주거 지역 — 소음 주의, 사진 촬영 시 주민 배려",
            "부산 특산물: 어묵(오뎅), 씨앗 호떡, 납작만두, 동래 파전",
            "택시: 카카오택시 앱 사용 권장 (언어 장벽 최소화)",
        ]
    },
    "jeju": {
        "nameKo": "제주", "country": "한국", "emoji": "🇰🇷",
        "cover": "https://images.unsplash.com/photo-1570194065650-d99fb4ee7745?w=1200&q=80",
        "port_slug": "jeju",
        "half": {
            "title": "반일(4~5시간) — 성산일출봉+협재 해변",
            "steps": [
                ("09:00", "제주 외항 터미널 출발", "택시 or 렌터카로 성산 이동 (40분)"),
                ("09:40", "성산일출봉 입장", "유네스코 세계유산, 정상 전망 (왕복 1시간)"),
                ("11:00", "해녀 공연", "성산 해녀 전시관, 해녀 공연 관람"),
                ("11:30", "협재 해수욕장 이동", "에메랄드 바다 (차로 1시간)"),
                ("12:30", "협재 점심+해변 산책", "해산물 or 제주 흑돼지"),
                ("14:00", "제주 터미널 복귀", ""),
            ]
        },
        "full": {
            "title": "종일(9시간) — 제주 동서 코스",
            "steps": [
                ("08:30", "터미널 출발 (렌터카 필수)", ""),
                ("09:00", "성산일출봉", "일출봉 트레킹+해녀 공연"),
                ("10:30", "만장굴", "세계 최대 용암 동굴 (차로 20분)"),
                ("12:00", "제주시 점심", "제주 흑돼지 or 몸국"),
                ("13:30", "협재 해수욕장", "스노클링, 해변 카페"),
                ("15:00", "한림 공원", "협재 근처 정원+동굴"),
                ("16:30", "제주 시내 기념품", "감귤 초콜릿, 한라봉 주스"),
                ("17:30", "터미널 복귀", ""),
            ]
        },
        "tours": [
            ("🌋", "성산일출봉+만장굴 투어", "제주 유네스코 유산 2개 코스", "₩50,000~80,000", "5시간"),
            ("🏊", "해녀 체험", "해녀 의상 입고 제주 바다 물질 체험", "₩40,000~60,000", "2시간"),
            ("🚲", "E-바이크 해안 투어", "제주 해안도로 전기 자전거 투어", "₩40,000~60,000", "3시간"),
            ("🍊", "감귤 농장 체험", "제주 감귤 따기+시식+포장", "₩20,000~30,000", "1.5시간"),
            ("🚁", "제주 헬기 투어", "한라산+성산+협재 공중 조망", "₩120,000~200,000", "15분"),
        ],
        "tips": [
            "렌터카 필수: 대중교통 배차 간격 길고 커버 범위 제한적",
            "국제면허증 준비 (외국 크루즈 승객): 제주 렌터카 업체 공항·항구에서 운영",
            "기항 시간 짧으면 성산일출봉 단독 집중 추천",
            "제주 음식: 흑돼지 구이, 몸국, 옥돔구이, 해물뚝배기",
            "제주 기념품: 한라봉 초콜릿, 삼다수, 오메기떡, 감귤 화장품",
        ]
    },
    "singapore": {
        "nameKo": "싱가포르", "country": "싱가포르", "emoji": "🇸🇬",
        "cover": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=1200&q=80",
        "port_slug": "singapore",
        "half": {
            "title": "반일(5시간) — 마리나 베이+가든스",
            "steps": [
                ("09:00", "마리나 베이 크루즈 터미널 출발", "택시 또는 MRT"),
                ("09:30", "가든스 바이 더 베이", "슈퍼트리 그로브+플라워돔 (2시간)"),
                ("11:30", "마리나 베이 샌즈 전망대", "Sands SkyPark Observation Deck (비투숙객 SGD 35)"),
                ("12:30", "클락 키 점심", "싱가포르 칠리 크랩 or 호커 센터"),
                ("14:00", "터미널 복귀", ""),
            ]
        },
        "full": {
            "title": "종일(9시간) — 싱가포르 멀티 컬처",
            "steps": [
                ("08:30", "터미널 출발", "MRT 이동"),
                ("09:00", "차이나타운", "불치사, 맥스웰 푸드 센터 조식"),
                ("10:00", "가든스 바이 더 베이", "온실 2개 관람 (2시간)"),
                ("12:00", "마리나 베이 샌즈", "전망대+쇼핑몰 구경"),
                ("13:00", "리틀 인디아", "무스타파 센터, 스리 비라마칼리암만 사원"),
                ("14:30", "센토사 섬", "유니버설 스튜디오 or 실로소 해변"),
                ("17:00", "칠리 크랩 저녁", "점보 씨푸드 or 롱비치"),
                ("18:30", "터미널 복귀", ""),
            ]
        },
        "tours": [
            ("🦁", "싱가포르 시티 투어", "머라이언 공원+마리나 베이+차이나타운", "SGD 50~80", "4시간"),
            ("🌿", "가든스+마리나 베이 투어", "온실 가이드+야경 포함", "SGD 70~100", "4시간"),
            ("🎢", "유니버설 스튜디오", "센토사 섬 테마파크 종일 자유 이용", "SGD 88", "종일"),
            ("🦒", "싱가포르 동물원+나이트 사파리", "야간 사파리 세계 최고 수준", "SGD 50~80", "4시간"),
            ("🦀", "칠리 크랩 쿠킹 클래스", "싱가포르 시그니처 요리 직접 만들기", "SGD 80~120", "3시간"),
        ],
        "tips": [
            "EZ-Link 카드: 편의점에서 SGD 10~15에 구매, MRT·버스 모두 사용",
            "영어 공용어라 외국인도 매우 편리한 여행 환경",
            "껌 반입 금지, 길거리 음식 취식 제한 구역 주의",
            "호커 센터 음식 SGD 4~8 — 현지 최고의 가성비 식사",
            "싱가포르 환율: 1 SGD ≈ KRW 1,000 (2026 기준 대략)",
        ]
    },
    "juneau": {
        "nameKo": "주노 (알래스카)", "country": "미국", "emoji": "🇺🇸",
        "cover": "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1200&q=80",
        "port_slug": "juneau",
        "half": {
            "title": "반일(4시간) — 멘덴홀 빙하",
            "steps": [
                ("09:00", "주노 크루즈 터미널 출발", "다운타운에서 셔틀버스 탑승 (20분)"),
                ("09:30", "멘덴홀 빙하 비지터센터", "전시 관람, 빙하 개요 파악"),
                ("10:00", "빙하 전망 트레일", "Nugget Falls 트레일 (왕복 2.4km, 45분)"),
                ("11:00", "빙하 가까이 접근", "호수 가장자리에서 빙하 촬영"),
                ("11:30", "셔틀로 다운타운 복귀", ""),
                ("12:00", "주노 다운타운", "기념품 쇼핑, 알래스카 킹크랩 점심"),
                ("13:30", "터미널 복귀", ""),
            ]
        },
        "full": {
            "title": "종일(8시간) — 빙하+고래+독수리",
            "steps": [
                ("08:30", "고래 관찰 투어", "스피드보트로 험발 고래 서식지 이동 (3시간)"),
                ("11:30", "다운타운 귀환", "알래스카 킹크랩 점심"),
                ("13:00", "멘덴홀 빙하 셔틀", "빙하 트레킹 (2시간)"),
                ("15:30", "Mount Roberts 트램웨이", "다운타운 바로 옆, 케이블카로 산정 전망 (1시간)"),
                ("17:00", "터미널 복귀", ""),
            ]
        },
        "tours": [
            ("🧊", "빙하 헬기+아이스워킹", "헬기 타고 빙하 착지+트레킹, 크램폰 제공", "USD 300~400", "3시간"),
            ("🐋", "험발 고래 관찰", "조각선으로 고래 서식지 이동, 점프 목격", "USD 120~160", "3시간"),
            ("🎣", "알래스카 연어 낚시", "가이드와 함께 킹새먼 낚시", "USD 200~300", "4시간"),
            ("🚁", "빙하+피요르드 헬기 투어", "주노 빙하 지대 공중 조망", "USD 200~300", "1시간"),
            ("🦅", "독수리+자연 트레킹", "흰머리독수리 관찰+주노 자연 가이드 투어", "USD 80~120", "3시간"),
        ],
        "tips": [
            "멘덴홀 빙하 셔틀: 다운타운 미셀 산 모퉁이 출발, 왕복 USD 18~22",
            "고래 관찰 최적 시기: 6~8월 (고래 이동 시기, 95%+ 목격률)",
            "날씨: 여름에도 10~15도, 비 많음 — 방수 재킷+레이어링 필수",
            "킹크랩 맛집: Tracy's King Crab Shack (주노 다운타운, 현지 최고 맛집)",
            "알래스카 기념품: 연어 훈제, 베리잼, 원주민 공예품",
        ]
    },
}

# ──────────────────────────────────────────
# 투어 페이지 생성
# ──────────────────────────────────────────
CSS = """<style>
    .g-hero{position:relative;height:380px;overflow:hidden;display:flex;align-items:flex-end}
    .g-hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
    .g-hero-overlay{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.75),rgba(0,0,0,.1) 60%)}
    .g-hero-content{position:relative;z-index:1;width:100%;padding:32px 0;color:#fff}
    .breadcrumb{font-size:.82rem;color:rgba(255,255,255,.75);margin-bottom:8px}
    .breadcrumb a{color:rgba(255,255,255,.75);text-decoration:none}
    .g-hero h1{font-size:1.9rem;font-weight:900;margin:0 0 8px}
    .g-hero-meta{display:flex;gap:8px;flex-wrap:wrap;font-size:.83rem;opacity:.9}
    .g-hero-meta span{background:rgba(255,255,255,.15);padding:3px 10px;border-radius:20px;backdrop-filter:blur(4px)}
    .g-layout{display:grid;grid-template-columns:1fr 300px;gap:36px;max-width:1200px;margin:44px auto;padding:0 20px;align-items:start}
    @media(max-width:900px){.g-layout{grid-template-columns:1fr}}
    .g-body h2{font-size:1.25rem;font-weight:900;color:#1a237e;margin:36px 0 14px;padding-bottom:8px;border-bottom:3px solid #ff6f00;display:inline-block}
    .g-body p{color:#616161;line-height:1.9;margin-bottom:12px}
    .g-body ul{padding-left:20px;color:#616161;line-height:2;margin-bottom:12px}
    .timeline{margin:16px 0;border-left:3px solid #ff6f00;padding-left:20px}
    .tl-item{position:relative;margin-bottom:20px}
    .tl-item::before{content:'';position:absolute;left:-26px;top:4px;width:10px;height:10px;background:#ff6f00;border-radius:50%}
    .tl-time{font-size:.78rem;font-weight:700;color:#ff6f00;margin-bottom:2px}
    .tl-title{font-weight:700;color:#1a237e;font-size:.92rem}
    .tl-desc{font-size:.82rem;color:#9e9e9e;margin-top:2px}
    .tour-card{border:1px solid #eeeeee;border-radius:8px;padding:16px;margin-bottom:12px;display:flex;gap:14px;align-items:flex-start}
    .tour-icon{font-size:1.8rem;flex-shrink:0}
    .tour-name{font-weight:700;color:#1a237e;font-size:.95rem}
    .tour-desc{font-size:.83rem;color:#616161;margin-top:3px}
    .tour-meta{display:flex;gap:10px;margin-top:6px;font-size:.8rem}
    .tour-price{background:#fff3e0;color:#e65100;padding:2px 8px;border-radius:10px;font-weight:700}
    .tour-dur{background:#e8f5e9;color:#2e7d32;padding:2px 8px;border-radius:10px}
    .tip-list{background:#fff8e1;border-radius:8px;padding:14px 20px;margin:14px 0}
    .tip-list li{font-size:.87rem;color:#616161;line-height:1.9}
    .sidebar-card{background:#fff;border:1px solid #eeeeee;border-radius:8px;padding:18px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,.1)}
    .sidebar-card h3{font-size:.93rem;font-weight:700;color:#1a237e;margin:0 0 12px;padding-bottom:8px;border-bottom:2px solid #eeeeee}
    .cta-btn{display:block;background:#ff6f00;color:#fff;text-align:center;padding:12px;border-radius:8px;font-weight:700;font-size:.9rem;text-decoration:none;margin-top:8px;transition:background .2s}
    .cta-btn:hover{background:#e65100}
    .cta-btn.navy{background:#1a237e}
    .cta-btn.navy:hover{background:#0d1642}
    h2[id]{scroll-margin-top:80px}
    .g-sidebar{position:sticky;top:80px}
  </style>"""

def make_tour_page(slug, t):
    nameKo = t["nameKo"]; country = t["country"]; emoji = t["emoji"]
    cover = t["cover"]; port_slug = t["port_slug"]
    half = t["half"]; full_ = t["full"]
    tours = t["tours"]; tips = t["tips"]

    def tl(steps):
        return "".join(f"""<div class="tl-item">
          <div class="tl-time">{tm}</div>
          <div class="tl-title">{html.escape(title)}</div>
          {"<div class='tl-desc'>"+html.escape(desc_)+"</div>" if desc_ else ""}
        </div>""" for tm, title, desc_ in steps)

    tour_cards = "".join(f"""<div class="tour-card">
      <div class="tour-icon">{ic}</div>
      <div>
        <div class="tour-name">{html.escape(name)}</div>
        <div class="tour-desc">{html.escape(desc_)}</div>
        <div class="tour-meta">
          <span class="tour-price">💰 {html.escape(price)}</span>
          <span class="tour-dur">⏱ {html.escape(dur)}</span>
        </div>
      </div>
    </div>""" for ic, name, desc_, price, dur in tours)

    tip_items = "".join(f"<li>{html.escape(tip)}</li>" for tip in tips)
    dots = "../../"

    pg_title = f"{nameKo} 크루즈 기항지 투어 추천 2026 | 반일·종일 코스 완벽 가이드 - 크루즈링크"
    desc = f"{nameKo} 크루즈 기항지 투어 완벽 가이드. 반일·종일 추천 코스, 주요 투어 상품, 현지 팁까지 크루즈링크가 정리합니다."
    keywords = f"{nameKo} 크루즈 투어, {nameKo} 기항지 투어, {nameKo} 볼거리, 크루즈 기항지"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(pg_title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta name="keywords" content="{html.escape(keywords)}">
  <link rel="canonical" href="https://www.cruiselink.co.kr/guide/tours/{slug}.html">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="크루즈링크">
  <meta property="og:title" content="{html.escape(pg_title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:image" content="{cover}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap">
  <link rel="stylesheet" href="{dots}assets/css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚢</text></svg>">
  {CSS}
</head>
<body>
<div id="header"></div>
<section class="g-hero">
  <img src="{cover}" alt="{html.escape(nameKo)}" loading="eager">
  <div class="g-hero-overlay"></div>
  <div class="g-hero-content">
    <div class="container">
      <div class="breadcrumb"><a href="{dots}">홈</a> › <a href="../">가이드</a> › <a href="./">기항지 투어</a> › {html.escape(nameKo)}</div>
      <h1>{emoji} {html.escape(nameKo)} 기항지 투어 가이드 2026</h1>
      <div class="g-hero-meta">
        <span>🌍 {html.escape(country)}</span>
        <span>⏱ 반일/종일 코스 수록</span>
        <span>🗺️ 추천 투어 {len(tours)}개</span>
      </div>
    </div>
  </div>
</section>
<div class="g-layout">
  <article class="g-body">
    <h2 id="half">{html.escape(half['title'])}</h2>
    <div class="timeline">{tl(half['steps'])}</div>

    <h2 id="full">{html.escape(full_['title'])}</h2>
    <div class="timeline">{tl(full_['steps'])}</div>

    <h2 id="tours">추천 투어 상품 {len(tours)}개</h2>
    <p>크루즈 선사 공식 투어 외 현지 업체 투어를 이용하면 30~50% 절약할 수 있습니다.</p>
    {tour_cards}

    <h2 id="tips">현지 실전 팁</h2>
    <ul class="tip-list">{tip_items}</ul>

    <h2 id="port">기항지 상세 정보</h2>
    <p>도시 소개, 볼거리, 이동 방법 등 더 자세한 정보는 기항지 정보 페이지를 참고하세요.</p>
    <a href="../ports/{port_slug}.html" style="display:inline-block;background:#1a237e;color:#fff;padding:12px 20px;border-radius:8px;font-weight:700;text-decoration:none;margin-top:4px">{emoji} {html.escape(nameKo)} 기항지 정보 보기 →</a>
  </article>

  <aside class="g-sidebar">
    <div class="sidebar-card">
      <h3>📋 목차</h3>
      <ul style="list-style:none;padding:0;margin:0">
        <li><a href="#half" style="font-size:.84rem;color:#616161;text-decoration:none;padding:4px 8px;display:block;border-radius:4px">반일 추천 코스</a></li>
        <li><a href="#full" style="font-size:.84rem;color:#616161;text-decoration:none;padding:4px 8px;display:block;border-radius:4px">종일 추천 코스</a></li>
        <li><a href="#tours" style="font-size:.84rem;color:#616161;text-decoration:none;padding:4px 8px;display:block;border-radius:4px">추천 투어 {len(tours)}개</a></li>
        <li><a href="#tips" style="font-size:.84rem;color:#616161;text-decoration:none;padding:4px 8px;display:block;border-radius:4px">실전 팁</a></li>
      </ul>
    </div>
    <div class="sidebar-card">
      <h3>🚢 {html.escape(nameKo)} 기항 크루즈</h3>
      <p style="font-size:.82rem;color:#616161;margin-bottom:4px">{html.escape(nameKo)}을 기항하는 크루즈 상품 보기</p>
      <a class="cta-btn" href="{dots}search.html">크루즈 검색</a>
      <a class="cta-btn navy" href="{dots}#inquiry">무료 상담 신청</a>
    </div>
  </aside>
</div>
<div id="footer"></div>
<script src="{dots}assets/data/translations.js"></script>
<script src="{dots}assets/js/api.js"></script>
<script src="{dots}assets/js/components.js"></script>
<script>
  document.getElementById('header').innerHTML = Components.header('{dots}');
  document.getElementById('footer').innerHTML = Components.footer('{dots}');
</script>
</body></html>"""

# 인덱스
def make_tours_index():
    cards = "".join(f"""
    <a href="{slug}.html" style="background:#fff;border:1px solid #eeeeee;border-radius:8px;overflow:hidden;display:block;text-decoration:none;color:inherit;transition:box-shadow .2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,.12)'" onmouseout="this.style.boxShadow=''">
      <img src="{t['cover']}" alt="{html.escape(t['nameKo'])}" style="width:100%;height:140px;object-fit:cover">
      <div style="padding:14px">
        <div style="font-size:1.1rem">{t['emoji']}</div>
        <div style="font-weight:700;color:#1a237e;margin-top:4px">{html.escape(t['nameKo'])}</div>
        <div style="font-size:.8rem;color:#9e9e9e;margin-top:2px">{html.escape(t['country'])} · {len(t['tours'])}개 투어</div>
      </div>
    </a>""" for slug, t in TOURS.items())

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>크루즈 기항지 투어 가이드 | 반일·종일 코스 총정리 - 크루즈링크</title>
  <meta name="description" content="크루즈 기항지별 반일·종일 추천 투어 코스. 바르셀로나, 로마, 도쿄, 부산 등 주요 기항지 투어 완벽 가이드.">
  <link rel="canonical" href="https://www.cruiselink.co.kr/guide/tours/">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap">
  <link rel="stylesheet" href="../../assets/css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚢</text></svg>">
</head>
<body>
<div id="header"></div>
<section style="background:linear-gradient(135deg,#1a237e,#283593);color:#fff;padding:70px 0;text-align:center">
  <div class="container">
    <h1 style="font-size:2rem;font-weight:900;margin:0 0 10px">🗺️ 크루즈 기항지 투어 가이드</h1>
    <p style="opacity:.85;margin:0">기항지별 반일·종일 추천 코스와 현지 투어 정보를 확인하세요</p>
  </div>
</section>
<div class="container" style="padding:44px 20px">
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">
    {cards}
  </div>
</div>
<div id="footer"></div>
<script src="../../assets/data/translations.js"></script>
<script src="../../assets/js/api.js"></script>
<script src="../../assets/js/components.js"></script>
<script>
  document.getElementById('header').innerHTML = Components.header('../../');
  document.getElementById('footer').innerHTML = Components.footer('../../');
</script>
</body></html>"""

print("=== 기항지 투어 가이드 생성 ===")
with open(OUT / "index.html", "w", encoding="utf-8") as f:
    f.write(make_tours_index())
print("✅ guide/tours/index.html")

for slug, t in TOURS.items():
    with open(OUT / f"{slug}.html", "w", encoding="utf-8") as f:
        f.write(make_tour_page(slug, t))
    print(f"  ✅ tours/{slug}.html — {t['nameKo']}")

print(f"\n🎉 투어 페이지 {len(TOURS)+1}개 완료!")
