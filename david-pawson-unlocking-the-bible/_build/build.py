import re, sys, unicodedata, html
import markdown

src, out = sys.argv[1], sys.argv[2]
md = open(src, encoding='utf-8').read()

def slug(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('đ', 'd').replace('Đ', 'D')
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()
    return s

# drop title block, intro quote, TOC; handled by hero/nav
body_md = md.split('## 1. Về tác giả', 1)[1]
body_md = '## 1. Về tác giả' + body_md
intro = re.search(r'^> (.+)$', md, re.M).group(1)

h = markdown.markdown(body_md, extensions=['tables', 'sane_lists'])
h = h.replace('<hr />', '')

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

# book paragraphs: <p><strong>Name (n bài).</strong> ...
books = []  # (volume label, name, id)
cur_vol = ''
def walk(text):
    global cur_vol
    out = []
    pos = 0
    for m in re.finditer(r'<h3 id="([^"]+)">(.*?)</h3>|<p><strong>([^<]+?)</strong>', text):
        if m.group(1):
            cur_vol = m.group(2)
            continue
        label = m.group(3)
        if not re.search(r'\(\d+ bài|\(1 bài, chung|^Giô-ên\.$|^Nhập đề', label):
            continue
        name = re.sub(r'\s*\(.*$', '', label).rstrip('.')
        bid = 'sach-' + slug(name)
        books.append((cur_vol, name, bid))
        out.append((m.start(), bid))
    return out
marks = walk(h)
for start, bid in reversed(marks):
    h = h[:start] + f'<p class="book" id="{bid}">' + h[start+3:]

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
