import re, sys, unicodedata, html
import markdown, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figures import F

src, out = sys.argv[1], sys.argv[2]
md = open(src, encoding='utf-8').read()

def slug(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('đ', 'd').replace('Đ', 'D')
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()
    return s

# bỏ phần tiêu đề, trích dẫn mở đầu; trang dùng dải đầu và thanh mục lục riêng
body_md = '## 1. Giới thiệu nhanh' + md.split('## 1. Giới thiệu nhanh', 1)[1]
intro = re.search(r'^> (.+)$', md, re.M).group(1)

h = markdown.markdown(body_md, extensions=['tables', 'sane_lists'])
h = h.replace('<hr />', '')
# hình minh hoạ: khối <!-- fig:x --> ... <!-- /fig --> được thay hẳn bằng hình; <!-- fig:x --> đứng một mình thì chèn hình vào
h = re.sub(r'<!-- fig:(\w+) -->(?:(?!<!-- fig:).)*?<!-- /fig -->', lambda m: F[m.group(1)], h, flags=re.S)
h = re.sub(r'<!-- fig:(\w+) -->', lambda m: F[m.group(1)], h)

# ids for h2/h3
nav = []
def hrep(m):
    tag, inner = m.group(1), m.group(2)
    i = slug(inner)
    if tag == 'h2':
        nav.append([inner, i, []])
    elif nav:
        nav[-1][2].append((inner, i))
    return f'<{tag} id="{i}">{inner}</{tag}>'
h = re.sub(r'<(h2|h3)>(.*?)</\1>', hrep, h)

# mỗi sách (h4) thành một thẻ; các dòng "**Nhãn:**" thành hàng câu hỏi có nhãn
QLAB = {'Bối cảnh': 1, 'Mục đích': 2, 'Hình dạng': 3, 'Về Đức Chúa Trời': 4, 'Pawson nhấn mạnh': 5, 'Áp dụng': 6, 'Ghi nhớ': 7}

def qrows(art):
    out, pos = [], 0
    pat = re.compile(r'<li><strong>(' + '|'.join(QLAB) + r'):</strong>\s*')
    while True:
        m = pat.search(art, pos)
        if not m:
            out.append(art[pos:]); break
        out.append(art[pos:m.start()])
        depth, i = 1, m.end()
        while depth:
            nxt = re.search(r'<li[ >]|</li>', art[i:])
            j = i + nxt.start()
            if nxt.group(0) == '</li>':
                depth -= 1
                if depth == 0:
                    break
            else:
                depth += 1
            i = j + len(nxt.group(0))
        lab = m.group(1)
        body = art[m.end():j]
        body = re.sub(r'^([a-zà-ỹđ])', lambda c: c.group(1).upper(), body)
        out.append(f'<li class="qrow q{QLAB[lab]}"><span class="qlab">{lab}</span><div class="qbody">{body}</div></li>')
        pos = j + len('</li>')
    return ''.join(out).replace('<ul>\n<li class="qrow', '<ul class="qs">\n<li class="qrow', 1)

books = []  # (volume label, name, id)
parts = re.split(r'(?=<h[234][ >])', h)
cur_vol, res, i = '', [], 0
while i < len(parts):
    p = parts[i]
    m3 = re.match(r'<h3 id="[^"]+">(.*?)</h3>', p)
    if m3:
        cur_vol = m3.group(1)
    if p.startswith('<h2'):
        cur_vol = ''
    m4 = re.match(r'<h4>(.*?)</h4>', p)
    if m4:
        name = m4.group(1)
        bid = 'sach-' + slug(re.sub(r'^Nhập đề:\s*', 'nhap de ', name))
        books.append((cur_vol, name, bid))
        body = p[m4.end():]
        body = re.sub(r'^\s*<p><em>(.*?)</em></p>', r'<p class="meta">\1</p>', body, count=1)
        p = f'<article class="book" id="{bid}"><h4>{name}</h4>{qrows(body)}</article>\n'
    res.append(p)
    i += 1
h = ''.join(res)

# wrap each h2 section
parts = re.split(r'(?=<h2 id=)', h)
h = ''.join(f'<section class="sec">{p}</section>' if p.startswith('<h2') else p for p in parts)
# tables scroll
h = h.replace('<table>', '<div class="tbl"><table>').replace('</table>', '</table></div>')
# external links new tab
h = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', h)

# nav html
nav_html = []
for title, i, subs in nav:
    short = re.sub(r'^\d+\.\s*', '', title)
    num = re.match(r'^(\d+)\.', title)
    nav_html.append(f'<li><a href="#{i}"><span class="n">{num.group(1) if num else ""}</span>{short}</a>')
    nav_html.append('</li>')
nav_html = '\n'.join(nav_html)

# book index grouped by volume label
groups = []
for vol, name, bid in books:
    if not groups or groups[-1][0] != vol:
        groups.append([vol, []])
    groups[-1][1].append((name, bid))
idx = []
for vol, items in groups:
    v = re.sub(r':.*$', '', vol)
    vt = vol.split(':', 1)[1].strip() if ':' in vol else ''
    chips = ''.join(f'<a class="chip" href="#{b}" data-name="{html.escape(slug(n).replace("-", " "))}">{n}</a>' for n, b in items)
    idx.append(f'<div class="vol"><div class="vol-h"><span class="vol-n">{v}</span><span class="vol-t">{vt}</span></div><div class="chips">{chips}</div></div>')
idx_html = '\n'.join(idx)
print(len(books), 'book entries;', len(nav), 'sections', file=sys.stderr)

tpl = open(sys.argv[3], encoding='utf-8').read()
page = tpl.replace('{{INTRO}}', intro).replace('{{NAV}}', nav_html).replace('{{INDEX}}', idx_html).replace('{{BODY}}', h).replace('{{NBOOKS}}', str(len(books)))
open(out, 'w', encoding='utf-8').write(page)
