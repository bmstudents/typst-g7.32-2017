"""hd4 @ref НА ФОРМУЛУ: ссылка @ea на блочную формулу печатает её номер в
скобках '(N)'. Проверяем, что @ea→(1), @eb→(2), @ec→(3) — ссылка совпадает
с фактическим номером формулы, а не сбита на 1.
"""
import re
import helpers as h

c = h.Checks("hd4_eq_ref_parens")
pdf = h.compile("hd4_eq_ref_parens.typ")
t = " ".join(h.text(pdf).split())

def ref_between(a, b):
    m = re.search(re.escape(a) + r"\s+(.+?)\s+" + re.escape(b), t)
    return m.group(1) if m else None

ra = ref_between("RA1", "EA1")
rb = ref_between("RB", "EB")
rc = ref_between("RC", "EC")

c.check("ref_a_is_1",
        ra == "(1)",
        f"@ea вернул {ra!r}, ожидалось '(1)'.\nТекст:\n{t}")

c.check("ref_b_is_2",
        rb == "(2)",
        f"@eb вернул {rb!r}, ожидалось '(2)'.\nТекст:\n{t}")

c.check("ref_c_is_3",
        rc == "(3)",
        f"@ec вернул {rc!r}, ожидалось '(3)'.\nТекст:\n{t}")

c.done()
