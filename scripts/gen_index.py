# 첫 화면(index.html) 만들기: python -I scripts/gen_index.py scripts/index-data.json index.html
# 과목·영역·내용요소·키워드·세부내용은 index-data.json (example1.xlsx 에서 옮김). 칸이 채워진 노트는 목차에서 자동으로 링크된다
import sys, json, html

DATA = json.load(open(sys.argv[1], encoding='utf-8'))
OUT = sys.argv[2]
e = html.escape

IDS = ['ds', 'algo', 'os']
ACCENT = ['#a9dce4', '#f9cade', '#fbe6a2']
TINT = ['#e3f3f6', '#fdeaf2', '#fdf5d9']

n_areas = sum(len(s['areas']) for s in DATA)
n_items = sum(len(a['items']) for s in DATA for a in s['areas'])

# 노트(ds|algo|os/번호/index.html)의 칸이 하나라도 채워졌으면 목차에서 링크한다
import os
SITE = os.path.dirname(os.path.abspath(OUT))
def note_href(sid, no):
    rel = f"{sid}/{no.replace('.', '-')}/index.html"
    f = os.path.join(SITE, rel)
    if not os.path.exists(f):
        return None
    return rel if open(f, encoding='utf-8').read().count('<p class="empty">') < 4 else None
n_linked = sum(1 for si, s in enumerate(DATA) for ai, a in enumerate(s['areas']) for ii, _ in enumerate(a['items'])
               if note_href(IDS[si], f'{si+1}.{ai+1}.{ii+1}'))

CSS = """
  @font-face{font-family:'CookieRun';font-weight:700;src:url(fonts/CookieRun-700.woff2) format('woff2');font-display:swap}
  @font-face{font-family:'Maplestory';font-weight:300;src:url(fonts/Maplestory-300.woff2) format('woff2');font-display:swap}
  @font-face{font-family:'Maplestory';font-weight:700;src:url(fonts/Maplestory-700.woff2) format('woff2');font-display:swap}
  :root{--ink:#4b3b6b;--paper:#fffdf7;--page:#e7e3f7;--grid:#d8d2ee;--soft:#fffaee;--muted:#5f4f86;--line:rgba(75,59,107,.16);--guide:rgba(75,59,107,.28);--sh:rgba(75,59,107,.18);--focus:#d9488f}
  *{box-sizing:border-box}
  @font-face{font-family:'NEXON Lv2 Gothic';font-weight:400;src:url(fonts/NEXONLv2Gothic-Regular.subset.woff2) format('woff2');font-display:swap}
  body{margin:0;padding:24px 16px 48px;color:var(--ink);font-family:'NEXON Lv2 Gothic','Apple SD Gothic Neo','Malgun Gothic',sans-serif;font-weight:400;line-height:1.5;word-break:keep-all;overflow-wrap:break-word;
    background-color:var(--page);background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:28px 28px}
  a{color:inherit}
  :focus-visible{outline:3px solid var(--focus);outline-offset:2px}
  .cr{font-family:'CookieRun','Maplestory',sans-serif;font-weight:700}
  .window{max-width:1040px;margin:0 auto;background:var(--paper);border:4px solid var(--ink);border-radius:16px;box-shadow:8px 8px 0 rgba(75,59,107,.22)}
  /* 제목줄 */
  .titlebar{display:flex;flex-wrap:wrap;align-items:center;gap:8px 16px;padding:16px 20px;border-bottom:4px solid var(--ink);border-radius:12px 12px 0 0;
    background:linear-gradient(90deg,#f9cade 0%,#d6c4f5 55%,#c4d8f7 100%)}
  .titlebar h1{margin:0;font-size:26px;line-height:1.2;white-space:nowrap}
  .titlebar .sub{font-size:15px}
  .count{margin-left:auto;padding:4px 12px;border:3px solid var(--ink);border-radius:9px;background:var(--paper);box-shadow:3px 3px 0 rgba(75,59,107,.25);font-size:14px;white-space:nowrap}
  /* 과목 탭 + 모두 펼치기 */
  .bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;padding:20px 20px 0}
  .tabs{display:flex;flex-wrap:wrap;gap:8px}
  .tab{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:8px 16px;border:3px solid var(--ink);border-radius:10px;background:var(--paper);box-shadow:3px 3px 0 rgba(75,59,107,.25);
    color:var(--ink);font-size:17px;line-height:1.2;cursor:pointer}
  .tab .n{font-family:'Maplestory',sans-serif;font-size:13px}
  .tab[aria-selected="true"]{background:var(--accent);transform:translate(2px,2px);box-shadow:1px 1px 0 rgba(75,59,107,.25)}
  .btn-all{min-height:44px;padding:8px 16px;border:3px solid var(--ink);border-radius:10px;background:var(--soft);box-shadow:3px 3px 0 rgba(75,59,107,.25);
    color:var(--ink);font-family:'Maplestory',sans-serif;font-weight:700;font-size:15px;cursor:pointer}
  /* 본문 */
  main{padding:20px 20px 32px}
  .notice{margin:0 0 20px;padding:12px 16px;border:3px solid var(--ink);border-radius:11px;background:var(--soft);font-size:15px;text-wrap:pretty}
  .panel[hidden]{display:none}
  .subject-head{display:flex;flex-wrap:wrap;align-items:center;gap:8px 16px;padding:12px 16px;border:3px solid var(--ink);border-radius:12px;background:var(--accent);box-shadow:5px 5px 0 var(--sh)}
  .subject-head .big{font-size:28px;line-height:1}
  .subject-head h2{margin:0;font-size:26px;line-height:1.2}
  .subject-head .meta{margin-left:auto;font-size:15px}
  /* 트리 개요: 영역 → 내용요소 → 세부내용 */
  .area{margin-top:36px}
  .area-head{display:flex;align-items:baseline;gap:12px;margin:0 0 8px}
  .area-head .no{font-size:18px}
  .area-head h3{margin:0;font-size:21px;line-height:1.3}
  .area-head .cnt{font-size:14px;color:var(--muted)}
  .tree{list-style:none;margin:0 0 0 12px;padding:0;border-left:3px solid var(--guide)}
  .item{position:relative;display:flex;gap:16px;align-items:flex-start;padding:12px 0 12px 24px}
  .item > .no{flex:none;width:52px;padding-top:2px;font-size:14px;color:var(--muted)}
  .item .body{flex:1;min-width:0;display:flex;flex-direction:column;gap:8px}
  .item .head{display:flex;align-items:flex-start;gap:12px}
  .item .name{flex:0 1 auto;min-width:0;font-family:'Maplestory',sans-serif;font-size:16px;font-weight:700;line-height:1.55;text-wrap:pretty;text-decoration:none}
  .item a.name{text-decoration:underline;text-decoration-color:var(--guide);text-decoration-thickness:2px;text-underline-offset:4px}
  .soon{flex:none;margin-left:auto;margin-top:2px;padding:4px 8px;border:2px dashed #8b7cb8;border-radius:6px;font-size:12px;line-height:1;color:var(--muted);white-space:nowrap}
  .tags{display:flex;flex-wrap:wrap;gap:4px 12px;margin:0;padding:0;list-style:none}
  .tags li{font-size:14px;line-height:1.5;color:var(--muted)}
  .det summary{display:inline-flex;align-items:center;gap:8px;min-height:40px;padding:8px 12px;border:2px solid var(--ink);border-radius:8px;background:var(--tint);
    font-family:'Maplestory',sans-serif;font-size:14px;font-weight:700;line-height:1.2;cursor:pointer;list-style:none;user-select:none}
  .det summary::-webkit-details-marker{display:none}
  /* 스크립트가 있으면: '세부내용' 버튼 대신 이름 오른쪽 ⌄ 버튼으로 접고 편다 (없으면 위 버튼 그대로) */
  .tog{display:none;flex:none;place-items:center;width:28px;height:28px;margin:-2px 0 0 -10px;padding:0;border:0;border-radius:50%;background:transparent;color:var(--ink);cursor:pointer}
  .tog[aria-expanded="true"] svg{transform:rotate(180deg)}
  .js .tog{display:inline-grid}
  .js .det > summary{display:none}
  .js .det:not([open]){display:none}
  .js .det ul{margin-top:0}
  .det summary svg{flex:none}
  .det[open] summary svg{transform:rotate(180deg)}
  .det ul{list-style:none;margin:8px 0 0;padding:12px 16px;border:2px dashed var(--guide);border-radius:10px;background:var(--soft);display:flex;flex-direction:column;gap:8px}
  .det li{display:flex;gap:8px;font-size:15px;line-height:1.6;text-wrap:pretty}
  /* 마우스가 있는 기기에서만 — 휴대폰에서 누른 뒤 색이 남지 않게 */
  @media (hover:hover){
    .tab[aria-selected="false"]:hover{background:var(--soft)}
    .btn-all:hover{background:var(--page)}
    .tog:hover{background:var(--tint)}
    .item a.name:hover{text-decoration-color:var(--ink)}
  }
  .det li .br{flex:none;color:var(--muted)}
  @media (max-width:520px){
    body{padding:12px 12px 32px}
    .titlebar h1{font-size:22px}
    .count{margin-left:0}
    .bar{padding:16px 12px 0}
    main{padding:16px 12px 24px}
    .tree{margin-left:4px}
    .item{gap:8px;padding:12px 0 12px 16px}
    .item > .no{width:44px;font-size:13px}
    .det summary{min-height:44px}
    .tog{width:44px;height:44px;margin:-10px 0 0 -14px}
  }
"""

JS = """
(function () {
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  var panels = Array.prototype.slice.call(document.querySelectorAll('[role="tabpanel"]'));
  var ids = tabs.map(function (t) { return t.dataset.id; });
  function select(id, focus) {
    tabs.forEach(function (t) {
      var on = t.dataset.id === id;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      if (on && focus) t.focus();
    });
    panels.forEach(function (p) { p.hidden = p.id !== 'p-' + id; });
    syncAll();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () {
      select(t.dataset.id);
      history.replaceState(null, '', '#' + t.dataset.id);
    });
    t.addEventListener('keydown', function (ev) {
      var d = ev.key === 'ArrowRight' ? 1 : ev.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      ev.preventDefault();
      var next = ids[(i + d + ids.length) % ids.length];
      select(next, true);
      history.replaceState(null, '', '#' + next);
    });
  });
  // 세부내용 모두 펼치기/접기 — 지금 보이는 과목에만
  var btn = document.querySelector('.btn-all');
  function visibleDetails() {
    var p = panels.filter(function (x) { return !x.hidden; })[0];
    return p ? Array.prototype.slice.call(p.querySelectorAll('details.det')) : [];
  }
  function syncAll() {
    var ds = visibleDetails();
    var allOpen = ds.length > 0 && ds.every(function (d) { return d.open; });
    btn.textContent = allOpen ? '세부내용 모두 접기' : '세부내용 모두 펼치기';
  }
  btn.hidden = false;
  btn.addEventListener('click', function () {
    var ds = visibleDetails();
    var open = !ds.every(function (d) { return d.open; });
    ds.forEach(function (d) { d.open = open; });
    syncAll();
  });
  document.querySelectorAll('details.det').forEach(function (d) { d.addEventListener('toggle', syncAll); });
  // 이름 오른쪽 ⌄ 버튼 — 눌러서 세부내용 접고 펴기, 모두 펼치기와도 맞춰진다
  document.querySelectorAll('.tog').forEach(function (b) {
    var d = document.getElementById(b.getAttribute('aria-controls'));
    b.addEventListener('click', function () { d.open = !d.open; });
    d.addEventListener('toggle', function () {
      b.setAttribute('aria-expanded', d.open ? 'true' : 'false');
    });
  });
  var start = location.hash.slice(1);
  select(ids.indexOf(start) >= 0 ? start : ids[0]);
})();
"""

CHEV = '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg>'

out = []
w = out.append
w('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n')
w('<title>컴퓨터 이론 공부 노트</title>\n<meta name="description" content="자료구조 · 알고리즘 · 운영체제 영역별 내용요소와 세부내용">\n<link rel="icon" href="data:,">\n<script>document.documentElement.classList.add(\'js\')</script>\n<style>')
w(CSS)
w('</style>\n</head>\n<body>\n<div class="window">\n')
w('  <header class="titlebar">\n    <h1 class="cr">컴퓨터 이론</h1>\n    <span class="sub">자료구조 · 알고리즘 · 운영체제 공부 노트</span>\n')
w(f'    <span class="count">연결된 자료 {n_linked} / {n_items}</span>\n  </header>\n')

# 과목 탭
w('  <div class="bar">\n    <div class="tabs" role="tablist" aria-label="과목">\n')
for si, s in enumerate(DATA):
    total = sum(len(a['items']) for a in s['areas'])
    w(f'      <button type="button" class="tab cr" role="tab" id="t-{IDS[si]}" data-id="{IDS[si]}" aria-controls="p-{IDS[si]}" aria-selected="{"true" if si == 0 else "false"}" style="--accent:{ACCENT[si]}">{si+1} {e(s["name"])} <span class="n">{total}개</span></button>\n')
w('    </div>\n    <button type="button" class="btn-all" hidden>세부내용 모두 펼치기</button>\n  </div>\n')

w('  <main>\n')
w(f'    <p class="notice">{len(DATA)}과목 · {n_areas}영역 · 내용요소 {n_items}개. 세부내용이 있는 내용요소는 이름 옆 화살표 버튼을 눌러 펼쳐요. 정리한 노트가 있는 내용요소는 이름을 누르면 노트로 가고, 아직 없는 것은 ‘준비 중’이에요.</p>\n')
for si, s in enumerate(DATA, 1):
    sid = IDS[si-1]
    total = sum(len(a['items']) for a in s['areas'])
    w(f'    <section class="panel" id="p-{sid}" role="tabpanel" aria-labelledby="t-{sid}" style="--accent:{ACCENT[si-1]};--tint:{TINT[si-1]}">\n')
    w(f'      <div class="subject-head"><span class="big cr">{si}</span><h2 class="cr">{e(s["name"])}</h2><span class="meta">{len(s["areas"])}개 영역 · 내용요소 {total}개</span></div>\n')
    for ai, a in enumerate(s['areas'], 1):
        w(f'      <section class="area" id="{sid}-{ai}">\n')
        w(f'        <div class="area-head"><span class="no cr">{si}.{ai}</span><h3 class="cr">{e(a["name"])}</h3><span class="cnt">{len(a["items"])}개</span></div>\n')
        w('        <ol class="tree">\n')
        for ii, it in enumerate(a['items'], 1):
            w(f'          <li class="item"><span class="no cr">{si}.{ai}.{ii}</span><div class="body">\n')
            did = f'd-{sid}-{ai}-{ii}'
            tog = f'<button type="button" class="tog" aria-expanded="false" aria-controls="{did}" aria-label="{e(it["t"])} 세부내용">{CHEV}</button>' if it['d'] else ''
            href = note_href(sid, f'{si}.{ai}.{ii}')
            name = f'<a class="name" href="{href}">{e(it["t"])}</a>' if href else f'<span class="name">{e(it["t"])}</span>'
            soon = '' if href else '<span class="soon">준비 중</span>'
            w(f'            <div class="head">{name}{tog}{soon}</div>\n')
            if it['k']:
                w('            <ul class="tags" aria-label="키워드">' + ''.join(f'<li>#{e(k)}</li>' for k in it['k']) + '</ul>\n')
            if it['d']:
                w(f'            <details class="det" id="{did}"><summary>세부내용 {CHEV}</summary><ul>' + ''.join(f'<li><span class="br" aria-hidden="true">└</span><span>{e(x)}</span></li>' for x in it['d']) + '</ul></details>\n')
            w('          </div></li>\n')
        w('        </ol>\n      </section>\n')
    w('    </section>\n')
w('  </main>\n</div>\n<script>')
w(JS)
w('</script>\n<!-- 수정 요청 메모(피드백 모드): 주소 끝에 ?memo=1 일 때만 켜짐. docs/feedback-mode.md -->\n<script src="tools/memo.js" defer></script>\n</body>\n</html>\n')

with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(''.join(out))
print(n_areas, n_items)
