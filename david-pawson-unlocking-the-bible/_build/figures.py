"""Hình minh hoạ SVG cho trang tuyển tập. Mỗi hình thay cho một dòng <!-- fig:ten --> trong tuyen-tap.md.

Màu lấy qua class (định nghĩa trong tpl.html) để tự đổi theo giao diện sáng/tối:
tx = chữ chính, tm = chữ phụ, ta = chữ màu nhấn, bx = hộp thường, bxa = hộp nhấn,
ln = đường nối, lna = đường nối màu nhấn, bar = cột biểu đồ, mk = đầu mũi tên.
"""
from html import escape

FS = 14  # cỡ chữ cơ sở trong hệ toạ độ viewBox


def T(x, y, s, cls='tx', anchor='start', size=FS, weight=None):
    w = f' font-weight="{weight}"' if weight else ''
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" text-anchor="{anchor}"{w}>{escape(s)}</text>'


def box(x, y, w, h, lines, cls='bx', tcls='tx', size=FS, first_bold=False, rx=8):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>']
    lh = size * 1.3
    y0 = y + h / 2 - (len(lines) - 1) * lh / 2 + size * 0.35
    for i, s in enumerate(lines):
        out.append(T(x + w / 2, round(y0 + i * lh, 1), s, tcls if i == 0 or not first_bold else 'tm', 'middle', size if i == 0 or not first_bold else size - 1, 600 if (first_bold and i == 0) else None))
    return ''.join(out)


def head(x, y, ang, cls):
    import math
    c, d = math.cos(ang), math.sin(ang)
    p = [(x, y), (x - 9 * c + 4.5 * d, y - 9 * d - 4.5 * c), (x - 9 * c - 4.5 * d, y - 9 * d + 4.5 * c)]
    return '<polygon points="' + ' '.join(f'{round(a, 1)},{round(b, 1)}' for a, b in p) + f'" class="{"mka" if cls == "lna" else "mk"}"/>'


def arrow(fid, x1, y1, x2, y2, label=None, lx=None, ly=None, cls='ln', dash=False, lcls='tm', anchor='middle', size=12):
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    ex, ey = x2 - 8 * math.cos(ang), y2 - 8 * math.sin(ang)
    d = ' stroke-dasharray="5 4"' if dash else ''
    s = f'<line x1="{x1}" y1="{y1}" x2="{round(ex, 1)}" y2="{round(ey, 1)}" class="{cls}"{d}/>' + head(x2, y2, ang, cls)
    if label:
        s += T(lx if lx is not None else (x1 + x2) / 2, ly if ly is not None else (y1 + y2) / 2 - 6, label, lcls, anchor, size)
    return s


def curve(x1, y1, x2, y2, cls='ln'):
    """Đường cong ra ngang, vào ngang từ trái sang phải, có đầu mũi tên."""
    m = (x1 + x2) / 2
    return f'<path d="M{x1},{y1} C{m},{y1} {m},{y2} {x2 - 8},{y2}" class="{cls}" fill="none"/>' + head(x2, y2, 0, cls)


def defs(fid):
    return ''


def fig(fid, w, h, label, body, caption, minw=480):
    return (f'<figure class="fig" id="hinh-{fid}"><div class="fig-sc"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}" style="min-width:{minw}px">'
            f'{defs(fid)}{body}</svg></div><figcaption>{caption}</figcaption></figure>')


F = {}

# 1. Cuộc đời tác giả -----------------------------------------------------------
def yx(y):
    return round(40 + (y - 1930) * 560 / 90, 1)

b = [f'<line x1="40" y1="100" x2="600" y2="100" class="ln"/>']
for yr in (1930, 1950, 1970, 1990, 2010):
    b.append(f'<line x1="{yx(yr)}" y1="100" x2="{yx(yr)}" y2="106" class="ln"/>' + T(yx(yr), 122, str(yr), 'tm', 'middle', 12))
spans = [(1956, 1959, 'bxa'), (1961, 1968, 'bxa'), (1968, 1980, 'bxa'), (1980, 2020, 'bx')]
for a, z, c in spans:
    b.append(f'<rect x="{yx(a)}" y="93" width="{round(yx(z) - yx(a), 1)}" height="14" rx="3" class="{c}"/>')
for y, row, s, anchor in [(1930, 70, '1930 · sinh ra', 'start'), (1957.5, 46, '1956–59 · tuyên úy RAF ở Aden', 'middle'),
                          (2003, 70, '2003 · sách gộp một cuốn', 'middle'), (2017, 46, '2017 · bản có biểu đồ', 'end')]:
    x = yx(y)
    tx = x if anchor != 'end' else yx(2020)
    b.append(f'<line x1="{x}" y1="{row + 6}" x2="{x}" y2="92" class="ln" stroke-dasharray="2 3"/>' + T(tx, row, s, 'tx', anchor, 13))
b.append(f'<circle cx="{yx(1930)}" cy="100" r="5" class="dot"/><circle cx="{yx(2020)}" cy="100" r="5" class="dot"/>')
for y, row, s, anchor in [(1964.5, 150, 'Gold Hill 1961–68', 'middle'), (1974, 172, 'Millmead, Guildford', 'middle'), (2000, 150, 'Dạy lưu động hơn 120 nước', 'middle'), (2020, 172, '2020 · qua đời, 90 tuổi', 'end')]:
    x = yx(y)
    b.append(f'<line x1="{x}" y1="108" x2="{x}" y2="{row - 13}" class="ln" stroke-dasharray="2 3"/>' + T(x if anchor != 'end' else yx(2020), row, s, 'tx', anchor, 13))
F['doi'] = fig('doi', 640, 190, 'Dòng thời gian cuộc đời David Pawson từ 1930 đến 2020', ''.join(b),
               'Cuộc đời và chức vụ của David Pawson. Thanh màu nhấn là các giai đoạn chăn hội thánh; năm rời Millmead được các nguồn ghi là 1979 hoặc 1981.')

# 2. Từ bài giảng đến các định dạng -------------------------------------------------
b = [box(5, 75, 175, 60, ['Thập niên 1960–70', 'dạy từng dòng, Guildford'], 'bx', first_bold=True),
     box(235, 75, 160, 60, ['Bài tổng quan', 'cho từng sách'], 'bxa', first_bold=True),
     arrow('dd', 180, 105, 233, 105, 'chắt lọc', ly=97),
     box(440, 10, 195, 52, ['Sách 8 tập, bản gộp', 'Andy Peck chép thành văn'], 'bx', first_bold=True),
     box(440, 79, 195, 52, ['Video, CD, DVD', 'YouTube, miễn phí'], 'bx', first_bold=True),
     box(440, 148, 195, 52, ['Podcast 98 tập', 'từ Sáng Thế đến Khải Huyền'], 'bx', first_bold=True),
     curve(395, 105, 438, 36), arrow('dd', 395, 105, 438, 105), curve(395, 105, 438, 174)]
F['dinhdang'] = fig('dinhdang', 640, 210, 'Bài giảng tổng quan từng sách được phát hành thành sách, video và podcast', ''.join(b),
                    'Cùng một nội dung đi ra ba dạng: sách (8 tập, rồi bản gộp), video và podcast.')

# 3. Ngữ cảnh lồng nhau -------------------------------------------------------------
b = [f'<rect x="10" y="10" width="360" height="190" rx="12" class="bx"/>', T(26, 34, 'Bối cảnh lịch sử và địa lý', 'tm', size=13),
     f'<rect x="40" y="48" width="300" height="130" rx="10" class="bx"/>', T(56, 72, 'Cả cuốn sách: ai viết, cho ai, vì sao', 'tm', size=13),
     box(110, 98, 160, 50, ['Câu Kinh Thánh'], 'bxa', 'ta'),
     arrow('nc', 372, 123, 448, 123, 'rút ra', ly=115, dash=True),
     f'<rect x="450" y="98" width="170" height="50" rx="8" class="bx" stroke-dasharray="5 4"/>', T(535, 128, 'Câu đứng một mình', 'tx', 'middle'),
     T(535, 172, 'dễ hiểu sai: "text people"', 'tm', 'middle', 13)]
F['ngucanh'] = fig('ngucanh', 640, 210, 'Mỗi câu nằm trong ngữ cảnh cuốn sách, mỗi cuốn sách nằm trong ngữ cảnh lịch sử', ''.join(b),
                   'Pawson đọc từ ngoài vào trong: lịch sử, rồi cả cuốn sách, rồi mới đến câu. Một câu bị rút khỏi hai lớp khung đó dễ bị hiểu sai.')

# 4. Hy Lạp và Hê-bơ-rơ ---------------------------------------------------------------
b = [T(150, 22, 'Tư duy Hy Lạp (phương Tây thừa hưởng)', 'tx', 'middle', 13, 600),
     box(20, 50, 115, 70, ['Thuộc linh', 'thiêng liêng'], 'bx', first_bold=True),
     box(165, 50, 115, 70, ['Thể xác', 'thế tục'], 'bx', first_bold=True),
     f'<line x1="150" y1="40" x2="150" y2="130" class="wall"/>', T(150, 152, 'bị tách rời, thể xác bị xem là thấp kém', 'tm', 'middle', 12),
     T(485, 22, 'Tư duy Hê-bơ-rơ (Kinh Thánh)', 'ta', 'middle', 13, 600),
     f'<rect x="340" y="34" width="290" height="104" rx="12" class="bxa"/>', T(485, 54, 'Một Đức Chúa Trời tạo nên cả hai', 'ta', 'middle', 12),
     box(356, 66, 115, 58, ['Thuộc linh'], 'bx'), box(499, 66, 115, 58, ['Thể xác'], 'bx'),
     f'<line x1="471" y1="95" x2="499" y2="95" class="lna"/>', T(485, 152, 'thuộc về nhau, và đều tốt lành', 'tm', 'middle', 12)]
F['hylap'] = fig('hylap', 640, 165, 'So sánh tư duy Hy Lạp tách thuộc linh khỏi thể xác với tư duy Hê-bơ-rơ xem cả hai là một', ''.join(b),
                 'Chìa khóa Pawson dùng cho Nhã Ca, Châm Ngôn, Cô-rinh-tô, Giăng và 1 Giăng: "trước mặt Đức Chúa Trời, không có gì là thế tục ngoại trừ tội lỗi."')

# 5. Văn xuôi và thơ ---------------------------------------------------------------
b = [box(20, 15, 150, 50, ['Tâm trí Chúa'], 'bx'), arrow('vt', 172, 40, 466, 40, 'Văn xuôi: truyền ý nghĩ', ly=32), box(470, 15, 150, 50, ['Tâm trí ta'], 'bx'),
     box(20, 90, 150, 50, ['Lòng Chúa'], 'bxa', 'ta'), arrow('vt', 172, 115, 466, 115, 'Thơ: truyền cảm xúc, chạm tới ý chí', ly=107, cls='lna', lcls='ta'), box(470, 90, 150, 50, ['Lòng ta'], 'bxa', 'ta'),
     T(320, 168, 'Thơ Hê-bơ-rơ không vần; dùng nhịp và cặp câu lặp ý', 'tm', 'middle', 12)]
F['tho'] = fig('tho', 640, 180, 'Văn xuôi truyền ý nghĩ từ tâm trí đến tâm trí, thơ truyền cảm xúc từ lòng đến lòng', ''.join(b),
               'Vì vậy nên dùng bản Kinh Thánh trình bày rõ phần thơ, và đọc to. Ma-la-chi toàn văn xuôi là một dấu hiệu Pawson phân tích.')

# 6. Sáu cấp độ đọc ---------------------------------------------------------------
lv = [('1', 'Giai thoại', 'một câu chuyện hay'), ('2', 'Tĩnh nguyện', 'một lời cho riêng mình'), ('3', 'Nhân vật', 'An-ne, A-bi-ga-in, Đa-vít'),
      ('4', 'Lịch sử Israel', 'dân tộc phát triển ra sao'), ('5', 'Phê bình', 'Pawson cảnh giác'), ('6', 'Thần học', 'Đức Chúa Trời là nhân vật chính')]
b = []
for i, (n, a, c) in enumerate(lv):
    y = 10 + (5 - i) * 34
    w = 70 + i * 46
    cls, tc = ('bxa', 'ta') if n == '6' else ('bx', 'tx')
    b.append(f'<rect x="10" y="{y}" width="{w}" height="28" rx="5" class="{cls}"/>' + T(24, y + 19, n, 'ta' if n == '6' else 'tm', size=13, weight=600))
    b.append(T(w + 22, y + 19, a, tc, size=14, weight=600) + T(w + 22 + len(a) * 8.6 + 12, y + 19, c, 'tm', size=12))
F['capdo'] = fig('capdo', 640, 214, 'Sáu cấp độ đọc một câu chuyện Kinh Thánh, cao nhất là cấp độ thần học', ''.join(b),
                 'Sáu cấp độ đọc một câu chuyện (bài giảng 2 Sa-mu-ên). Pawson muốn người đọc leo tới bậc 6: hỏi câu chuyện nói gì về Đức Chúa Trời.')

# 7. Vòng luẩn quẩn và đường thẳng --------------------------------------------------
cx, cy, r = 150, 105, 62
b = [T(150, 20, 'Các Quan Xét: vòng luẩn quẩn', 'tx', 'middle', 13, 600),
     f'<circle cx="{cx}" cy="{cy}" r="{r}" class="ln" fill="none"/>',
     f'<path d="M{cx + r},{cy - 6} l-5,10 l10,0 z" class="mk"/>', f'<path d="M{cx - r},{cy + 6} l-5,-10 l10,0 z" class="mk"/>',
     T(cx, cy - r - 8, 'bỏ Chúa', 'tm', 'middle', 12), T(cx + r + 8, cy + 4, 'bị áp bức', 'tm', 'start', 12),
     T(cx, cy + r + 18, 'kêu cầu', 'tm', 'middle', 12), T(cx - r - 8, cy + 4, 'được giải cứu', 'tm', 'end', 12),
     T(cx, cy + 5, 'lặp lại', 'tm', 'middle', 12),
     T(480, 20, 'Ru-tơ: đường thẳng có đích', 'ta', 'middle', 13, 600)]
names = ['Ru-tơ', 'Ô-bết', 'Gie-sê', 'Đa-vít', '… Đấng Christ']
for i, n in enumerate(names):
    y = 44 + i * 30
    last = i == len(names) - 1
    b.append(f'<circle cx="370" cy="{y}" r="6" class="{"dot" if last else "dotb"}"/>' + T(386, y + 5, n, 'ta' if last else 'tx', size=13, weight=600 if last else None))
    if not last:
        b.append(arrow('vl', 370, y + 8, 370, y + 23, cls='lna'))
b.append(T(480, 200, 'sự cứu chuộc đưa ra khỏi vòng quay', 'tm', 'middle', 12))
F['vongtron'] = fig('vongtron', 640, 210, 'Các Quan Xét là một vòng lặp, Ru-tơ là một dòng dõi tiến về Đấng Christ', ''.join(b),
                    'Hai sách vốn là một trong Kinh Thánh Hê-bơ-rơ. Đời sống xa Chúa thành vòng lặp; Ru-tơ mở ra dòng dõi dẫn đến vua Đa-vít và Đấng Christ.')

# 8. Biểu đồ số bài giảng theo tập ----------------------------------------------------
rows = [('Tổng quan Cựu Ước', 1), ('Tập 1 · Luật pháp', 14), ('Tập 2 · Đất và vương quốc', 8), ('Tập 3 · Thi ca, khôn ngoan', 9),
        ('Tập 4–5 · Các tiên tri, lưu đày', 28), ('Tập 6 · Phúc Âm, Công Vụ', 8), ('Tập 7 · Phao-lô', 15), ('Tập 8 · Thư chung, Khải Huyền', 15)]
X0, SC, RH = 230, 360 / 28, 30
b = []
for g in (0, 7, 14, 21, 28):
    gx = round(X0 + g * SC, 1)
    b.append(f'<line x1="{gx}" y1="30" x2="{gx}" y2="{30 + len(rows) * RH + 34}" class="grid"/>' + T(gx, 20, str(g), 'tm', 'middle', 11))
for i, (n, v) in enumerate(rows):
    y = 34 + i * RH + (30 if i >= 5 else 0)
    w = round(v * SC, 1)
    b.append(f'<g class="hv"><title>{escape(n)}: {v} bài</title><rect x="{X0 - 225}" y="{y - 3}" width="{225 + w + 40}" height="{RH}" class="hit"/>'
             f'<rect x="{X0}" y="{y}" width="{w}" height="{RH - 8}" rx="3" class="bar"/></g>')
    b.append(T(X0 - 10, y + 16, n, 'tx', 'end', 13))
    b.append(T(X0 + w + 6, y + 16, str(v), 'tx', 'start', 13, 600))
sep = 34 + 5 * RH + 10
b.append(f'<line x1="5" y1="{sep}" x2="640" y2="{sep}" class="ln" stroke-dasharray="3 3"/>')
b.append(T(8, sep - 6, '↑ Cựu Ước: 60 bài', 'tm', 'start', 12) + T(8, sep + 17, '↓ Tân Ước: 38 bài', 'tm', 'start', 12))
F['bieudo'] = fig('bieudo', 640, 312, 'Biểu đồ cột ngang: số bài giảng podcast theo từng tập, nhiều nhất là các sách tiên tri với 28 bài', ''.join(b),
                  'Số bài giảng podcast theo từng tập, đếm từ danh sách 98 tập chính thức. Tập 4 và 5 được gộp vì bản podcast không ghi ranh giới giữa hai tập. Rê chuột lên cột để xem số liệu.')

# 9. Phục Truyền: sở hữu và cư ngụ ---------------------------------------------------
b = [box(10, 80, 150, 60, ['Đức Chúa Trời', 'ban xứ làm quà'], 'bx', first_bold=True),
     arrow('pt', 162, 110, 233, 110, 'sở hữu', ly=102), T(197, 128, 'vô điều kiện', 'tm', 'middle', 11),
     box(235, 80, 150, 60, ['Miền đất hứa', 'luôn thuộc về Israel'], 'bxa', 'ta', first_bold=True),
     curve(385, 110, 448, 45, 'lna'), curve(385, 110, 448, 175),
     T(418, 74, 'giữ luật', 'ta', 'end', 12), T(418, 156, 'bỏ luật', 'tm', 'end', 12),
     box(450, 20, 180, 50, ['Được ở trong xứ', 'hưởng phước'], 'bxa', 'ta', first_bold=True),
     box(450, 150, 180, 50, ['Mất quyền cư ngụ', 'bị lưu đày'], 'bx', first_bold=True)]
F['phuctruyen'] = fig('phuctruyen', 640, 215, 'Quyền sở hữu miền đất là vô điều kiện, quyền cư ngụ phụ thuộc việc giữ luật', ''.join(b),
                      '"Quyền sở hữu là vô điều kiện, quyền cư ngụ là có điều kiện." Theo Pawson, đây là chìa khóa của cả lịch sử Israel về sau: mọi tiên tri đều quy về Phục Truyền.')

# 10. Thi Thiên 22–24 ----------------------------------------------------------------
b = [box(10, 20, 180, 60, ['Thi Thiên 22', 'Đấng Cứu Rỗi · thập tự'], 'bx', first_bold=True),
     arrow('tt', 192, 50, 228, 50), box(230, 20, 180, 60, ['Thi Thiên 23', 'Đấng Chăn Giữ'], 'bx', first_bold=True),
     arrow('tt', 412, 50, 448, 50), box(450, 20, 180, 60, ['Thi Thiên 24', 'Đấng Tể Trị · Vua vinh hiển'], 'bxa', 'ta', first_bold=True),
     T(320, 110, 'Phải qua thập tự giá trước, rồi mới có quyền gọi Ngài là Đấng Chăn Giữ', 'tm', 'middle', 12)]
F['thithien'] = fig('thithien', 640, 125, 'Thi Thiên 22, 23, 24 đọc liền nhau: Cứu Rỗi, Chăn Giữ, Tể Trị', ''.join(b),
                    'Một ví dụ về các nhóm thi thiên nên đọc cùng nhau.')

# 11. Ê-sai, Kinh Thánh thu nhỏ ------------------------------------------------------
S = 600 / 66
b = []
for i, (lab, a, z) in enumerate([('Kinh Thánh · 66 sách', 'Cựu Ước 39', 'Tân Ước 27'), ('Ê-sai · 66 chương', 'chương 1–39', 'chương 40–66')]):
    y = 30 + i * 80
    b.append(T(20, y - 8, lab, 'tx', size=13, weight=600))
    b.append(f'<rect x="20" y="{y}" width="{round(39 * S - 2, 1)}" height="34" rx="4" class="bx"/>' + T(20 + 39 * S / 2, y + 22, a, 'tx', 'middle', 13))
    b.append(f'<rect x="{round(20 + 39 * S, 1)}" y="{y}" width="{round(27 * S, 1)}" height="34" rx="4" class="bxa"/>' + T(20 + 39 * S + 27 * S / 2, y + 22, z, 'ta', 'middle', 13))
b.append(T(20 + 39 * S / 2, 172, 'phán xét · Chúa như lửa', 'tm', 'middle', 12) + T(20 + 39 * S + 27 * S / 2, 172, 'an ủi · Chúa như Cha', 'tm', 'middle', 12))
F['esai'] = fig('esai', 640, 185, 'Ê-sai có 66 chương chia 39 và 27, giống Kinh Thánh có 66 sách chia 39 và 27', ''.join(b),
                'Pawson gọi Ê-sai là "Kinh Thánh thu nhỏ": cùng tỷ lệ 39 và 27, và phần sau chuyển từ phán xét sang an ủi.')

# 12. Các tiên tri và cuộc lưu đày ----------------------------------------------------
cols = [(10, 300, 'Trước lưu đày', 'cảnh báo', ['Áp-đia', 'Giô-ên', 'Giô-na', 'A-mốt', 'Ô-sê', 'Ê-sai', 'Mi-chê', 'Na-hum', 'Sô-phô-ni', 'Ha-ba-cúc', 'Giê-rê-mi'], 'bx'),
        (320, 140, 'Trong lưu đày', 'an ủi', ['Ca Thương', 'Ê-xê-chi-ên', 'Đa-ni-ên'], 'bx'),
        (470, 160, 'Sau lưu đày', 'khích lệ', ['A-ghê', 'Xa-cha-ri', 'Ma-la-chi'], 'bx')]
b = []
for x, w, h1, h2, ns, c in cols:
    b.append(f'<rect x="{x}" y="58" width="{w}" height="150" rx="10" class="{c}"/>' + T(x + 14, 82, h1, 'tx', size=14, weight=600) + T(x + 14, 100, h2, 'ta', size=12))
    per = 3 if w > 200 else 1
    cw = (w - 28) / per
    for i, n in enumerate(ns):
        b.append(T(round(x + 14 + (i % per) * cw, 1), 124 + (i // per) * 20, n, 'tx', size=13))
for x, s1, s2 in [(160, '722 TCN', 'Samari sụp đổ'), (315, '586 TCN', 'Giê-ru-sa-lem sụp đổ'), (465, '538 TCN', 'Si-ru cho hồi hương')]:
    b.append(f'<line x1="{x}" y1="40" x2="{x}" y2="58" class="ln"/><circle cx="{x}" cy="40" r="4" class="dot"/>' + T(x, 16, s1, 'tx', 'middle', 12, 600) + T(x, 31, s2, 'tm', 'middle', 11))
b.append(T(550, 226, '→ 400 năm im lặng', 'tm', 'middle', 12))
F['tientri'] = fig('tientri', 640, 235, 'Các tiên tri xếp theo thời điểm so với cuộc lưu đày: trước để cảnh báo, trong để an ủi, sau để khích lệ', ''.join(b),
                   'Pawson nhóm các tiên tri theo cuộc lưu đày. Các mốc năm là mốc lịch sử thông dụng; thứ tự tên trong mỗi cột không phải niên đại chính xác, và hình không theo tỷ lệ thời gian.')

# 13. Bốn sách Phúc Âm ---------------------------------------------------------------
b = [T(10, 70, 'Cho người', 'tm', size=12), T(10, 86, 'chưa tin', 'tm', size=12), T(10, 170, 'Cho Cơ Đốc', 'tm', size=12), T(10, 186, 'nhân', 'tm', size=12),
     box(90, 40, 220, 70, ['Mác · viết đầu tiên', 'hành động · lời giảng Phi-e-rơ'], 'bxa', 'ta', first_bold=True),
     box(400, 40, 230, 70, ['Lu-ca', 'Cứu Chúa của mọi người'], 'bx', first_bold=True),
     box(90, 140, 220, 70, ['Ma-thi-ơ', 'Vua dân Do Thái · môn đồ hóa'], 'bx', first_bold=True),
     box(400, 140, 230, 70, ['Giăng', 'bên trong Chúa Giê-xu · Ngôi Lời'], 'bx', first_bold=True),
     arrow('pa', 312, 75, 398, 75, 'dùng khung', ly=67, cls='lna', lcls='ta'), arrow('pa', 200, 112, 200, 138, 'dùng khung', lx=208, ly=129, cls='lna', lcls='ta', anchor='start')]
F['phucam'] = fig('phucam', 640, 220, 'Bốn sách Phúc Âm theo độc giả: Mác và Lu-ca cho người chưa tin, Ma-thi-ơ và Giăng cho Cơ Đốc nhân', ''.join(b),
                  'Bốn góc nhìn cho bốn nhóm độc giả. Mác viết trước; Ma-thi-ơ và Lu-ca dựa trên khung của Mác rồi thêm tư liệu riêng.')

# 14. Công Vụ: vì sao, và bốn bước ---------------------------------------------------
b = [box(10, 15, 190, 50, ['Phúc Âm', 'trước thập tự: quá sớm'], 'bx', first_bold=True),
     box(225, 15, 190, 50, ['Công Vụ', 'người tìm đạo được dẫn dắt'], 'bxa', 'ta', first_bold=True),
     box(440, 15, 190, 50, ['Thư tín, Khải Huyền', 'cho người đã tin: quá muộn'], 'bx', first_bold=True),
     T(320, 100, 'Sau Lễ Ngũ Tuần, sự tái sinh gồm bốn bước:', 'tm', 'middle', 12)]
steps = ['Ăn năn tội', 'Tin Chúa Giê-xu', 'Báp-têm bằng nước', 'Nhận Thánh Linh']
for i, s in enumerate(steps):
    x = 10 + i * 158
    b.append(box(x, 115, 146, 44, [s], 'bxa', 'ta', size=13))
    if i < 3:
        b.append(arrow('cv', x + 146, 137, x + 158, 137, cls='lna'))
F['congvu'] = fig('congvu', 640, 170, 'Công Vụ là sách duy nhất cho thấy cách hướng dẫn người tìm đạo, qua bốn bước ăn năn, tin, báp-têm, nhận Thánh Linh', ''.join(b),
                  'Vì sao Công Vụ đặc biệt theo Pawson, và bốn bước của "sự tái sinh bình thường".')

# 15. Ga-la-ti: con đường và hai bên vực ----------------------------------------------
b = [f'<path d="M10,60 L10,150 L200,150 L200,60" class="ditch"/>', f'<path d="M440,60 L440,150 L630,150 L630,60" class="ditch"/>',
     f'<rect x="200" y="50" width="240" height="20" rx="3" class="bxa"/>',
     T(105, 90, 'Chủ nghĩa luật pháp', 'tx', 'middle', 14, 600), T(105, 110, 'được cứu nhờ việc lành', 'tm', 'middle', 12), T(105, 128, '"không được tự do phạm tội"', 'tm', 'middle', 12),
     T(535, 90, 'Sự phóng túng', 'tx', 'middle', 14, 600), T(535, 110, 'được cứu, khỏi cần việc lành', 'tm', 'middle', 12), T(535, 128, '"được tự do phạm tội"', 'tm', 'middle', 12),
     T(320, 34, 'Tự do trong Thánh Linh', 'ta', 'middle', 14, 600), T(320, 96, 'được cứu để làm việc lành', 'tm', 'middle', 12), T(320, 114, 'tự do để không phạm tội', 'tm', 'middle', 12)]
F['galati'] = fig('galati', 640, 165, 'Tự do trong Thánh Linh là con đường hẹp giữa hai bên vực: chủ nghĩa luật pháp và sự phóng túng', ''.join(b),
                  'Bộ ba Pawson dùng cho Ga-la-ti, Gia-cơ và Giu-đe: cả luật pháp lẫn phóng túng đều là kẻ thù của tự do.')

# 16. Ê-phê-sô hai nửa -----------------------------------------------------------------
b = [box(10, 20, 290, 70, ['Chương 1–3 · làm vào trong', 'giáo lý: ta được cứu BỞI điều gì'], 'bx', first_bold=True),
     arrow('ep', 302, 55, 338, 55),
     box(340, 20, 290, 70, ['Chương 4–6 · làm ra ngoài', 'bổn phận: ta được cứu ĐỂ làm gì'], 'bxa', 'ta', first_bold=True),
     T(320, 115, 'Thứ tự không đảo được: phải được cứu rồi mới sống đời sống Cơ Đốc', 'tm', 'middle', 12)]
F['ephe'] = fig('ephe', 640, 128, 'Ê-phê-sô chia hai nửa: giáo lý rồi đến bổn phận', ''.join(b), '"Chúng ta không được cứu bởi việc lành, nhưng được cứu để làm việc lành."')

# 17. Hê-bơ-rơ: tốt hơn ---------------------------------------------------------------
b = [T(110, 18, 'Hình bóng (Cựu Ước)', 'tm', 'middle', 12)]
for i, s in enumerate(['Các tiên tri', 'Các thiên sứ', 'Môi-se, Giô-suê', 'Các thầy tế lễ']):
    y = 30 + i * 44
    b.append(box(20, y, 180, 34, [s], 'bx', size=13))
    b.append(curve(202, y + 17, 418, 104, 'lna'))
b.append(T(330, 70, 'tốt hơn', 'ta', 'middle', 12))
b.append(box(420, 74, 210, 60, ['Chúa Giê-xu', 'thực thể'], 'bxa', 'ta', first_bold=True))
F['hebo'] = fig('hebo', 640, 210, 'Hê-bơ-rơ: Chúa Giê-xu tốt hơn các tiên tri, thiên sứ, lãnh tụ xưa và thầy tế lễ', ''.join(b),
                'Từ khóa của Hê-bơ-rơ là "tốt hơn": thực thể tốt hơn hình bóng.')

# 18. Khải Huyền: trình tự tương lai ---------------------------------------------------
ev = [('Hoạn nạn', '3 năm rưỡi', 'bx'), ('Tái lâm', 'Mê-ghi-đô', 'bxa'), ('Thiên hy niên', '1.000 năm', 'bxa'), ('Phán xét', 'Sách Sự Sống', 'bxa'), ('Trời mới', 'đất mới', 'bxa')]
b = []
for i, (a, c, cls) in enumerate(ev):
    x = 10 + i * 126
    b.append(box(x, 90, 112, 60, [a, c], cls, 'ta' if cls == 'bxa' else 'tx', first_bold=True, size=13))
    if i < 4:
        b.append(arrow('kh', x + 113, 120, x + 125, 120, cls='lna'))
b.append(arrow('kh', 66, 88, 66, 26, dash=True))
b.append(f'<line x1="56" y1="50" x2="76" y2="66" class="cross"/><line x1="76" y1="50" x2="56" y2="66" class="cross"/>')
b.append(T(84, 34, 'Cất lên trước hoạn nạn? Pawson phản đối:', 'tx', size=12, weight=600))
b.append(T(84, 50, 'hội thánh đi qua hoạn nạn, nhiều người tử đạo', 'tm', size=12))
b.append(T(320, 178, 'Bốn sự kiện lớn của phần cuối sách, đọc theo đúng thứ tự khải tượng', 'tm', 'middle', 12))
F['khaihuyen'] = fig('khaihuyen', 640, 190, 'Trình tự tương lai theo cách đọc Khải Huyền của Pawson: hoạn nạn, tái lâm, thiên hy niên, phán xét, trời mới đất mới', ''.join(b),
                     'Cách Pawson đọc Khải Huyền: tiền thiên hy niên, không có sự cất lên trước hoạn nạn. Đây là một trong nhiều trường phái giải nghĩa.')

# 19. Sáng Thế Ký: hai phần -------------------------------------------------------
b = [f'<rect x="20" y="62" width="130" height="40" rx="4" class="bx"/>' + T(85, 87, 'chương 1–11', 'tx', 'middle', 13),
     T(85, 52, 'Cả thế giới', 'tx', 'middle', 13, 600)]
for x1, x2, name, rng in [(152, 308, 'Áp-ra-ham', '12–25'), (310, 452, 'Y-sác, Gia-cốp', '25–36'), (454, 620, 'Giô-sép', '37–50')]:
    b.append(f'<rect x="{x1}" y="62" width="{x2 - x1}" height="40" rx="4" class="bxa"/>' + T((x1 + x2) / 2, 87, rng, 'ta', 'middle', 13))
    b.append(T((x1 + x2) / 2, 124, name, 'tx', 'middle', 13, 600))
b.append(T(386, 52, 'Một gia đình qua bốn thế hệ', 'ta', 'middle', 13, 600))
b.append(T(20, 124, 'Sáng tạo, sa ngã', 'tm', 'start', 12) + T(20, 141, 'Ca-in, Nô-ê, Nim-rốt', 'tm', 'start', 12))
b.append(f'<line x1="30" y1="26" x2="30" y2="60" class="ln" stroke-dasharray="2 3"/>' + T(36, 22, '1:1–2:3 · được Chúa trực tiếp truyền cho Môi-se', 'tm', 'start', 12))
F['sangthe'] = fig('sangthe', 640, 155, 'Sáng Thế Ký: chương 1 đến 11 nói về cả thế giới, chương 12 đến 50 nói về một gia đình qua bốn thế hệ', ''.join(b),
                   'Độ dài mỗi khối theo số chương. "Đức Chúa Trời bắt đầu sáng tạo bằng một người và bắt đầu cứu chuộc bằng một người."')

# 20. Xuất Ê-díp-tô: hai nửa ------------------------------------------------------
b = [box(10, 15, 290, 70, ['Nửa đầu · điều Chúa LÀM', 'giải cứu khỏi Ai Cập: ân điển'], 'bx', first_bold=True),
     arrow('xh', 302, 50, 338, 50),
     box(340, 15, 290, 70, ['Nửa sau · điều Chúa PHÁN', 'luật pháp: sống biết ơn'], 'bxa', 'ta', first_bold=True),
     T(320, 112, 'Được cứu chuộc trước, rồi mới được dạy sống đúng', 'tm', 'middle', 12)]
F['xuathanh'] = fig('xuathanh', 640, 125, 'Xuất Ê-díp-tô Ký chia hai nửa: điều Chúa làm, rồi điều Chúa phán', ''.join(b),
                    'Cùng thứ tự với Ê-phê-sô trong Tân Ước: ân điển đi trước, đời sống vâng phục theo sau.')

# 21. Dân Số Ký: hành trình 40 năm ----------------------------------------------------
import math as _m
b = [box(10, 80, 130, 52, ['Núi Si-na-i', 'điều tra ~600.000'], 'bx', first_bold=True),
     arrow('ds', 142, 106, 193, 106),
     box(195, 80, 170, 52, ['Ca-đe', '10/12 thám tử: không thể'], 'bx', first_bold=True),
     f'<path d="M367,106 C400,10 440,200 470,114" class="ln" stroke-dasharray="5 4" fill="none"/>',
     head(476, 106, _m.atan2(-86, 34), 'ln'),
     T(420, 50, '40 năm trong đồng vắng', 'tx', 'middle', 13, 600),
     box(480, 80, 150, 52, ['Bờ sông Giô-đanh', 'điều tra ~600.000'], 'bxa', 'ta', first_bold=True),
     T(320, 188, 'Thế hệ cũ qua đời; chỉ Giô-suê và Ca-lép còn lại', 'tm', 'middle', 12)]
F['danso'] = fig('danso', 640, 200, 'Dân Số Ký: từ núi Si-na-i đến Ca-đe, rồi 40 năm lang thang trước khi đến bờ Giô-đanh', ''.join(b),
                 'Hai cuộc điều tra dân số cho cùng một con số: dấu hiệu Chúa không ban phước. Theo Pawson, hai phần ba sách "lẽ ra không bao giờ xảy ra".')

# 22. Các Vua: vương quốc chia đôi -------------------------------------------------
b = [box(5, 92, 170, 56, ['Vương quốc thống nhất', 'Sa-lô-môn xây đền thờ'], 'bx', first_bold=True),
     curve(175, 120, 228, 50), curve(175, 120, 228, 180),
     box(230, 20, 215, 60, ['Bắc: Israel, 10 chi phái', 'mọi vua đều xấu · Ê-li, Ê-li-sê'], 'bx', first_bold=True),
     box(230, 150, 215, 60, ['Nam: Giu-đa, 2 chi phái', 'có vua tốt: Ê-xê-chia, Giô-si-a'], 'bxa', 'ta', first_bold=True),
     arrow('cv2', 447, 50, 488, 50), arrow('cv2', 447, 180, 488, 180, cls='lna'),
     box(490, 25, 145, 50, ['A-si-ri lưu đày', '722 TCN'], 'bx', first_bold=True),
     box(490, 155, 145, 50, ['Ba-by-lôn lưu đày', '586 TCN'], 'bx', first_bold=True),
     T(337, 228, 'phía nam tồn tại lâu hơn ~140 năm', 'tm', 'middle', 12)]
F['cacvua'] = fig('cacvua', 640, 235, 'Các Vua: vương quốc chia đôi, phía bắc bị A-si-ri lưu đày, phía nam bị Ba-by-lôn lưu đày', ''.join(b),
                  'Các vua được đánh giá theo việc tôn kính Đức Chúa Trời. Phía nam có những vua tốt trị vì lâu nên tồn tại lâu hơn.')

# 23. Đa-ni-ên: hai nửa ------------------------------------------------------------
b = [box(10, 15, 290, 70, ['Chương 1–6 · viết VỀ ông', 'phép lạ: trung tín giữa Ba-by-lôn'], 'bx', first_bold=True),
     arrow('dn', 302, 50, 338, 50),
     box(340, 15, 290, 70, ['Chương 7–12 · do ông viết', 'khải tượng về tương lai xa'], 'bxa', 'ta', first_bold=True),
     T(320, 112, '75 năm đời Đa-ni-ên, nói về 2.400 năm lịch sử', 'tm', 'middle', 12)]
F['danien'] = fig('danien', 640, 125, 'Đa-ni-ên chia hai nửa: chuyện về ông với các phép lạ, và các khải tượng do ông viết', ''.join(b),
                  'Các khải tượng ở nửa sau là những khải tượng riêng, không nối tiếp nhau và có phần chồng lên nhau.')

# 24. Ma-thi-ơ: năm bài giảng --------------------------------------------------------
b = [f'<line x1="10" y1="80" x2="630" y2="80" class="ln"/>', T(10, 70, 'Giáng sinh', 'tm', 'start', 12),
     T(630, 70, 'Thập tự,', 'tm', 'end', 12), T(630, 100, 'phục sinh', 'tm', 'end', 12)]
for i, (a, c) in enumerate([('Trên núi', 'lối sống'), ('Sứ mạng', 'ra đi'), ('Ngụ ngôn', 'hạt giống'), ('Cộng đồng', 'kỷ luật'), ('Tương lai', 'tái lâm')]):
    x = 90 + i * 94
    b.append(f'<rect x="{x}" y="46" width="84" height="68" rx="6" class="bxa"/>' + T(x + 42, 66, str(i + 1), 'ta', 'middle', 12, 600)
             + T(x + 42, 86, a, 'ta', 'middle', 13, 600) + T(x + 42, 104, c, 'tm', 'middle', 12))
b.append(T(320, 138, 'xen giữa các bài giảng là việc làm của Chúa minh họa lời Ngài', 'tm', 'middle', 12))
F['mathio'] = fig('mathio', 640, 150, 'Ma-thi-ơ có năm bài giảng xen giữa các việc làm, từ giáng sinh đến thập tự giá', ''.join(b),
                  'Năm bài giảng của Ma-thi-ơ đều nói về cách làm công dân của Nước Trời.')

# 25. Khải Huyền: thư cho bảy hội thánh ----------------------------------------------
parts = ['Địa chỉ', 'Thuộc tính', 'Khen', 'Trách', 'Khuyên', 'Kêu gọi', 'Bảo đảm']
b = []
for i, s in enumerate(parts):
    x = 10 + i * 90
    hi = s in ('Khen', 'Trách')
    b.append(T(x + 41, 20, str(i + 1), 'tm', 'middle', 11) + box(x, 28, 82, 44, [s], 'bxa' if hi else 'bx', 'ta' if hi else 'tx', size=13))
b.append(f'<line x1="231" y1="74" x2="231" y2="90" class="ln" stroke-dasharray="2 3"/>' + T(225, 104, 'hai hội thánh lớn nhất', 'tm', 'end', 12) + T(225, 120, 'không được khen', 'tm', 'end', 12))
b.append(f'<line x1="321" y1="74" x2="321" y2="90" class="ln" stroke-dasharray="2 3"/>' + T(327, 104, 'hội thánh bị bắt bớ', 'tm', 'start', 12) + T(327, 120, 'không bị trách', 'tm', 'start', 12))
F['baylathu'] = fig('baylathu', 640, 132, 'Mỗi thư gửi bảy hội thánh trong Khải Huyền gồm bảy phần', ''.join(b),
                    'Khung bảy phần của mỗi thư gửi bảy hội thánh (Khải Huyền 2–3), theo Pawson.')
