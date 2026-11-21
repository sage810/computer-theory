// 왼쪽 고정 목차(사이드바) — 첫 화면과 노트 58장이 같이 쓴다. 모양은 assets/sidebar.css, 목차 데이터는 assets/toc.js (npm run index 가 만듦)
// 불러오는 쪽: <script src=".../assets/sidebar.js" data-root="../../" data-current="3-1-6"></script>  (첫 화면은 data-root="" 이고 data-current 없음)
(function () {
  var me = document.currentScript;
  var TOC = window.CT_TOC;
  if (!me || !TOC) return;
  var ROOT = me.getAttribute('data-root') || '';
  var CUR = me.getAttribute('data-current') || '';
  var html = document.documentElement;
  var wide = window.matchMedia('(min-width: 1000px)');
  var KEY = 'ct-side';   // 넓은 화면에서 접었는지 기억 (이 브라우저에만)
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function store(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  var CHEV = '<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 4l4 4-4 4"/></svg>';
  var PANEL = '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M9 4v16"/></svg>';

  // 처음 펼쳐 둘 곳: 노트면 그 과목·영역, 첫 화면이면 지금 고른 과목 탭
  var openSid = '', openArea = '';
  if (CUR) {
    var p = CUR.split('-');
    openSid = TOC[+p[0] - 1].id; openArea = p[0] + '-' + p[1];
  } else {
    var t = document.querySelector('[role="tab"][aria-selected="true"]');
    openSid = t ? t.getAttribute('data-id') : TOC[0].id;
  }

  var h = '<div class="ct-side-head"><a class="ct-side-title cr" href="' + ROOT + 'index.html">목차</a>' +
    '<button type="button" class="ct-side-close" aria-label="목차 접기" aria-controls="ct-side">' + PANEL + '</button></div>' +
    '<nav class="ct-side-nav" aria-label="전체 목차">';
  TOC.forEach(function (s, si) {
    var sn = si + 1;
    h += '<details class="ct-s" data-sid="' + s.id + '" style="--accent:' + s.accent + ';--tint:' + s.tint + '"' + (s.id === openSid ? ' open' : '') + '>' +
      '<summary class="cr">' + CHEV + '<span>' + sn + ' ' + esc(s.name) + '</span></summary>';
    s.areas.forEach(function (a, ai) {
      var an = sn + '-' + (ai + 1);
      h += '<details class="ct-a"' + (an === openArea ? ' open' : '') + '><summary>' + CHEV +
        '<span class="no">' + sn + '.' + (ai + 1) + '</span><span>' + esc(a.name) + '</span></summary><ul>';
      a.items.forEach(function (it, ii) {
        var slug = an + '-' + (ii + 1);
        // 노트가 없으면 첫 화면의 그 줄로 (첫 화면 안에서는 새로 불러오지 않게 #만)
        var href = it.note ? ROOT + s.id + '/' + slug + '/index.html' : (CUR ? ROOT + 'index.html' : '') + '#i-' + slug;
        h += '<li><a href="' + href + '"' + (it.note ? ' class="has-note"' : '') + (slug === CUR ? ' aria-current="page"' : '') + '>' +
          '<span class="no">' + slug.replace(/-/g, '.') + '</span><span>' + esc(it.t) + '</span></a></li>';
      });
      h += '</ul></details>';
    });
    h += '</details>';
  });
  h += '</nav>';

  var side = document.createElement('aside');
  side.id = 'ct-side'; side.className = 'ct-side'; side.setAttribute('aria-label', '목차');
  side.innerHTML = h;
  var openBtn = document.createElement('button');
  openBtn.type = 'button'; openBtn.className = 'ct-side-open'; openBtn.setAttribute('aria-controls', 'ct-side');
  openBtn.innerHTML = PANEL + '<span>목차</span>';
  var shade = document.createElement('div');
  shade.className = 'ct-side-shade';
  document.body.insertBefore(shade, document.body.firstChild);
  document.body.insertBefore(openBtn, shade);
  document.body.insertBefore(side, openBtn);
  html.classList.add('has-side');
  var closeBtn = side.querySelector('.ct-side-close');
  var nav = side.querySelector('.ct-side-nav');

  function setOpen(open, focus) {
    html.classList.toggle('side-open', open);
    html.classList.toggle('side-closed', !open);
    openBtn.setAttribute('aria-expanded', String(open));
    closeBtn.setAttribute('aria-expanded', String(open));
    if (focus) (open ? closeBtn : openBtn).focus();
  }
  function initial() { setOpen(wide.matches ? stored() !== 'closed' : false); }
  initial();
  if (wide.addEventListener) wide.addEventListener('change', initial);

  openBtn.addEventListener('click', function () { setOpen(true, true); if (wide.matches) store('open'); });
  closeBtn.addEventListener('click', function () { setOpen(false, true); if (wide.matches) store('closed'); });
  shade.addEventListener('click', function () { setOpen(false); });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape' && !wide.matches && html.classList.contains('side-open')) setOpen(false, true);
  });
  // 좁은 화면에서 링크를 누르면 서랍을 닫는다 (같은 페이지 안 이동일 때)
  nav.addEventListener('click', function (ev) {
    if (!wide.matches && ev.target.closest('a')) setOpen(false);
  });

  // 지금 보는 내용요소를 목차 안에서 보이게
  var cur = side.querySelector('[aria-current]');
  if (cur) nav.scrollTop = Math.max(0, cur.offsetTop - nav.clientHeight / 3);

  // 첫 화면 과목 탭이 바뀌면 그 과목을 펼친다
  window.CTSide = {
    openSubject: function (sid) {
      var d = side.querySelector('.ct-s[data-sid="' + sid + '"]');
      if (d) d.open = true;
    }
  };
})();
