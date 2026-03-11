export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({error: 'Method not allowed'});

  const inquiry = req.body;
  const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
  const REPO = 'kimdaeri-bot/cruiselink-v2';
  const FILE_PATH = 'admin/inquiries.json';

  try {
    const getRes = await fetch(`https://api.github.com/repos/${REPO}/contents/${FILE_PATH}`, {
      headers: { Authorization: `Bearer ${GITHUB_TOKEN}`, Accept: 'application/vnd.github.v3+json' }
    });
    const fileData = await getRes.json();
    const currentContent = JSON.parse(Buffer.from(fileData.content, 'base64').toString('utf8'));
    const sha = fileData.sha;
    currentContent.push({ ...inquiry, id: Date.now().toString(), timestamp: new Date().toISOString(), status: '신규' });
    const newContent = Buffer.from(JSON.stringify(currentContent, null, 2)).toString('base64');
    await fetch(`https://api.github.com/repos/${REPO}/contents/${FILE_PATH}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${GITHUB_TOKEN}`, 'Content-Type': 'application/json', Accept: 'application/vnd.github.v3+json' },
      body: JSON.stringify({ message: 'feat: 새 문의 추가', content: newContent, sha })
    });
    res.status(200).json({ success: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}
