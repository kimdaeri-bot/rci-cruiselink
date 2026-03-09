#!/usr/bin/env python3
"""크루즈 뉴스 섹션 생성기 — 업계 동향 한국어 오리지널 기사"""
import html
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent
OUT = BASE / "guide" / "news"
OUT.mkdir(parents=True, exist_ok=True)

TODAY = "2026-03-09"

CSS = """<style>
  .g-hero{position:relative;height:340px;overflow:hidden;display:flex;align-items:flex-end}
  .g-hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .g-hero-overlay{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.78),rgba(0,0,0,.1) 60%)}
  .g-hero-content{position:relative;z-index:1;width:100%;padding:32px 0;color:#fff}
  .breadcrumb{font-size:.82rem;color:rgba(255,255,255,.75);margin-bottom:8px}
  .breadcrumb a{color:rgba(255,255,255,.75);text-decoration:none}
  .g-hero h1{font-size:1.8rem;font-weight:900;margin:0 0 8px;line-height:1.3}
  .article-meta{display:flex;gap:10px;flex-wrap:wrap;font-size:.83rem;opacity:.85}
  .article-meta span{background:rgba(255,255,255,.15);padding:3px 10px;border-radius:20px;backdrop-filter:blur(4px)}
  .article-layout{display:grid;grid-template-columns:1fr 300px;gap:36px;max-width:1200px;margin:44px auto;padding:0 20px;align-items:start}
  @media(max-width:900px){.article-layout{grid-template-columns:1fr}}
  .article-body h2{font-size:1.2rem;font-weight:900;color:#1a237e;margin:32px 0 12px}
  .article-body p{color:#424242;line-height:1.95;margin-bottom:16px;font-size:.97rem}
  .article-body ul{padding-left:20px;color:#424242;line-height:2.1;margin-bottom:16px}
  .article-body blockquote{border-left:4px solid #ff6f00;padding:12px 20px;background:#fff8e1;margin:20px 0;color:#616161;font-style:italic;border-radius:0 8px 8px 0}
  .tag-list{display:flex;gap:6px;flex-wrap:wrap;margin:16px 0 24px}
  .tag{display:inline-block;background:#e8eaf6;color:#1a237e;font-size:.78rem;padding:3px 10px;border-radius:10px;text-decoration:none}
  .tag:hover{background:#c5cae9}
  .sidebar-card{background:#fff;border:1px solid #eeeeee;border-radius:8px;padding:18px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,.1)}
  .sidebar-card h3{font-size:.93rem;font-weight:700;color:#1a237e;margin:0 0 12px;padding-bottom:8px;border-bottom:2px solid #eeeeee}
  .news-item{padding:10px 0;border-bottom:1px solid #eeeeee}
  .news-item:last-child{border-bottom:none}
  .news-item a{font-size:.85rem;font-weight:700;color:#1a237e;text-decoration:none;line-height:1.5;display:block}
  .news-item a:hover{text-decoration:underline}
  .news-item .date{font-size:.75rem;color:#9e9e9e;margin-top:2px}
  .cta-btn{display:block;background:#ff6f00;color:#fff;text-align:center;padding:12px;border-radius:8px;font-weight:700;font-size:.9rem;text-decoration:none;margin-top:8px}
  .cta-btn:hover{background:#e65100}
  .cta-btn.navy{background:#1a237e}
  .cta-btn.navy:hover{background:#0d1642}
</style>"""

# ──────────────────────────────────────────
# 뉴스 기사 데이터
# ──────────────────────────────────────────
ARTICLES = [
    {
        "slug": "royal-caribbean-beverage-package-2026",
        "title": "로열 캐리비안, 음료 패키지서 코카콜라 프리스타일 기계 제외",
        "subtitle": "2026년부터 무제한 음료 패키지 개편…승객 반응 엇갈려",
        "date": "2026-03-09",
        "category": "선사 소식",
        "cover": "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=1200&q=80",
        "tags": ["로열캐리비안", "음료패키지", "선사정책"],
        "body": """
<p>로열 캐리비안 인터내셔널(Royal Caribbean International)이 선내 무제한 음료 패키지(Unlimited Beverage Package) 정책을 개편한다고 발표했습니다. 핵심 변경 사항은 <strong>코카콜라 프리스타일(Coca-Cola Freestyle) 자판기 이용이 음료 패키지에서 제외</strong>된다는 것입니다.</p>

<p>코카콜라 프리스타일 기계는 100가지 이상의 음료를 자유롭게 혼합해 즐길 수 있는 셀프 서비스 기계로, 특히 어린이와 청소년 승객들에게 큰 인기를 끌었습니다. 기존에는 무제한 음료 패키지 구매 시 프리스타일 기계도 별도 컵 지급을 통해 자유롭게 이용할 수 있었습니다.</p>

<h2>변경 내용</h2>
<p>이번 개편에 따라 코카콜라 프리스타일 기계는 별도 컵(Daily Cup)을 구매해야만 이용할 수 있습니다. Daily Cup은 1일 이용권으로, 기계에서 원하는 음료를 횟수 제한 없이 이용할 수 있습니다.</p>
<ul>
  <li>무제한 음료 패키지 구매 승객: 프리스타일 기계 별도 구매 필요</li>
  <li>Daily Cup 가격: 약 $8~12/일 (선박 및 시즌에 따라 상이)</li>
  <li>시행 시점: 2026년 신규 예약분부터 순차 적용</li>
</ul>

<h2>승객 반응</h2>
<p>이번 변경에 대해 크루즈 커뮤니티의 반응은 엇갈리고 있습니다. 일부 승객들은 이미 비싼 음료 패키지에서 혜택이 줄어드는 데 불만을 표하고 있으며, 특히 어린이를 동반한 가족 여행객들의 반발이 큽니다. 반면 음주를 하지 않거나 탄산음료를 즐기지 않는 승객들은 상대적으로 큰 영향이 없다는 입장입니다.</p>

<blockquote>로열 캐리비안은 "서비스 품질 향상 및 운영 효율화를 위한 조치"라고 설명했습니다. 하지만 실질적으로는 비용 절감 조치로 해석하는 의견이 지배적입니다.</blockquote>

<h2>크루즈 예약 시 음료 패키지 선택 팁</h2>
<p>이번 변경을 고려할 때, 음료 패키지 구매 여부를 신중하게 따져봐야 합니다.</p>
<ul>
  <li>음주를 즐기는 성인 2인 이상: 무제한 음료 패키지 구매가 대체로 유리</li>
  <li>음주를 하지 않거나 소량 음주: 개별 구매(Pay As You Go)가 더 경제적</li>
  <li>어린이 동반 가족: 프리스타일 기계 별도 비용 감안해 예산 책정 필요</li>
</ul>
<p>크루즈링크 전문 상담원에게 문의하시면 여행 스타일에 맞는 음료 패키지 선택 조언을 드립니다.</p>
"""
    },
    {
        "slug": "luxury-cruise-newbuilds-2026-2028",
        "title": "럭셔리 크루즈 신조선 붐 — 2026~2028년 36척 이상 출항 예정",
        "subtitle": "Explora, Regent, Scenic 등 울트라 럭셔리 선사 경쟁 치열",
        "date": "2026-03-09",
        "category": "업계 동향",
        "cover": "https://images.unsplash.com/photo-1548574505-5e239809ee19?w=1200&q=80",
        "tags": ["럭셔리크루즈", "신조선", "엑스플로라", "리젠트"],
        "body": """
<p>세계 크루즈 업계에서 럭셔리·울트라 럭셔리 부문 신조선(New Build) 붐이 이어지고 있습니다. 업계 전문지 크루즈 인더스트리 뉴스(Cruise Industry News)에 따르면, <strong>2026년부터 2028년까지 럭셔리 크루즈 선박 36척 이상이 신규 취항</strong>할 예정입니다. 이는 팬데믹 이후 럭셔리 여행 수요가 급격히 회복된 데 따른 것으로 분석됩니다.</p>

<h2>주요 럭셔리 선사별 신조선 계획</h2>
<ul>
  <li><strong>Explora Journeys (엑스플로라 저니스)</strong>: Explora I(2023) ~ Explora VI 총 6척. 2026~2027년 Explora III·IV 취항 예정</li>
  <li><strong>Regent Seven Seas Cruises</strong>: Seven Seas Prestige 2026년 취항. 1,000명 이상 최대 규모 리젠트 선박</li>
  <li><strong>Scenic Group</strong>: 2027~2028년 리버 크루즈 선박 3척 추가 발주</li>
  <li><strong>Emerald Cruises</strong>: Emerald Kaia 2026년 3~4월 취항 임박</li>
  <li><strong>Ponant</strong>: 2027년 남극 탐험 전용 선박 추가 발주</li>
</ul>

<h2>럭셔리 크루즈 시장 성장 배경</h2>
<p>럭셔리 크루즈 시장이 급성장하는 이유는 복합적입니다.</p>
<ul>
  <li><strong>팬데믹 후 보복 여행</strong>: 프리미엄 경험에 더 많은 지출을 감수하는 '억눌린 수요' 폭발</li>
  <li><strong>밀레니얼 럭셔리 여행객</strong>: 40대 이하 고소득층의 체험 중심 소비 확대</li>
  <li><strong>All-Inclusive 트렌드</strong>: 숨겨진 비용 없는 완전 포함 상품 선호도 증가</li>
  <li><strong>소형 선박 선호</strong>: 소수 정예 서비스를 위한 700~1,200인 소형 선박 수요 증가</li>
</ul>

<h2>Explora Journeys — 한국 시장 기회</h2>
<p>MSC 그룹의 럭셔리 브랜드 엑스플로라 저니스는 한국 시장에서도 주목받고 있습니다. 전 객실 오션뷰·발코니, 주류 포함 All-Inclusive, 1.3:1 승무원 비율 등 최고 수준의 서비스로 고액 크루즈 여행자를 공략하고 있습니다.</p>
<p>크루즈링크에서는 엑스플로라 저니스 상품에 대한 전담 상담을 제공합니다. <strong>지중해, 북유럽, 카리브해</strong> 노선을 중심으로 2026~2027 시즌 얼리버드 혜택을 누릴 수 있습니다.</p>
"""
    },
    {
        "slug": "msc-musica-brazil-2026-27",
        "title": "MSC 무지카, 브라질 3개 항구 신규 출발지 추가 — 2026~27 시즌",
        "subtitle": "파라나과·이타자이·리우 출발로 남미 노선 확장",
        "date": "2026-03-08",
        "category": "선사 소식",
        "cover": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=1200&q=80",
        "tags": ["MSC크루즈", "MSC무지카", "남미크루즈", "브라질"],
        "body": """
<p>MSC 크루즈(MSC Cruises)가 <strong>MSC 무지카(MSC Musica) 선박의 2026~27 남미 시즌 운항 계획</strong>을 발표했습니다. 이번 시즌에는 기존 산투스(Santos) 외에 <strong>파라나과(Paranaguá), 이타자이(Itajaí), 리우데자네이루(Rio de Janeiro)</strong> 3개 항구를 추가 출발지로 운영합니다.</p>

<h2>MSC 무지카 2026~27 남미 노선 개요</h2>
<ul>
  <li><strong>출발 항구</strong>: 파라나과, 이타자이, 산투스, 리우데자네이루</li>
  <li><strong>주요 기항지</strong>: 부에노스아이레스(아르헨티나), 몬테비데오(우루과이), 피오르도스(칠레), 푼타아레나스</li>
  <li><strong>노선 길이</strong>: 7박~14박 다양한 옵션</li>
  <li><strong>시즌</strong>: 2026년 11월 ~ 2027년 3월 (남미 여름 시즌)</li>
</ul>

<h2>MSC 무지카 선박 소개</h2>
<p>MSC 무지카(MSC Musica)는 2006년 취항한 MSC의 중형 크루즈선입니다. 92,409톤 규모로 최대 3,013명을 수용할 수 있으며, 모나르트(Monarc) 클래스 선박 중 하나입니다. 음악을 테마로 한 인테리어로 유명하며, 지중해·남미·아프리카 등 다양한 노선에서 활약하고 있습니다.</p>

<h2>한국에서 남미 크루즈를 즐기려면</h2>
<p>남미 크루즈는 한국에서 비행기로 브라질·아르헨티나까지 이동 후 승선하는 방식입니다. 비행 거리가 길어 비용과 시간이 많이 소요되지만, 이과수 폭포, 부에노스아이레스 탱고, 파타고니아 빙하 등 유럽이나 아시아와는 전혀 다른 색다른 크루즈 경험을 제공합니다.</p>

<blockquote>크루즈링크에서는 남미 크루즈를 포함한 전 세계 MSC 크루즈 상품을 취급합니다. 항공권 연계 패키지 문의도 가능합니다.</blockquote>
"""
    },
    {
        "slug": "cruise-industry-outlook-2026",
        "title": "2026년 크루즈 업계 전망 — 역대 최대 승객 수 예상",
        "subtitle": "CLIA 발표: 2026년 전 세계 크루즈 승객 4,000만 명 돌파 전망",
        "date": "2026-03-07",
        "category": "업계 동향",
        "cover": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=1200&q=80",
        "tags": ["크루즈업계", "2026전망", "CLIA", "시장동향"],
        "body": """
<p>세계 크루즈 업계 협회 CLIA(Cruise Lines International Association)에 따르면, <strong>2026년 전 세계 크루즈 승객 수가 4,000만 명을 돌파</strong>할 것으로 전망됩니다. 이는 팬데믹 이전 최고 기록인 2019년 2,990만 명을 크게 상회하는 수치입니다.</p>

<h2>시장 성장 동인</h2>
<ul>
  <li><strong>아시아 시장 급성장</strong>: 중국, 일본, 한국 크루즈 수요 폭발적 증가. 중국 크루즈 시장은 2025년 완전 재개 이후 빠르게 회복</li>
  <li><strong>신조선 투입 가속화</strong>: 2026년 취항 예정 신조선 30척+ — 공급 확대가 수요 창출</li>
  <li><strong>MZ 세대 유입</strong>: 30~40대 크루즈 첫 경험자(First Timer) 비율 꾸준히 증가</li>
  <li><strong>짧은 미니 크루즈</strong>: 2~4박 단기 크루즈 수요 증가 — 크루즈 입문 장벽 낮아져</li>
</ul>

<h2>한국 시장 동향</h2>
<p>한국 크루즈 시장도 빠르게 성장하고 있습니다. 부산·인천·제주 기항 크루즈 노선이 매년 증가하고 있으며, MSC 벨리시마의 아시아 시즌 한국 기항이 한국 크루즈 여행자들에게 큰 인기를 끌고 있습니다.</p>
<ul>
  <li>한국 출발 크루즈: 부산 출발 일본·중국 기항 노선 2026년 다수 운항</li>
  <li>한국 인바운드: 외국 크루즈의 부산·제주 기항 증가, 지역 경제 효과</li>
  <li>크루즈 인지도: 과거 '중년층 여행'에서 '전 연령대 프리미엄 여행'으로 이미지 변화</li>
</ul>

<h2>2026년 주목할 크루즈 트렌드</h2>
<ul>
  <li><strong>익스피리언스 이코노미</strong>: 소유보다 경험에 투자하는 소비 트렌드 — 크루즈에 최적</li>
  <li><strong>웰니스 크루즈</strong>: 스파·요가·명상 프로그램 강화한 웰니스 특화 크루즈 증가</li>
  <li><strong>탐험 크루즈</strong>: 남극, 북극, 갈라파고스 등 오지 탐험 크루즈 수요 급증</li>
  <li><strong>그린 크루징</strong>: LNG 연료·탄소 중립 선박 확대 — 환경 친화적 크루즈 선호</li>
</ul>

<blockquote>"크루즈는 더 이상 어르신들의 여행이 아닙니다. 2026년 크루즈 승객 평균 연령은 46세로, 팬데믹 이전 대비 5세 낮아졌습니다." — CLIA 보고서</blockquote>
"""
    },
    {
        "slug": "alaska-cruise-2026-season",
        "title": "2026 알래스카 크루즈 시즌 완벽 가이드 — NCL·Princess·Holland America 주력",
        "subtitle": "5월~9월 성수기, 빙하·야생동물·오로라를 품은 크루즈",
        "date": "2026-03-06",
        "category": "목적지 가이드",
        "cover": "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1200&q=80",
        "tags": ["알래스카크루즈", "NCL", "프린세스크루즈", "빙하"],
        "body": """
<p>알래스카 크루즈는 매년 5월부터 9월까지만 운항하는 계절성 크루즈입니다. <strong>2026년 알래스카 시즌에는 NCL(노르웨지안 크루즈 라인), Princess Cruises(프린세스 크루즈), Holland America Line</strong> 등이 주력 선박을 배치합니다.</p>

<h2>2026 알래스카 시즌 핵심 정보</h2>
<ul>
  <li><strong>시즌</strong>: 2026년 5월 ~ 9월 (9월 하순 종료)</li>
  <li><strong>주요 출발지</strong>: 시애틀, 밴쿠버, 샌프란시스코</li>
  <li><strong>기항지</strong>: 주노, 스캐그웨이, 케치칸, 빅토리아, 시트카</li>
  <li><strong>특별 경험</strong>: 글레이셔 베이(Glacier Bay) 국립공원 크루징 — 빙하 감상</li>
</ul>

<h2>알래스카 크루즈 두 가지 루트</h2>
<p>알래스카 크루즈는 크게 두 가지 루트로 나뉩니다.</p>
<ul>
  <li><strong>라운드트립(Round Trip)</strong>: 시애틀 또는 밴쿠버 출발·도착. 7박~14박. 항공편 왕복 같은 도시</li>
  <li><strong>원웨이(One Way)</strong>: 밴쿠버 출발 → 앵커리지 도착 (또는 반대). 7박. 시작·종착지 다름. 항공편 다른 도시 구매 필요</li>
</ul>

<h2>알래스카 크루즈 하이라이트</h2>
<ul>
  <li><strong>멘덴홀 빙하(주노)</strong>: 접근 가능한 빙하 트레킹, 폭포 포함</li>
  <li><strong>글레이셔 베이</strong>: 선박에서 빙하 붕빙(calving) 목격 가능</li>
  <li><strong>케치칸</strong>: 세계 최대 토템폴 컬렉션, 연어 관찰</li>
  <li><strong>스캐그웨이</strong>: 19세기 골드러시 시대 마을, 화이트패스 철도</li>
  <li><strong>야생동물</strong>: 험발 고래, 범고래, 흑곰, 독수리, 물개 등</li>
</ul>

<h2>한국에서 알래스카 크루즈 예약하기</h2>
<p>알래스카 크루즈는 시애틀 또는 밴쿠버 직항이 있어 한국에서 접근성이 비교적 좋습니다. 인천-시애틀 직항 약 11시간, 인천-밴쿠버 직항 약 10시간입니다. 7박 알래스카 크루즈 기준 1인 $800~ 부터 예약 가능합니다.</p>
<p>크루즈링크에서는 NCL·프린세스·홀랜드 아메리카 알래스카 크루즈 상품을 제공합니다. 항공권 연계 상담도 문의해 주세요.</p>
"""
    },
    {
        "slug": "mediterranean-cruise-2026-guide",
        "title": "2026년 지중해 크루즈 완벽 가이드 — MSC·NCL·로열캐리비안 추천 노선",
        "subtitle": "봄·여름 시즌 인기 노선과 기항지 총정리",
        "date": "2026-03-05",
        "category": "목적지 가이드",
        "cover": "https://images.unsplash.com/photo-1523531294919-4bcd7c65e216?w=1200&q=80",
        "tags": ["지중해크루즈", "MSC크루즈", "바르셀로나", "2026크루즈"],
        "body": """
<p>지중해 크루즈는 전 세계 크루즈 노선 중 가장 인기 있는 목적지입니다. 바르셀로나, 로마, 아테네, 산토리니, 두브로브니크 등 세계 최고의 관광지들을 한 번의 크루즈로 방문할 수 있어 '유럽 일주의 가성비 최고 방법'으로 불립니다. <strong>2026년 지중해 크루즈 시즌(4월~10월)</strong>을 앞두고 주요 노선과 선사를 정리했습니다.</p>

<h2>2026년 지중해 크루즈 주요 선사·노선</h2>

<h2>MSC 크루즈 — 서부 지중해 강자</h2>
<p>MSC는 지중해 최다 선박 운항 선사입니다. 2026년 서부 지중해 주요 노선:</p>
<ul>
  <li><strong>바르셀로나 출발 7박</strong>: 마르세유→제노바→치비타베키아(로마)→메시나→발레타(몰타)→바르셀로나. MSC World Europa, MSC Bellissima 운항</li>
  <li><strong>제노바 출발 7박</strong>: 바르셀로나→팔마 데 마요르카→발렌시아→나폴리→피레우스(아테네). MSC Seashore 운항</li>
</ul>

<h2>로열 캐리비안 — 이스턴·웨스턴 지중해</h2>
<ul>
  <li><strong>바르셀로나 출발 7박</strong>: 마르세유→나폴리→코르푸→두브로브니크→베니스(치오지아)→바르셀로나</li>
  <li><strong>그리스 특화 노선</strong>: 피레우스 출발 에게해 섬 순환 (산토리니·미코노스·로도스)</li>
</ul>

<h2>지중해 크루즈 최적 방문 시기</h2>
<ul>
  <li><strong>4~5월</strong>: 비수기 특가, 혼잡 적음, 날씨 쾌적. 최고 가성비 시즌</li>
  <li><strong>6~8월</strong>: 성수기, 가장 더움(35~40도), 혼잡 최고. 가격 높음</li>
  <li><strong>9~10월</strong>: 성수기 후 특가, 날씨 여전히 좋음. 추천 시즌</li>
</ul>

<h2>지중해 크루즈 한국 출발 방법</h2>
<p>한국에서 지중해 크루즈를 이용하려면 일반적으로 다음 경로를 이용합니다.</p>
<ul>
  <li>인천 → 바르셀로나 직항/경유 (약 13~15시간)</li>
  <li>인천 → 로마 (피우미치노) 직항/경유 (약 12~14시간)</li>
  <li>인천 → 아테네 경유 (약 14~16시간)</li>
</ul>
<p>크루즈링크에서 바르셀로나·로마 출발 지중해 크루즈 상품을 다양하게 제공합니다. <strong>얼리버드 예약 시 최대 30% 할인</strong> 혜택을 받을 수 있으니 지금 바로 문의해 보세요.</p>

<blockquote>지중해 크루즈 인기 1위: 바르셀로나 출발 서부 지중해 7박. 로마·나폴리·발레타(몰타)·바르셀로나를 한 번에 방문합니다.</blockquote>
"""
    },
    {
        "slug": "explora-journeys-korea-2026",
        "title": "엑스플로라 저니스, 2026년 아시아 노선 확대 — 한국 고객 주목",
        "subtitle": "MSC 그룹 울트라 럭셔리 브랜드, 싱가포르·일본·홍콩 기항 노선 강화",
        "date": "2026-03-04",
        "category": "선사 소식",
        "cover": "https://assets.widgety.co.uk/2024/09/25/13/40/26/e94c8bd1-9cff-48a0-9ad6-d4b5de07fd11/Explora I - Exterior - Photo Credit Explora Journeys.jpg",
        "tags": ["엑스플로라저니스", "럭셔리크루즈", "아시아크루즈", "MSC그룹"],
        "body": """
<p>MSC 그룹의 울트라 럭셔리 크루즈 브랜드 <strong>엑스플로라 저니스(Explora Journeys)</strong>가 2026년 아시아 노선을 대폭 확대합니다. 기존 지중해·카리브해 중심에서 벗어나, 싱가포르·일본·홍콩을 포함한 아시아 태평양 노선에 Explora I과 Explora II를 배치할 예정입니다.</p>

<h2>엑스플로라 저니스 아시아 2026 주요 노선</h2>
<ul>
  <li><strong>싱가포르 출발 아시아 일주</strong>: 14박~21박. 홍콩·나가사키·고베·도쿄 기항</li>
  <li><strong>일본 순환</strong>: 도쿄 출발 일본 심층 탐방 코스. 교토(고베 기항)·히로시마·나가사키</li>
  <li><strong>동남아 럭셔리</strong>: 싱가포르→방콕→다낭→호치민→싱가포르</li>
</ul>

<h2>엑스플로라 저니스란?</h2>
<p>엑스플로라 저니스는 2023년 첫 선박(Explora I) 취항 이후 빠르게 럭셔리 시장에서 입지를 굳히고 있는 브랜드입니다. 특징은 다음과 같습니다.</p>
<ul>
  <li><strong>전 객실 오션뷰 + 발코니/테라스</strong>: 인사이드 객실 없음. 최소 스위트급</li>
  <li><strong>레스토랑·바 All-Inclusive</strong>: 9개 레스토랑, 12개 바 모두 포함 (와인·스피릿 포함)</li>
  <li><strong>승객 대 승무원 비율 1.3:1</strong>: 업계 최고 수준 개인 서비스</li>
  <li><strong>소규모 선박</strong>: 약 900명 승객. 혼잡하지 않은 여유로운 크루즈</li>
  <li><strong>기항지 딥다이브</strong>: 일반 크루즈보다 긴 기항 시간(12~18시간), 심층 탐방 가능</li>
</ul>

<h2>한국 고객을 위한 예약 안내</h2>
<p>엑스플로라 저니스는 아직 국내 인지도가 높지 않지만, 럭셔리 여행을 즐기는 한국 고객들에게 최고의 선택이 될 수 있습니다. 특히 <strong>허니문·특별 기념일·버킷리스트 여행</strong>으로 각광받고 있습니다.</p>
<p>크루즈링크는 엑스플로라 저니스 상품을 취급하는 국내 전문 여행사 중 하나입니다. 2026~2027 시즌 아시아 노선은 조기 마감이 예상되므로 사전 상담을 권장합니다.</p>

<blockquote>엑스플로라 저니스 아시아 14박 기준 가격: 1인 USD $6,000~15,000. 전 식사·주류·기항지 투어 일부 포함.</blockquote>
"""
    },
    {
        "slug": "cruise-booking-tips-2026",
        "title": "2026 크루즈 예약 완벽 가이드 — 얼마나 미리? 어떻게 싸게?",
        "subtitle": "얼리버드부터 라스트 미닛까지, 최저가 크루즈 예약 전략",
        "date": "2026-03-03",
        "category": "여행 팁",
        "cover": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1200&q=80",
        "tags": ["크루즈예약", "얼리버드", "크루즈팁", "가격전략"],
        "body": """
<p>크루즈를 처음 예약하는 분들이 가장 많이 묻는 질문이 있습니다. "얼마나 미리 예약해야 하나요?" 그리고 "어떻게 하면 더 싸게 예약할 수 있나요?" 이 두 가지 질문에 대한 답을 크루즈 전문가 관점에서 정리했습니다.</p>

<h2>크루즈 예약 타이밍 전략</h2>

<h2>얼리버드(Early Bird) — 6~12개월 전</h2>
<p>가장 다양한 선택지와 최저 가격을 동시에 잡을 수 있는 최적 타이밍입니다.</p>
<ul>
  <li>원하는 날짜·선박·객실 타입 선택 폭 넓음</li>
  <li>선사별 얼리버드 프로모션: 10~30% 할인 + 무료 음료 패키지, 드링크 크레딧, 객실 업그레이드 등 혜택</li>
  <li>특히 인기 성수기(여름 지중해, 알래스카 시즌)는 6개월 전에도 원하는 객실 매진 가능</li>
</ul>

<h2>준얼리버드 — 3~6개월 전</h2>
<ul>
  <li>얼리버드 혜택은 줄어들지만 여전히 선택 폭 넓음</li>
  <li>대부분의 노선 이 시점에서 예약 활발</li>
  <li>발코니 이상 인기 객실부터 마감 시작</li>
</ul>

<h2>라스트 미닛(Last Minute) — 4~8주 전</h2>
<ul>
  <li>남은 객실 빠른 판매를 위한 파격 할인 가능성</li>
  <li>단, 인기 성수기는 라스트 미닛 오히려 가격 상승</li>
  <li>항공권 연동 일정 잡기 어려울 수 있음</li>
  <li>선택지 제한 — 인사이드 객실만 남는 경우 많음</li>
</ul>

<h2>더 저렴하게 예약하는 방법 5가지</h2>
<ul>
  <li><strong>①  비수기 선택</strong>: 봄(4~5월), 가을(9~10월) 지중해는 여름보다 30~40% 저렴</li>
  <li><strong>② 인사이드 객실 도전</strong>: 창문 없지만 가장 저렴. 크루즈 초보자에게 의외로 추천</li>
  <li><strong>③ 선사 뉴스레터 구독</strong>: MSC, NCL 등 선사 뉴스레터에서 플래시 세일 정보 획득</li>
  <li><strong>④ 전문 여행사 이용</strong>: 직접 예약보다 전문 여행사(크루즈링크 등) 통하면 추가 혜택 가능</li>
  <li><strong>⑤ 그룹 예약</strong>: 8객실 이상 그룹 예약 시 무료 객실 또는 특별 할인 적용</li>
</ul>

<h2>크루즈 예약 전 꼭 확인할 것</h2>
<ul>
  <li>취소 수수료 정책: 출발 90일 이전 취소 vs 이후 취소 환불 조건 확인</li>
  <li>여행자 보험: 크루즈는 일반 여행보험으로 커버 안 되는 경우 있음 — 크루즈 전용 보험 권장</li>
  <li>비자 요건: 기항지별 비자 확인 (중국·미국 ESTA 등)</li>
  <li>추가 비용: 드링크 패키지, 기항지 투어, 그래티티(팁) 등 예산 포함</li>
</ul>

<p>크루즈링크에서는 최신 선사 프로모션 정보를 바탕으로 최적의 크루즈 예약을 도와드립니다. 무료 상담으로 시작해 보세요.</p>
"""
    },
]

# 관련 기사 (사이드바용)
def other_articles(current_slug):
    return [a for a in ARTICLES if a["slug"] != current_slug][:4]

def make_article(a):
    dots = "../../"
    related = other_articles(a["slug"])
    related_html = "".join(f"""<div class="news-item">
      <a href="{r['slug']}.html">{html.escape(r['title'])}</a>
      <div class="date">📅 {r['date']} · {html.escape(r['category'])}</div>
    </div>""" for r in related)

    tags_html = "".join(f'<a href="index.html?tag={t}" class="tag">#{html.escape(t)}</a>' for t in a["tags"])

    pg_title = f"{html.escape(a['title'])} - 크루즈링크 뉴스"
    desc_text = a["subtitle"]

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{pg_title}</title>
  <meta name="description" content="{html.escape(desc_text)}">
  <link rel="canonical" href="https://www.cruiselink.co.kr/guide/news/{a['slug']}.html">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="크루즈링크">
  <meta property="og:title" content="{pg_title}">
  <meta property="og:description" content="{html.escape(desc_text)}">
  <meta property="og:image" content="{a['cover']}">
  <meta property="og:url" content="https://www.cruiselink.co.kr/guide/news/{a['slug']}.html">
  <meta property="article:published_time" content="{a['date']}">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"NewsArticle","headline":{repr(a['title'])},"datePublished":"{a['date']}","image":"{a['cover']}","author":{{"@type":"Organization","name":"크루즈링크"}},"publisher":{{"@type":"Organization","name":"크루즈링크","url":"https://www.cruiselink.co.kr"}}}}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap">
  <link rel="stylesheet" href="{dots}assets/css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚢</text></svg>">
  {CSS}
</head>
<body>
<div id="header"></div>

<section class="g-hero">
  <img src="{a['cover']}" alt="{html.escape(a['title'])}" loading="eager">
  <div class="g-hero-overlay"></div>
  <div class="g-hero-content">
    <div class="container">
      <div class="breadcrumb"><a href="{dots}">홈</a> › <a href="../">가이드</a> › <a href="./">크루즈 뉴스</a></div>
      <h1>{html.escape(a['title'])}</h1>
      <div class="article-meta">
        <span>📅 {a['date']}</span>
        <span>🏷️ {html.escape(a['category'])}</span>
        <span>✍️ 크루즈링크</span>
      </div>
    </div>
  </div>
</section>

<div class="article-layout">
  <article class="article-body">
    <p style="font-size:1.05rem;font-weight:700;color:#424242;border-left:4px solid #ff6f00;padding-left:14px;margin-bottom:24px">{html.escape(a['subtitle'])}</p>
    {a['body']}
    <div class="tag-list">{tags_html}</div>
  </article>

  <aside style="position:sticky;top:80px">
    <div class="sidebar-card">
      <h3>🚢 크루즈 예약 문의</h3>
      <p style="font-size:.82rem;color:#616161;margin-bottom:4px">전문 상담원이 최적 상품을 안내해 드립니다.</p>
      <a class="cta-btn" href="{dots}search.html">상품 검색</a>
      <a class="cta-btn navy" href="{dots}#inquiry">무료 상담 신청</a>
    </div>
    <div class="sidebar-card">
      <h3>📰 다른 뉴스</h3>
      {related_html}
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

def make_news_index():
    cards = "".join(f"""
    <a href="{a['slug']}.html" style="background:#fff;border:1px solid #eeeeee;border-radius:8px;overflow:hidden;display:block;text-decoration:none;color:inherit;transition:box-shadow .2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,.12)'" onmouseout="this.style.boxShadow=''">
      <img src="{a['cover']}" alt="{html.escape(a['title'])}" style="width:100%;height:180px;object-fit:cover" loading="lazy">
      <div style="padding:16px">
        <div style="font-size:.75rem;background:#e8eaf6;color:#1a237e;padding:2px 8px;border-radius:10px;display:inline-block;margin-bottom:8px">{html.escape(a['category'])}</div>
        <div style="font-weight:700;color:#1a237e;font-size:.95rem;line-height:1.5;margin-bottom:6px">{html.escape(a['title'])}</div>
        <div style="font-size:.82rem;color:#9e9e9e">{a['date']}</div>
      </div>
    </a>""" for a in ARTICLES)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>크루즈 뉴스 & 업계 동향 | 크루즈링크</title>
  <meta name="description" content="크루즈 업계 최신 뉴스, 선사 소식, 목적지 가이드, 예약 팁을 크루즈링크가 한국어로 전달합니다.">
  <link rel="canonical" href="https://www.cruiselink.co.kr/guide/news/">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap">
  <link rel="stylesheet" href="../../assets/css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚢</text></svg>">
</head>
<body>
<div id="header"></div>
<section style="background:linear-gradient(135deg,#1a237e,#283593);color:#fff;padding:70px 0;text-align:center">
  <div class="container">
    <h1 style="font-size:2rem;font-weight:900;margin:0 0 10px">📰 크루즈 뉴스 & 업계 동향</h1>
    <p style="opacity:.85;margin:0">크루즈 업계 최신 소식과 전문 정보를 한국어로 제공합니다</p>
  </div>
</section>
<div class="container" style="padding:44px 20px">
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px">{cards}</div>
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

print("=== 크루즈 뉴스 섹션 생성 ===")
with open(OUT / "index.html", "w", encoding="utf-8") as f:
    f.write(make_news_index())
print("✅ guide/news/index.html")
for a in ARTICLES:
    with open(OUT / f"{a['slug']}.html", "w", encoding="utf-8") as f:
        f.write(make_article(a))
    print(f"  ✅ news/{a['slug']}.html")
print(f"\n🎉 뉴스 기사 {len(ARTICLES)+1}개 완료!")
