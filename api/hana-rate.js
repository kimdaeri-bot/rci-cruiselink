/**
 * /api/hana-rate
 * 하나은행 1회차 현금 매도율 (USD/KRW) 반환
 * 1차: 네이버 금융 실시간
 * 2차: frankfurter.app (ECB 기준)
 * 3차: fawazahmed0 currency-api
 */
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 's-maxage=600, stale-while-revalidate');

  // 1차: 네이버 금융 USD/KRW 현재가
  try {
    const r = await fetch(
      'https://m.stock.naver.com/front-api/v1/forex/prices?category=exchange&reutersCode=USD%2FKRW',
      { headers: { 'User-Agent': 'Mozilla/5.0', Referer: 'https://finance.naver.com/' } }
    );
    const data = await r.json();
    const price = data?.result?.closePrice || data?.result?.currentPrice;
    if (price) {
      return res.json({ rate: parseFloat(String(price).replace(/,/g, '')), source: 'naver' });
    }
  } catch (_) {}

  // 2차: 네이버 금융 대안 엔드포인트
  try {
    const r = await fetch(
      'https://api.stock.naver.com/forex/price/USDKRW',
      { headers: { 'User-Agent': 'Mozilla/5.0' } }
    );
    const data = await r.json();
    const price = data?.closePrice || data?.currentPrice;
    if (price) {
      return res.json({ rate: parseFloat(String(price).replace(/,/g, '')), source: 'naver2' });
    }
  } catch (_) {}

  // 3차: frankfurter.app
  try {
    const r = await fetch('https://api.frankfurter.app/latest?from=USD&to=KRW');
    const data = await r.json();
    if (data?.rates?.KRW) {
      return res.json({ rate: data.rates.KRW, source: 'frankfurter' });
    }
  } catch (_) {}

  // 4차: fawazahmed0
  try {
    const r = await fetch('https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.min.json');
    const data = await r.json();
    const krw = data?.usd?.krw;
    if (krw) {
      return res.json({ rate: parseFloat(krw.toFixed(2)), source: 'fawazahmed0' });
    }
  } catch (_) {}

  return res.status(500).json({ error: 'all sources failed' });
}
