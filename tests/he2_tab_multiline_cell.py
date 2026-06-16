"""he2 EDGE-таблицы #8: многострочная ячейка (текст с \\).

ИНВАРИАНТЫ:
  1) все три строки ячейки присутствуют: ВЕРХОДИН, СЕРЕДИНА, НИЗТРИ;
  2) они на трёх РАЗНЫХ возрастающих базовых линиях (явный \\ = три строки);
  3) соседняя короткая ячейка выровнена по ВЕРХУ строки — её базовая линия
     совпадает с первой строкой многострочной ячейки (ВЕРХОДИН), а не центр/низ;
  4) подпись «Таблица 1» строго выше тела (над таблицей).

Файл пакета при провале: gost732-2017/styles/table.typ (align ячеек) /
utils/table.typ.
"""
import helpers as h

c = h.Checks("he2_tab_multiline_cell")
pdf = h.compile("he2_tab_multiline_cell.typ")
t = h.text(pdf)
ws = h.words(pdf)
TOL = 2.0

for m in ["ВЕРХОДИН", "СЕРЕДИНА", "НИЗТРИ", "короткаяячейка"]:
    c.check(f"present_{m}", m in t, f"нет {m}:\n{t}")

y_top = h.y_of(pdf, "ВЕРХОДИН")
y_mid = h.y_of(pdf, "СЕРЕДИНА")
y_bot = h.y_of(pdf, "НИЗТРИ")
y_short = h.y_of(pdf, "короткаяячейка")

if None not in (y_top, y_mid, y_bot):
    c.check("three_increasing_lines", y_top < y_mid < y_bot,
            f"строки ячейки не по возрастанию: {y_top} {y_mid} {y_bot} — "
            f"явный \\\\ не дал 3 строки. Файл: gost732-2017/styles/table.typ")

if y_top is not None and y_short is not None:
    c.check("neighbor_top_aligned", abs(y_short - y_top) <= TOL,
            f"короткая ячейка (y={y_short}) не по верху многострочной "
            f"(верх y={y_top}) — выравнивание ячеек не top. "
            f"Файл: gost732-2017/styles/table.typ")

y_cap = h.y_of(pdf, "Таблица")
if y_cap is not None and y_top is not None:
    c.check("caption_above_body", y_cap < y_top,
            f"подпись (y={y_cap}) не выше тела (y={y_top}). "
            f"Файл: gost732-2017/styles/figure.typ")
c.done()
