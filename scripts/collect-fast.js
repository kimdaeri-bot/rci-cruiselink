#!/usr/bin/env node
// 전선사 데이터 수집: Widgety API → ships.json + cruises.json
// Phase 1 = 선박+크루즈 ref (ships.json 7페이지)
// Phase 2 = 크루즈 상세(가격/일정) holidays/dates/{ref}.json
const fs = require('fs');
const path = require('path');

const BASE = 'https://www.widgety.co.uk/api';
const AUTH = 'app_id=fdb0159a2ae2c59f9270ac8e42676e6eb0fb7c36&token=03428626b23f5728f96bb58ff9bcf4bcb04f8ea258b07ed9fa69d8dd94b46b40';
const OUT = path.join(__dirname, '..', 'assets', 'data');
const TODAY = new Date().toISOString().slice(0,10);
const BATCH = 15;
const sleep = ms => new Promise(r => setTimeout(r, ms));

// 스킵할 선사 (데이터 형식 불일치 / 미지원)
const SKIP_OPERATORS = ['Disney Cruise Line'];

async function apiFetch(ep) {
  const url = `${BASE}/${ep}${ep.includes('?')?'&':'?'}${AUTH}`;
  try { const r = await fetch(url); if(!r.ok) return null; return await r.json(); }
  catch { return null; }
}

async function batchFetch(eps) {
  const results = [];
  for(let i=0; i<eps.length; i+=BATCH) {
    const batch = eps.slice(i, i+BATCH);
    const r = await Promise.all(batch.map(apiFetch));
    results.push(...r);
    process.stdout.write(`  ${Math.min(i+BATCH, eps.length)}/${eps.length}\r`);
    if(i+BATCH < eps.length) await sleep(400);
  }
  console.log();
  return results;
}

// ── 선사 매핑 ──
const OPERATOR_MAP = {
  'MSC Cruises':                    { short: 'MSC',       ko: 'MSC 크루즈',         tag: '#MSC크루즈' },
  'Norwegian Cruise Line':          { short: 'NCL',       ko: '노르웨이전 크루즈 라인', tag: '#노르웨이전크루즈' },
  'Royal Caribbean International':  { short: 'RCI',       ko: '로얄 캐리비안',       tag: '#로얄캐리비안' },
  'Celebrity Cruises':              { short: 'Celebrity', ko: '셀러브리티 크루즈',    tag: '#셀러브리티크루즈' },
  'Princess Cruises':               { short: 'Princess',  ko: '프린세스 크루즈',     tag: '#프린세스크루즈' },
  'Carnival Cruise Line':           { short: 'Carnival',  ko: '카니발 크루즈',       tag: '#카니발크루즈' },
  'Holland America Line':           { short: 'HAL',       ko: '홀랜드 아메리카',     tag: '#홀랜드아메리카' },
  'Cunard':                         { short: 'Cunard',    ko: '큐나드',              tag: '#큐나드' },
  'P&O Cruises':                    { short: 'PO',        ko: 'P&O 크루즈',          tag: '#PO크루즈' },
  'Seabourn Cruise Line':           { short: 'Seabourn',  ko: '씨번 크루즈',         tag: '#씨번크루즈' },
  'Silversea Cruises':              { short: 'Silversea', ko: '실버씨 크루즈',       tag: '#실버씨' },
  'Oceania Cruises':                { short: 'Oceania',   ko: '오세아니아 크루즈',   tag: '#오세아니아크루즈' },
  'Regent Seven Seas Cruises':      { short: 'RSSC',      ko: '리젠트 세븐시즈',     tag: '#리젠트세븐시즈' },
};

function getOpInfo(opName) {
  return OPERATOR_MAP[opName] || { short: opName.split(' ')[0], ko: opName, tag: `#${opName.split(' ')[0]}크루즈` };
}

// ── 번역 사전 ──
const portKo = {
  "Tokyo":"도쿄","Yokohama":"요코하마","Kobe":"고베","Osaka":"오사카","Hiroshima":"히로시마",
  "Naha":"나하","Kagoshima":"가고시마","Nagasaki":"나가사키","Hakodate":"하코다테","Beppu":"벳푸",
  "Shimizu":"시미즈","Sasebo":"사세보","Ishigaki":"이시가키","Busan":"부산","Incheon":"인천",
  "Jeju Island":"제주도","Shanghai":"상하이","Hong Kong":"홍콩","Singapore":"싱가포르",
  "Barcelona":"바르셀로나","Rome":"로마","Civitavecchia":"치비타베키아","Naples":"나폴리",
  "Venice":"베네치아","Dubrovnik":"두브로브니크","Santorini":"산토리니","Mykonos":"미코노스",
  "Athens":"아테네","Piraeus":"피레우스","Marseille":"마르세유","Genoa":"제노바",
  "Valletta":"발레타","Lisbon":"리스본","Southampton":"사우샘프턴","Amsterdam":"암스테르담",
  "Copenhagen":"코펜하겐","Stockholm":"스톡홀름","Helsinki":"헬싱키","Oslo":"오슬로",
  "Bergen":"베르겐","Juneau":"주노","Ketchikan":"케치칸","Skagway":"스캐그웨이","Seward":"수어드",
  "Miami":"마이애미","Fort Lauderdale":"포트 로더데일","Cozumel":"코수멜","Nassau":"나소",
  "Honolulu":"호놀룰루","Maui":"마우이","Keelung":"지룽","Keelung (Chilung)":"지룽",
  "Miyako Islands":"미야코지마","Kochi":"고치","Fukuoka":"후쿠오카","Messina":"메시나",
  "La Spezia":"라스페치아","Cannes":"칸","Malaga":"말라가","Split":"스플리트","Kotor":"코토르",
  "Corfu":"코르푸","Rhodes":"로도스","Phuket":"푸켓","Penang":"페낭","Langkawi":"랑카위",
  "Cabo San Lucas":"카보산루카스","Puerto Vallarta":"푸에르토 바야르타","Seattle":"시애틀",
  "Victoria":"빅토리아","New York":"뉴욕","Bermuda":"버뮤다","Reykjavik":"레이캬비크",
  "Dubai":"두바이","Haifa":"하이파","Kusadasi":"쿠사다시","Flam":"플롬","Geiranger":"게이랑에르",
  "Stavanger":"스타방에르","Tallinn":"탈린","Kiel":"킬","Hamburg":"함부르크","Le Havre":"르아브르",
  "Palma de Mallorca":"팔마 데 마요르카","Ibiza":"이비자","Ajaccio":"아작시오","Cagliari":"칼리아리",
  "Catania":"카타니아","Bari":"바리","Ocean Cay":"오션 케이","Great Stirrup Cay":"그레이트 스터럽 케이",
  "Harvest Caye":"하베스트 케이","Labadee":"라바디","Roatan":"로아탄","George Town":"조지타운",
  "Ocho Rios":"오초리오스","Gangjeong":"강정","Sakaiminato":"사카이미나토","Maizuru":"마이즈루",
  "Aburatsu":"아부라쓰","Aomori":"아오모리","Akita":"아키타","Kanazawa":"가나자와",
  "Port Canaveral":"포트 카나베랄","San Juan":"산후안","St. Thomas":"세인트 토마스",
  "St. Maarten":"세인트 마르텐","Barbados":"바베이도스","Aruba":"아루바","Curacao":"퀴라소",
  "Cartagena":"카르타헤나","Buenos Aires":"부에노스 아이레스","Rio de Janeiro":"리우데자네이루",
  "Valparaiso":"발파라이소","Santiago":"산티아고","Sydney":"시드니","Auckland":"오클랜드",
  "Melbourne":"멜버른","Bora Bora":"보라보라","Papeete":"파페에테","Noumea":"누메아",
  "Port Vila":"포트 빌라","Suva":"수바","Colombo":"콜롬보","Cochin":"코친",
  "Taipei":"타이베이","Tianjin":"톈진","Xiamen":"샤먼","Qingdao":"칭다오",
  "Ho Chi Minh City":"호치민","Ha Long Bay":"하롱베이","Da Nang":"다낭","Chan May":"찬마이",
  "Bangkok":"방콕","Laem Chabang":"램차방","Ko Samui":"코사무이","Bali":"발리","Lombok":"롬복",
  "Komodo":"코모도","Jakarta":"자카르타","Semarang":"스마랑","Benoa":"베노아",
  "Muscat":"무스카트","Abu Dhabi":"아부다비","Aqaba":"아카바","Djibouti":"지부티",
  "Piraeus (Athens)":"피레우스 (아테네)","Ephesus (Kusadasi)":"에페수스 (쿠사다시)",
  "Bridgetown":"브리지타운","Fort-de-France":"포르 드 프랑스","Pointe-a-Pitre":"포앵타피트르",
  "Basseterre":"바스테르","Roseau":"로조","Castries":"카스트리스","Kingstown":"킹스타운",
  "Grenada":"그레나다","Tobago":"토바고","Port of Spain":"포트오브스페인",
  "Great Barrier Reef":"그레이트 배리어 리프","Cairns":"케언즈","Darwin":"다윈",
  "Hobart":"호바트","Burnie":"버니","Port Douglas":"포트 더글라스",
  "Nuku Alofa":"누쿠알로파","Apia":"아피아","Lautoka":"로토카","Savusavu":"사부사부",
  "Half Moon Cay":"하프문 케이","Princess Cays":"프린세스 케이",
  "CocoCay":"코코케이","Perfect Day at CocoCay":"코코케이 퍼펙트 데이"
};

const countryKo = {
  "Japan":"일본","South Korea":"한국","China":"중국","Taiwan":"대만","Singapore":"싱가포르",
  "Vietnam":"베트남","Thailand":"태국","Malaysia":"말레이시아","Philippines":"필리핀",
  "Indonesia":"인도네시아","Spain":"스페인","Italy":"이탈리아","France":"프랑스",
  "Greece":"그리스","Turkey":"터키","Croatia":"크로아티아","Montenegro":"몬테네그로",
  "Portugal":"포르투갈","Malta":"몰타","United Kingdom":"영국","Netherlands":"네덜란드",
  "Germany":"독일","Denmark":"덴마크","Sweden":"스웨덴","Norway":"노르웨이",
  "Finland":"핀란드","Iceland":"아이슬란드","Estonia":"에스토니아","United States":"미국",
  "Canada":"캐나다","Mexico":"멕시코","Bahamas":"바하마","Jamaica":"자메이카",
  "Honduras":"온두라스","Belize":"벨리즈","Brazil":"브라질","Australia":"호주",
  "New Zealand":"뉴질랜드","United Arab Emirates":"아랍에미리트","Oman":"오만",
  "Qatar":"카타르","Israel":"이스라엘","Cyprus":"키프로스","Belgium":"벨기에",
  "Poland":"폴란드","Barbados":"바베이도스","Aruba":"아루바","Bermuda":"버뮤다",
  "Cuba":"쿠바","Puerto Rico":"푸에르토리코","Colombia":"콜롬비아","Monaco":"모나코",
  "Argentina":"아르헨티나","Chile":"칠레","Peru":"페루","Uruguay":"우루과이",
  "French Polynesia":"프랑스령 폴리네시아","New Caledonia":"뉴칼레도니아",
  "Fiji":"피지","Vanuatu":"바누아투","Tonga":"통가","Samoa":"사모아",
  "Sri Lanka":"스리랑카","India":"인도","Jordan":"요르단","Egypt":"이집트",
  "Djibouti":"지부티","Martinique":"마르티니크","Guadeloupe":"과들루프",
  "St. Lucia":"세인트 루시아","St. Kitts and Nevis":"세인트 키츠 네비스",
  "Grenada":"그레나다","Trinidad and Tobago":"트리니다드 토바고",
  "Dominica":"도미니카","Antigua and Barbuda":"앤티가 바부다",
  "U.S. Virgin Islands":"미국령 버진 아일랜드","British Virgin Islands":"영국령 버진 아일랜드",
  "Sint Maarten":"신트 마르텐","Curacao":"퀴라소","Bonaire":"보나이르"
};

const SE_ASIA_COUNTRIES = ['Vietnam','Thailand','Malaysia','Philippines','Indonesia','Cambodia','Myanmar','Sri Lanka','India'];

function getDest(regions, countries, startsAt) {
  const r = (regions||[]).join(' ');
  const sc = startsAt?.country || '';
  if(r.includes('Mediterranean')) return 'mediterranean';
  if(r.includes('Alaska')) return 'alaska';
  if(r.includes('Caribbean')||r.includes('Bahamas')) return 'caribbean';
  if(r.includes('Northern Europe')||r.includes('Scandinavia')||r.includes('Baltic')) return 'northern-europe';
  if(r.includes('Hawaii')) return 'hawaii';
  if(r.includes('Asia')) {
    if(sc==='Japan'||sc==='South Korea') return 'korea';
    const hasSEA = countries.some(c => SE_ASIA_COUNTRIES.includes(c));
    if(hasSEA) return 'asia';
    const hasJP = countries.includes('Japan');
    if(hasJP) return 'japan';
    return 'asia';
  }
  if(r.includes('South America')) return 'south-america';
  if(r.includes('Oceania')||r.includes('Pacific')) return 'oceania';
  if(r.includes('Middle East')) return 'asia';
  if(sc==='Japan'||sc==='South Korea') return 'korea';
  return 'other';
}

const destNameKo = {
  mediterranean:'지중해', alaska:'알래스카', caribbean:'카리브해',
  'northern-europe':'북유럽', hawaii:'하와이', korea:'한국/일본',
  japan:'일본', asia:'아시아', 'south-america':'남미', oceania:'오세아니아', other:''
};

function makeTitle(dest, countries, nights) {
  const dname = destNameKo[dest]||'';
  const cko = (countries||[]).map(c=>countryKo[c]||c);
  const unique = [...new Set(cko)];
  if(unique.length<=3 && unique.length>0) return `${unique.join('·')} ${nights}박 크루즈`;
  if(dname) return `${dname} ${nights}박 크루즈`;
  return `${nights}박 크루즈`;
}

function makeHashtags(dest, opName, shipTitle, ports) {
  const tags = [];
  const dname = destNameKo[dest];
  if(dname) tags.push(`#${dname}크루즈`);
  const opInfo = getOpInfo(opName);
  tags.push(opInfo.tag);
  if(shipTitle) tags.push(`#${shipTitle.replace(/\s/g,'')}`);
  const topPorts = ports.slice(0,2).map(p=>portKo[p]||p);
  topPorts.forEach(p=>{ if(p) tags.push(`#${p}`); });
  return tags;
}

(async () => {
  console.log('🚢 CruiseLink V2 전선사 데이터 수집');
  console.log(`📅 ${TODAY}\n`);

  // Phase 1: Get ALL ships (7 pages × 25척 = 175척)
  console.log('Phase 1: 전체 선박 목록 수집 (7페이지)...');
  const allShips = [];
  for(let page=1; page<=7; page++) {
    const d = await apiFetch(`ships.json?per_page=25&page=${page}`);
    if(d?.ships) {
      allShips.push(...d.ships);
      process.stdout.write(`  페이지 ${page}/7 (${allShips.length}척)\r`);
    }
    await sleep(300);
  }
  console.log(`\n  ✅ ${allShips.length}척 확인`);

  // 선사별 집계
  const opCount = {};
  allShips.forEach(s => {
    const op = s.operator?.name || 'Unknown';
    opCount[op] = (opCount[op]||0) + 1;
  });
  console.log('\n선사별:');
  Object.entries(opCount).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>console.log(`  ${k}: ${v}척`));

  // 스킵할 선사 필터
  const filteredShips = allShips.filter(s => !SKIP_OPERATORS.includes(s.operator?.name));
  console.log(`\n스킵: ${SKIP_OPERATORS.join(', ')} → ${allShips.length - filteredShips.length}척 제외`);
  console.log(`수집 대상: ${filteredShips.length}척\n`);

  // Phase 2: Build ships.json + collect cruise refs
  console.log('Phase 2: 선박 정보 정리 + 크루즈 ref 수집...');
  const shipsJson = [];
  const allCruiseRefs = [];

  for(const s of filteredShips) {
    const opName = s.operator?.name || 'Unknown';
    const opInfo = getOpInfo(opName);
    // href: https://www.widgety.co.uk/api/ships/adventure-of-the-seas.json
    const slug = s.href ? s.href.split('/ships/')[1]?.replace('.json','') : s.title.toLowerCase().replace(/[^a-z0-9]+/g,'-');
    const facts = s.ship_facts || {};
    const cruises = s.cruises || [];

    shipsJson.push({
      id: s.id, slug, title: s.title,
      operator: opName, operatorShort: opInfo.short, operatorKo: opInfo.ko,
      profileImage: s.profile_image_href, coverImage: s.cover_image_href || s.profile_image_href,
      shipClass: s.ship_class?.trim()||'', size: s.size, style: s.style,
      launchYear: facts.launch_year, refitYear: facts.refit_year,
      grossTonnage: facts.gross_tonnage, length: facts.length, width: facts.width,
      speed: facts.speed, capacity: facts.capacity, crewCount: facts.crew_count,
      deckCount: facts.deck_count, cabinCount: facts.cabin_count,
      videoUrl: s.video_url || '',
      cruiseCount: cruises.length
    });

    cruises.forEach(c => allCruiseRefs.push({
      ref: c.ref, shipSlug: slug, shipTitle: s.title, opName,
      operatorShort: opInfo.short,
      coverImage: s.cover_image_href || s.profile_image_href,
      profileImage: s.profile_image_href
    }));
  }

  fs.mkdirSync(OUT, {recursive:true});
  fs.writeFileSync(path.join(OUT,'ships.json'), JSON.stringify(shipsJson, null, 0));
  console.log(`✅ ships.json: ${shipsJson.length}척`);
  console.log(`📋 전체 크루즈 ref: ${allCruiseRefs.length}건\n`);

  // Phase 3: Cruise details (holidays/dates/{ref}.json)
  console.log('Phase 3: 크루즈 상세 수집 (가격/일정)...');
  const estMin = Math.ceil(allCruiseRefs.length / BATCH * 0.4 / 60);
  console.log(`  ${allCruiseRefs.length}건, 예상 ${estMin}~${estMin+5}분\n`);

  const cruiseDetails = await batchFetch(allCruiseRefs.map(c => `holidays/dates/${c.ref}.json`));

  // Build cruises.json
  const cruisesJson = [];
  const unmappedPorts = new Set();
  let skipped = 0;

  for(let i=0; i<allCruiseRefs.length; i++) {
    const meta = allCruiseRefs[i];
    const d = cruiseDetails[i];
    if(!d || d.status) { skipped++; continue; }

    const dateFrom = d.date_from?.slice(0,10);
    const dateTo = d.date_to?.slice(0,10);
    if(!dateFrom || dateFrom < TODAY) { skipped++; continue; }

    const nights = Math.round((new Date(dateTo)-new Date(dateFrom))/(86400000));
    const regions = d.regions||[];
    const countries = d.countries||[];
    const dest = getDest(regions, countries, d.starts_at);

    const days = d.itinerary?.days||[];
    const uniquePortNames = [];
    days.forEach(day => {
      const loc = day.locations?.[0];
      if(loc?.name && !uniquePortNames.includes(loc.name)) {
        uniquePortNames.push(loc.name);
        if(!portKo[loc.name]) unmappedPorts.add(loc.name);
      }
    });

    const portRoute = uniquePortNames.map(p=>portKo[p]||p).join(' → ');
    const prices = d.headline_prices?.cruise;
    const title = makeTitle(dest, countries, nights);
    const hashtags = makeHashtags(dest, meta.opName, meta.shipTitle, uniquePortNames);

    cruisesJson.push({
      ref: meta.ref,
      shipSlug: meta.shipSlug,
      shipTitle: meta.shipTitle,
      operator: meta.opName,
      operatorShort: meta.operatorShort,
      dateFrom, dateTo, nights,
      regions, countries,
      countriesKo: countries.map(c=>countryKo[c]||c),
      destination: dest,
      startsAt: {name:d.starts_at?.name, nameKo:portKo[d.starts_at?.name]||d.starts_at?.name, country:d.starts_at?.country, countryKo:countryKo[d.starts_at?.country]||d.starts_at?.country},
      endsAt: {name:d.ends_at?.name, nameKo:portKo[d.ends_at?.name]||d.ends_at?.name, country:d.ends_at?.country, countryKo:countryKo[d.ends_at?.country]||d.ends_at?.country},
      ports: uniquePortNames.map(p=>({name:p, nameKo:portKo[p]||p})),
      portRoute,
      priceInside: prices?.double?.from_inside ? Math.round(parseFloat(prices.double.from_inside)) : null,
      priceOutside: prices?.double?.from_outside ? Math.round(parseFloat(prices.double.from_outside)) : null,
      priceBalcony: prices?.double?.from_balcony ? Math.round(parseFloat(prices.double.from_balcony)) : null,
      priceSuite: prices?.double?.from_suite ? Math.round(parseFloat(prices.double.from_suite)) : null,
      currency: 'USD',
      availability: d.availability_string||'available',
      image: meta.coverImage,
      title, hashtags
    });
  }

  cruisesJson.sort((a,b)=>a.dateFrom.localeCompare(b.dateFrom));
  fs.writeFileSync(path.join(OUT,'cruises.json'), JSON.stringify(cruisesJson, null, 0));
  console.log(`\n✅ cruises.json: ${cruisesJson.length}건 저장 (${skipped}건 스킵)`);

  // 결과 요약
  const destCount = {};
  const opCount2 = {};
  cruisesJson.forEach(c => {
    destCount[c.destination] = (destCount[c.destination]||0)+1;
    opCount2[c.operatorShort] = (opCount2[c.operatorShort]||0)+1;
  });

  console.log('\n📊 목적지별:');
  Object.entries(destCount).sort((a,b)=>b[1]-a[1]).forEach(([d,n])=>console.log(`  ${d}: ${n}건`));
  console.log('\n📊 선사별:');
  Object.entries(opCount2).sort((a,b)=>b[1]-a[1]).forEach(([d,n])=>console.log(`  ${d}: ${n}건`));

  if(unmappedPorts.size > 0) {
    const arr = [...unmappedPorts].sort();
    fs.writeFileSync(path.join(OUT,'unmapped-ports.json'), JSON.stringify(arr, null, 2));
    console.log(`\n⚠️ 미번역 기항지 ${unmappedPorts.size}개 → unmapped-ports.json`);
    arr.slice(0,15).forEach(p=>console.log(`  - ${p}`));
  }

  const shipSize = fs.statSync(path.join(OUT,'ships.json')).size;
  const cruiseSize = fs.statSync(path.join(OUT,'cruises.json')).size;
  console.log(`\n📦 ships.json ${(shipSize/1024).toFixed(0)}KB, cruises.json ${(cruiseSize/1024/1024).toFixed(1)}MB`);
  console.log('\n🎉 수집 완료!');
})();
