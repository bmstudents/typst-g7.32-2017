"""pb table-inset-10: инсет работает и справа. Содержимое right-выровненной
ячейки заканчивается на 10pt раньше правой границы таблицы (552.76).
Контроль: ячейка с inset:0pt стоит ровно у левой границы (85.04)."""
import helpers as h

c = h.Checks("pb_table_inset_right")
pdf = h.compile("pb_table_inset_right.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 700]

right_cell = [w for w in ws if w[5] == "Ж"]
zero_cell = [w for w in ws if w[5] == "Б"]
c.check("cells_visible",
        len(right_cell) == 1 and len(zero_cell) == 1,
        f"ячейки не найдены: {[w[5] for w in ws]}")

if right_cell:
    table_right = 552.76
    inset_r = table_right - right_cell[0][3]
    c.check("right_inset_10pt",
            abs(inset_r - 10) < 2,
            f"инсет справа {inset_r:.2f}pt, ждём ~10 (текст x1={right_cell[0][3]:.2f})")

if zero_cell:
    # inset:0pt снимает отступ — текст ровно у границы, доказывая что
    # обычные 10pt — это именно инсет, а не поля абзаца.
    c.check("zero_inset_flush",
            abs(zero_cell[0][1] - 85.04) < 1,
            f"inset:0pt ячейка не у границы: x0={zero_cell[0][1]:.2f}, ждём 85.04")

c.done()
