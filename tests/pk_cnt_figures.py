"""pk: 2 рисунка + #колво-рисунков выводит "2"."""
import re
import helpers as h

c = h.Checks("pk_cnt_figures")
pdf = h.compile("pk_cnt_figures.typ")
t = " ".join(h.text(pdf).split())

m = re.search(r"маркеррисунков\s+(\d+)\s+маркеррисунков", t)
val = int(m.group(1)) if m else None
c.check("counter_emitted", val is not None,
        f"маркер #колво-рисунков не нашёлся в:\n{t[:200]}")
c.check("counter_eq_2", val == 2,
        f"#колво-рисунков = {val}, ожидалось 2")
c.check("two_figures_rendered",
        "Рисунок 1" in t and "Рисунок 2" in t,
        "в документе не два рисунка")
c.done()
