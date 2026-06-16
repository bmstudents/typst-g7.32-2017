"""pf_toc_indent_prefix: x номера записи растёт с уровнем — '1' < '1.1' < '1.1.1'."""
import helpers as h

c = h.Checks("pf_toc_indent_prefix")
pdf = h.compile("pf_toc_indent_prefix.typ")
toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
toc = [w for w in h.words(pdf) if w[0] == toc_page]


def x_of(label):
    hits = [w for w in toc if w[5] == label]
    return hits[0][1] if hits else None


x1 = x_of("1")
x2 = x_of("1.1")
x3 = x_of("1.1.1")

c.check("all_levels_present", None not in (x1, x2, x3),
        f"не все номера найдены: 1={x1} 1.1={x2} 1.1.1={x3}")
c.check("l2_right_of_l1", x2 is not None and x1 is not None and x2 > x1,
        f"уровень 2 не правее 1: x1={x1} x2={x2}")
c.check("l3_right_of_l2", x3 is not None and x2 is not None and x3 > x2,
        f"уровень 3 не правее 2: x2={x2} x3={x3}")

c.done()
