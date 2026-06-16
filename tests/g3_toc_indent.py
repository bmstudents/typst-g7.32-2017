"""g3_toc_indent: отступ записи в оглавлении растёт с уровнем (x уровня 2 > x уровня 1)."""
import helpers as h

c = h.Checks("g3_toc_indent")
pdf = h.compile("g3_toc_indent.typ")
toc = [w for w in h.words(pdf) if w[0] == 1]


def x_of_prefix(label):
    hits = [w for w in toc if w[5] == label]
    return hits[0][1] if hits else None


x1 = x_of_prefix("1")
x2 = x_of_prefix("1.1")
x3 = x_of_prefix("1.1.1")

c.check("levels_present", None not in (x1, x2, x3),
        f"не все номера записей найдены: x1={x1} x2={x2} x3={x3}")
c.check("indent_l2_gt_l1", x2 > x1, f"уровень 2 не правее уровня 1: x1={x1:.2f} x2={x2:.2f}")
c.check("indent_l3_gt_l2", x3 > x2, f"уровень 3 не правее уровня 2: x2={x2:.2f} x3={x3:.2f}")

c.done()
