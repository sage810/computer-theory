#!/usr/bin/env node
// "피드백 모드" / "메모 켜줘" — 이 PC 에서 수정 요청 메모(tools/memo.js)를 바로 쓸 수 있게 한다.
//   npm run memo              → 첫 화면을 연다
//   npm run memo -- algo      → 알고리즘 탭으로 연다 (ds · algo · os)
//   npm run memo -- 3-1-1     → 그 내용요소가 있는 영역 노트를 그 자리에서 연다 (3.1.1 도 됨)
//   npm run memo -- 3-1       → 그 영역 노트를 연다
// 하는 일: ① 미리보기 서버(8090)가 꺼져 있으면 뒤에서 켬 ② 주소 끝에 ?memo=1 을 붙여 브라우저로 연다.
// 이 서버에서 연 메모 창은 "📤 보내기"로 요청을 .claude/feedback.md 에 바로 쌓는다(scripts/serve.mjs).
// 서버는 PC 를 끄거나 작업 관리자에서 node 를 끝내면 꺼진다.
import path from 'node:path';
import os from 'node:os';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const base = 'http://127.0.0.1:8090';
const tab = (process.argv.slice(2).find((a) => !a.startsWith('--')) || '').replace(/^#/, '');
// 영역 번호(3-1) 또는 내용요소 번호(3-1-1, 3.1.1)면 그 영역 노트를 연다 (내용요소면 그 자리로)
const note = /^([123])[.-](\d+)(?:[.-](\d+))?$/.exec(tab);
const pagePath = note ? `/${['ds', 'algo', 'os'][+note[1] - 1]}/${note[1]}-${note[2]}/` : '/';
const hash = ['ds', 'algo', 'os'].includes(tab) ? '#' + tab : note && note[3] ? `#n-${note[1]}-${note[2]}-${note[3]}` : '';

// ① 서버 — /__feedback 이 응답해야 이 저장소의 서버다
const up = async () => { try { return (await fetch(base + '/__feedback', { signal: AbortSignal.timeout(1500) })).ok; } catch { return false; } };
let started = false;
if (!(await up())) {
  spawn(process.execPath, [path.join(ROOT, 'scripts', 'serve.mjs')], { cwd: ROOT, detached: true, stdio: 'ignore', windowsHide: true }).unref();
  started = true;
  for (let i = 0; i < 20 && !(await up()); i++) await new Promise((r) => setTimeout(r, 300));
  if (!(await up())) { console.error('✖ 미리보기 서버를 켜지 못했어요. 8090 포트를 다른 프로그램이 쓰는지 확인하고 `npm run serve` 로 직접 켜 보세요.'); process.exit(1); }
}

// ② 열기
const url = `${base}${pagePath}?memo=1${hash}`;
const page = await (await fetch(base + pagePath)).text();
if (!page.includes('tools/memo.js')) console.log('△ 이 서버의 첫 화면에 메모 기능이 없어요. index.html 에 tools/memo.js 가 붙어 있는지 확인하세요.');
if (process.platform === 'win32') spawn('cmd', ['/c', 'start', '""', url], { detached: true, stdio: 'ignore', windowsHide: true }).unref();
console.log(`✔ 메모 켰어요${started ? ' (미리보기 서버도 새로 켬)' : ''}: ${url}`);
const ts = Object.values(os.networkInterfaces()).flat()
  .filter((a) => a && a.family === 'IPv4' && /^100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\./.test(a.address)).map((a) => a.address);
for (const ip of ts) console.log(`  원격(Tailscale 기기)에서: http://${ip}:8090${pagePath}?memo=1${hash}  (안 열리면 Windows 방화벽이 8090 을 막는 것)`);
console.log('  글을 드래그 또는 🎯 요소 고르기 → 오른쪽 아래 📝 메모 → 요청 적기 → 📤 보내기 (.claude/feedback.md 에 쌓임) → Claude 에 "피드백 처리해줘"');
