#!/usr/bin/env node
// 이 저장소를 내 컴퓨터에서 GitHub Pages 처럼 열어 보기 + 수정 요청 메모(피드백 모드) 받기.
//   npm run serve   → http://127.0.0.1:8090/ (끄려면 Ctrl + C)
// 수정 요청 메모(?memo=1)의 "📤 보내기"를 받아 .claude/feedback.md 에 쌓는다. GitHub Pages 에는 이 주소가 없다.
//   GET    /__feedback?page=/   → { ok, file, open, entries }  (그 페이지의 처리 전 항목, 오래된 것부터)
//   POST   /__feedback  { page, title, note, text, element, where, viewport } → 항목 추가
//   DELETE /__feedback  { key }  → 처리 전 항목 지우기 (key = 제목줄 "시각 · 페이지 「제목」")
// middle school info 의 scripts/serve.mjs 를 옮긴 것. 그쪽이 8080 을 쓰므로 여기는 8090.
// 원격(선생님의 다른 Tailscale 기기)에서도 열리게 이 PC 의 Tailscale 주소(100.x)로도 같이 연다.
import http from 'node:http';
import path from 'node:path';
import fs from 'node:fs';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PORT = 8090;
const FILE = path.join(ROOT, '.claude', 'feedback.md');
const TS_IPS = Object.values(os.networkInterfaces()).flat()
  .filter((a) => a && a.family === 'IPv4' && /^100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\./.test(a.address))
  .map((a) => a.address);
const HOSTNAME = os.hostname().toLowerCase();
const HEADER = `# 화면 피드백

미리보기(\`npm run memo\`, ?memo=1)의 "📤 보내기"로 쌓인 수정 요청. 처리하면 \`[ ]\` 를 \`[x]\` 로 바꾸고 한 줄로 무엇을 했는지 적는다.
(Claude: 세션 시작 때 이 파일에 \`[ ]\` 가 있으면 먼저 알리고 docs/feedback-mode.md 순서대로 처리할 것. 이 파일은 git 에 올리지 않는다.)

`;
const oneLine = (s) => String(s ?? '').replace(/\s+/g, ' ').trim();
const read = () => (fs.existsSync(FILE) ? fs.readFileSync(FILE, 'utf8') : '');

function format(f) {
  const when = new Date().toLocaleString('ko-KR', { hour12: false });
  const lines = [`## ${when} · ${oneLine(f.page) || '/'}${f.title ? ` 「${oneLine(f.title)}」` : ''}`, '- 종류: 메모'];
  if (f.element) lines.push(`- 요소: ${oneLine(f.element)}`);
  if (f.where) lines.push(`- 위치: ${oneLine(f.where)}`);
  if (f.text) lines.push(`- 선택한 글: "${oneLine(f.text)}"`);
  lines.push(`- 메모: ${oneLine(f.note)}`, `- 화면: ${oneLine(f.viewport)}`, '- 상태: [ ] 처리 전', '');
  return lines.join('\n') + '\n';
}

function entries(text, page) {
  const get = (lines, label) => lines.find((l) => l.startsWith(`- ${label}: `))?.slice(label.length + 4) ?? '';
  return text.split(/\n(?=## )/).filter((x) => x.startsWith('## ')).map((sec) => {
    const lines = sec.split('\n');
    const key = lines[0].slice(3);
    return { key, page: key.split(' · ')[1]?.split(' ')[0] ?? '', open: get(lines, '상태').startsWith('[ ]'),
      note: get(lines, '메모'), text: get(lines, '선택한 글').replace(/^"|"$/g, '') };
  }).filter((e) => e.open && (!page || e.page === page));
}

// '//' 처럼 이상한 주소도 서버가 멈추지 않게 base 에 이어 붙여 해석한다
const parseUrl = (u) => { try { return new URL('http://x' + (u.startsWith('/') ? u : '/' + u)); } catch { return null; } };

function feedback(req, res) {
  const url = parseUrl(req.url);
  if (!url) return false;
  if (url.pathname !== '/__feedback') return false;
  const json = (code, obj) => { res.writeHead(code, { 'content-type': 'application/json; charset=utf-8' }); res.end(JSON.stringify(obj)); };
  // 다른 웹사이트가 이 PC 의 미리보기 서버로 글을 끼워 넣지 못하게 한다(feedback.md 는 Claude 가 수정 지시로 읽는다):
  // 주소는 127.0.0.1·localhost·이 PC 의 Tailscale 주소(IP·MagicDNS 이름)로만, Origin 이 붙으면 같은 곳만, 쓰기는 JSON 으로만.
  const isLocal = (h) => h === '127.0.0.1' || h === 'localhost' || TS_IPS.includes(h)
    || h === HOSTNAME || (h.startsWith(HOSTNAME + '.') && h.endsWith('.ts.net'));
  let sameOrigin = true;
  if (req.headers.origin) { try { const o = new URL(req.headers.origin); sameOrigin = isLocal(o.hostname) && o.host === req.headers.host; } catch { sameOrigin = false; } }
  if (!isLocal((req.headers.host || '').replace(/:\d+$/, '')) || !sameOrigin) { json(403, { ok: false, error: '이 PC 미리보기 화면에서만 쓸 수 있어요.' }); return true; }
  if (req.method !== 'GET' && !/^application\/json\b/i.test(req.headers['content-type'] || '')) { json(415, { ok: false, error: 'JSON 으로만 보낼 수 있어요.' }); return true; }
  if (req.method === 'GET') {
    const text = read();
    json(200, { ok: true, file: '.claude/feedback.md', open: (text.match(/^- 상태: \[ \]/gm) ?? []).length, entries: entries(text, url.searchParams.get('page')) });
    return true;
  }
  if (req.method !== 'POST' && req.method !== 'DELETE') { json(405, { ok: false }); return true; }
  let body = '';
  req.on('data', (c) => { body += c; if (body.length > 100000) req.destroy(); });
  req.on('end', () => {
    try {
      const data = JSON.parse(body);
      if (req.method === 'POST') {
        if (!oneLine(data.note)) return json(400, { ok: false, error: '요청을 적어 주세요.' });
        fs.mkdirSync(path.dirname(FILE), { recursive: true });
        if (!fs.existsSync(FILE)) fs.writeFileSync(FILE, HEADER, 'utf8');
        fs.appendFileSync(FILE, format(data), 'utf8');
        return json(200, { ok: true });
      }
      const parts = read().split(/\n(?=## )/);
      const i = parts.findIndex((x) => x.startsWith('## ') && x.split('\n')[0].slice(3) === data.key);
      if (i < 0) return json(404, { ok: false, error: '항목을 찾을 수 없어요(이미 지워졌거나 파일이 바뀜).' });
      if (!/^- 상태: \[ \]/m.test(parts[i])) return json(409, { ok: false, error: '이미 처리된 항목은 지울 수 없어요.' });
      parts.splice(i, 1);
      fs.writeFileSync(FILE, parts.join('\n').replace(/\n*$/, '\n\n'), 'utf8');
      json(200, { ok: true });
    } catch (e) {
      json(400, { ok: false, error: String(e.message ?? e) });
    }
  });
  return true;
}

// 정적 파일 — 사이트에 올라가는 것(index.html · fonts/ · tools/)만 내보낸다. 메모·설정·엑셀은 보이지 않게
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.json': 'application/json', '.woff2': 'font/woff2', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.ico': 'image/x-icon' };
function onRequest(req, res) {
  if (feedback(req, res)) return;
  let p;
  try { p = decodeURIComponent(parseUrl(req.url).pathname); } catch { res.writeHead(400); res.end(); return; }
  if (p.endsWith('/')) p += 'index.html';
  const segs = p.split('/').filter(Boolean);
  const f = path.join(ROOT, ...segs);
  const allowed = (segs.length === 1 && segs[0] === 'index.html') || (segs.length > 1 && ['fonts', 'tools'].includes(segs[0]));
  const blocked = !allowed || segs.some((s) => s.startsWith('.'));
  if (blocked || !f.startsWith(ROOT + path.sep) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f).toLowerCase()] || 'application/octet-stream', 'cache-control': 'no-store' });
  fs.createReadStream(f).pipe(res);
}

const listen = (srv, port, host) => new Promise((r, j) => { srv.once('error', j); srv.listen(port, host, r); });
const main = http.createServer(onRequest);
try { await listen(main, PORT, '127.0.0.1'); }
catch { console.error(`✖ ${PORT} 포트를 이미 쓰는 프로그램이 있어요. 그 프로그램(node)을 끄고 다시 해 보세요.`); process.exit(1); }
console.log(`▶ http://127.0.0.1:${PORT}/  (끄려면 Ctrl + C)`);
for (const host of TS_IPS) {
  try { await listen(http.createServer(onRequest), PORT, host); console.log(`  원격(Tailscale 기기): http://${host}:${PORT}/`); } catch {}
}
