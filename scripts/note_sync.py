# Word 원고 → 노트(HTML) 반영: python -I scripts/note_sync.py "노트 원고/운영체제/3-1-1 ….docx" os/3-1-1
# - 노트 index.html 의 공부 칸(<!-- 아래 칸을 채워요 --> 부터 </main> 앞까지)만 바꾼다. 머리·이전/다음·목차는 그대로
# - 원고 서식(3.1.1 기준): 제목 → 위치 줄(·키워드·세부내용) → 제목 1(칸 이름) → 글머리 목록(단계 = 들여쓰기, 굵게 = 용어) · 그림 · 표
# - 분홍 [원본과 다름 …] 글 → <span class="fix">, 그림은 노트 폴더에 fig-1.png … 로 저장
# - 원고 제목이 노트 제목과 다르면 알리기만 한다 (목차 이름은 scripts/index-data.json 에서 고친다)
import sys, os, re, zipfile, struct, html
import xml.etree.ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
WP = '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}'
PR = '{http://schemas.openxmlformats.org/package/2006/relationships}'
SITE_URL = 'https://sage810.github.io/computer-theory/'
FIX_COLOR = 'A3356B'
MUTED = '5F4F86'
EMPTY = '아직 비어 있어요.'
e = html.escape


# ── Word → 모형 ──────────────────────────────────────────────
def img_size(b):
    if b[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', b[16:24])
    if b[:2] == b'\xff\xd8':
        i = 2
        while i < len(b):
            m, l = b[i + 1], struct.unpack('>H', b[i + 2:i + 4])[0]
            if m in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack('>HH', b[i + 5:i + 9]); return w, h
            i += 2 + l
    return 0, 0


def docx_to_model(path, note_dir=None):
    z = zipfile.ZipFile(path)
    doc = ET.fromstring(z.read('word/document.xml'))
    styles = {}
    if 'word/styles.xml' in z.namelist():
        for st in ET.fromstring(z.read('word/styles.xml')).findall(W + 'style'):
            styles[st.get(W + 'styleId')] = st.find(W + 'name').get(W + 'val').lower()
    fmt = {}   # (numId, ilvl) → 'bullet' | 'decimal' …
    if 'word/numbering.xml' in z.namelist():
        n = ET.fromstring(z.read('word/numbering.xml'))
        absn = {a.get(W + 'abstractNumId'): a for a in n.findall(W + 'abstractNum')}
        for num in n.findall(W + 'num'):
            a = absn.get(num.find(W + 'abstractNumId').get(W + 'val'))
            if a is None: continue
            for lv in a.findall(W + 'lvl'):
                nf = lv.find(W + 'numFmt')
                fmt[(num.get(W + 'numId'), lv.get(W + 'ilvl'))] = nf.get(W + 'val') if nf is not None else 'bullet'
    rels = {}
    if 'word/_rels/document.xml.rels' in z.namelist():
        for r in ET.fromstring(z.read('word/_rels/document.xml.rels')).findall(PR + 'Relationship'):
            rels[r.get('Id')] = r.get('Target')

    def style(p):
        s = p.find(f'{W}pPr/{W}pStyle')
        return styles.get(s.get(W + 'val'), s.get(W + 'val').lower()) if s is not None else 'normal'

    def run_fmt(r):
        rp = r.find(W + 'rPr'); b = False; color = ''
        if rp is not None:
            x = rp.find(W + 'b'); b = x is not None and x.get(W + 'val') not in ('0', 'false')
            c = rp.find(W + 'color'); color = (c.get(W + 'val') or '').upper() if c is not None else ''
        return b, color

    images = []

    def para_runs(p):
        out = []
        def add(t, b=False, fix=False, href=None, color=''):
            if out and not out[-1].get('br') and (out[-1]['b'], out[-1]['fix'], out[-1].get('href')) == (b, fix, href):
                out[-1]['t'] += t
            else:
                out.append({'t': t, 'b': b, 'fix': fix, 'href': href, 'color': color})
        def walk_run(r, href=None):
            b, color = run_fmt(r)
            for c in r:
                tag = c.tag.split('}')[1]
                if tag == 't': add(c.text or '', b, color == FIX_COLOR, href, color)
                elif tag == 'tab': add(' ', b, color == FIX_COLOR, href, color)
                elif tag == 'br': out.append({'br': True})
                elif tag == 'drawing':
                    blip = c.find('.//' + A + 'blip')
                    if blip is not None:
                        images.append(blip.get(R + 'embed'))
                        out.append({'img': blip.get(R + 'embed'),
                                    'alt': (c.find('.//' + WP + 'docPr').get('descr') or '') if c.find('.//' + WP + 'docPr') is not None else ''})
        for c in p:
            tag = c.tag.split('}')[1]
            if tag == 'r': walk_run(c)
            elif tag == 'hyperlink':
                tgt = rels.get(c.get(R + 'id'), '')
                for r in c.findall(W + 'r'): walk_run(r, tgt or None)
        return out

    model = {'title': '', 'sections': []}
    sec = None
    stack = []          # [(level, list block)]
    last_img = None     # 바로 앞 문단이 그림이면 그 figure (설명 붙이기용)
    n_img = 0

    def save_img(rid, alt):
        nonlocal n_img
        target = rels.get(rid, '')
        data = z.read('word/' + target) if target else b''
        ext = os.path.splitext(target)[1].lower() or '.png'
        n_img += 1
        name = f'fig-{n_img}{".jpeg" if ext in (".jpg", ".jpeg") else ext}'
        if note_dir:
            open(os.path.join(note_dir, name), 'wb').write(data)
        w, h = img_size(data)
        return {'t': 'img', 'src': name, 'w': w, 'h': h, 'alt': alt, 'caption': ''}

    body = doc.find(W + 'body')
    for el in body:
        tag = el.tag.split('}')[1]
        if tag == 'tbl':
            if sec is None: continue
            rows = []
            for tr in el.findall(W + 'tr'):
                row = []
                for tc in tr.findall(W + 'tc'):
                    shd = tc.find(f'{W}tcPr/{W}shd')
                    th = shd is not None and (shd.get(W + 'fill') or 'auto').lower() not in ('auto', 'ffffff')
                    cell = []
                    for i, p in enumerate(tc.findall(W + 'p')):
                        if i: cell.append({'br': True})
                        cell += [r for r in para_runs(p) if 'img' not in r]
                    if th:   # 머리칸은 원래 굵으니 굵게 표시는 뺀다
                        cell = [dict(r, b=False) if not r.get('br') else r for r in cell]
                    row.append({'th': th, 'runs': cell})
                rows.append(row)
            sec['blocks'].append({'t': 'table', 'rows': rows}); stack = []; last_img = None
            continue
        if tag != 'p': continue
        st = style(el)
        runs = para_runs(el)
        text = ''.join(r.get('t', '') for r in runs).strip()
        imgs = [r for r in runs if 'img' in r]
        runs = [r for r in runs if 'img' not in r]
        if st == 'title':
            model['title'] = text; continue
        if st == 'heading 1':
            sec = {'name': text, 'blocks': []}; model['sections'].append(sec); stack = []; last_img = None; continue
        if sec is None:
            continue   # 위치 줄·키워드·세부내용 (머리는 목차 데이터에서 만든다)
        if st in ('heading 2', 'heading 3'):
            if text: sec['blocks'].append({'t': 'h3' if st == 'heading 2' else 'h4', 'text': text})
            stack = []; last_img = None; continue
        num = el.find(f'{W}pPr/{W}numPr')
        ind = el.find(f'{W}pPr/{W}ind')
        left = int(ind.get(W + 'left') or ind.get(W + 'start') or 0) if ind is not None else 0
        if imgs:
            for im in imgs:
                fig = save_img(im['img'], im['alt'])
                lvl = max(0, round(left / 400) - 1) if left else None
                host = None
                if lvl is not None and stack:
                    for lv, lst in reversed(stack):
                        if lv <= lvl and lst['items']: host = lst['items'][-1]; break
                if host is not None: host['figs'].append(fig)
                else: sec['blocks'].append(fig); stack = []
                last_img = fig
            continue
        if last_img is not None and text and num is None and all(r.get('br') or r.get('color') == MUTED for r in runs):
            last_img['caption'] = text; last_img = None; continue
        last_img = None
        if not text:
            continue
        if num is not None:
            nid = num.find(W + 'numId').get(W + 'val')
            il = num.find(W + 'ilvl'); lvl = int(il.get(W + 'val')) if il is not None else 0
            ordered = fmt.get((nid, str(lvl)), 'bullet') != 'bullet'
            if text == EMPTY: continue
            while stack and stack[-1][0] > lvl: stack.pop()
            if not stack or stack[-1][0] < lvl:
                new = {'t': 'list', 'ordered': ordered, 'items': []}
                if stack and stack[-1][1]['items']:
                    stack[-1][1]['items'][-1]['children'].append(new)
                elif not stack:
                    sec['blocks'].append(new)
                else:
                    new = stack[-1][1]   # 단계를 건너뛴 경우: 같은 목록에 넣는다
                stack.append((lvl, new))
            stack[-1][1]['items'].append({'runs': clean(runs), 'children': [], 'figs': []})
            continue
        stack = []
        if text == EMPTY: continue
        sec['blocks'].append({'t': 'p', 'runs': clean(runs)})
    for s in model['sections']:
        if not s['blocks']: s['blocks'] = [{'t': 'empty'}]
    return model


def clean(runs):
    out = [dict(r) for r in runs]
    while out and not out[0].get('br') and not out[0]['t'].strip(): out.pop(0)
    while out and not out[-1].get('br') and not out[-1]['t'].strip(): out.pop()
    if out and not out[0].get('br'): out[0]['t'] = out[0]['t'].lstrip()
    if out and not out[-1].get('br'): out[-1]['t'] = out[-1]['t'].rstrip()
    return out


# ── 모형 → HTML ──────────────────────────────────────────────
def runs_html(runs):
    h = ''
    for r in runs:
        if r.get('br'): h += '<br>'; continue
        t = r['t']
        if r.get('fix'):
            inner = t.strip().strip('[]').strip()
            h += (' ' if h and not h.endswith(' ') else '') + f'<span class="fix">{e(inner)}</span>'
            continue
        x = e(t)
        href = r.get('href')
        if href:
            if href.startswith(SITE_URL): href = '../../' + href[len(SITE_URL):]
            x = f'<a href="{e(href)}">{x}</a>'
        if r.get('b'):
            lead = len(x) - len(x.lstrip(' ')); trail = len(x) - len(x.rstrip(' '))
            x = ' ' * lead + f'<strong>{x.strip(" ")}</strong>' + ' ' * trail if x.strip(' ') else x
        h += x
    return h


def fig_html(f, ind):
    size = f' width="{f["w"]}" height="{f["h"]}"' if f.get('w') else ''
    alt = f.get('alt') or f.get('caption') or '그림'
    cap = f'\n{ind}  <figcaption>{e(f["caption"])}</figcaption>' if f.get('caption') else ''
    return f'{ind}<figure>\n{ind}  <img src="{e(f["src"])}"{size} alt="{e(alt)}">{cap}\n{ind}</figure>'


def list_html(l, ind):
    tag = 'ol' if l['ordered'] else 'ul'
    lines = [f'{ind}<{tag}>']
    for it in l['items']:
        inner = runs_html(it['runs'])
        subs = [list_html(c, ind + '    ') for c in it['children']] + [fig_html(f, ind + '    ') for f in it['figs']]
        if subs:
            lines.append(f'{ind}  <li>{inner}\n' + '\n'.join(subs) + f'\n{ind}  </li>')
        else:
            lines.append(f'{ind}  <li>{inner}</li>')
    lines.append(f'{ind}</{tag}>')
    return '\n'.join(lines)


def block_html(b, ind):
    t = b['t']
    if t == 'empty': return f'{ind}<p class="empty">{EMPTY}</p>'
    if t in ('h3', 'h4'): return f'{ind}<{t}>{e(b["text"])}</{t}>'
    if t == 'p': return f'{ind}<p>{runs_html(b["runs"])}</p>'
    if t == 'list': return list_html(b, ind)
    if t == 'img': return fig_html(b, ind)
    if t == 'table':
        rows = b['rows']; head = rows[0] if rows and all(c['th'] for c in rows[0]) else None
        out = [f'{ind}<table>']
        if head:
            out.append(f'{ind}  <thead><tr>' + ''.join(f'<th scope="col">{runs_html(c["runs"])}</th>' for c in head) + '</tr></thead>')
            rows = rows[1:]
        out.append(f'{ind}  <tbody>')
        for r in rows:
            out.append(f'{ind}    <tr>' + ''.join((f'<th scope="row">{runs_html(c["runs"])}</th>' if c['th'] else f'<td>{runs_html(c["runs"])}</td>') for c in r) + '</tr>')
        out.append(f'{ind}  </tbody>\n{ind}</table>')
        return '\n'.join(out)
    return ''


def sections_html(sections):
    out = []
    for i, s in enumerate(sections):
        sid = 'concept' if i == 0 else f'part-{i + 1}'
        out.append(f'    <section class="part" id="{sid}">\n      <h2>{e(s["name"])}</h2>\n' +
                   '\n'.join(block_html(b, '      ') for b in s['blocks']) + '\n    </section>')
    return '\n'.join(out)


MARK = '    <!-- 아래 칸을 채워요.'

def write_sections(note_html, sections):
    s = open(note_html, encoding='utf-8').read()
    i = s.index(MARK); j = s.index('\n', i) + 1; k = s.index('  </main>')
    s = s[:j] + sections_html(sections) + '\n' + s[k:]
    open(note_html, 'w', encoding='utf-8', newline='\n').write(s)


if __name__ == '__main__':
    docx, note_dir = sys.argv[1], sys.argv[2]
    for old in os.listdir(note_dir):
        if re.match(r'fig-\d+\.(png|jpe?g|gif)$', old): os.remove(os.path.join(note_dir, old))
    m = docx_to_model(docx, note_dir)
    f = os.path.join(note_dir, 'index.html')
    h1 = re.search(r'<h1 class="cr">(.*?)</h1>', open(f, encoding='utf-8').read())
    no = os.path.basename(os.path.normpath(note_dir)).replace('-', '.')
    if h1 and m['title'] != f'{no} {html.unescape(h1.group(1))}':
        print(f'! 원고 제목이 노트 제목과 달라요: 원고 "{m["title"]}" / 노트 "{no} {html.unescape(h1.group(1))}" — 목차 이름은 scripts/index-data.json 에서 고칩니다')
    write_sections(f, m['sections'])
    print('반영:', f, '| 칸', [s['name'] for s in m['sections']])
