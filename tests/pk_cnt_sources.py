"""pk: библиография с 2 цитированными источниками + #колво-источников выводит "2"."""
import re
import helpers as h

c = h.Checks("pk_cnt_sources")
pdf = h.compile("pk_cnt_sources.typ")
t = " ".join(h.text(pdf).split())

m = re.search(r"маркеристочников\s+(\d+)\s+маркеристочников", t)
val = int(m.group(1)) if m else None
c.check("counter_emitted", val is not None,
        f"маркер #колво-источников не нашёлся в:\n{t[:200]}")
c.check("counter_eq_2", val == 2,
        f"#колво-источников = {val}, ожидалось 2")
c.check("both_cited_rendered",
        "Петров" in t and "Иванова" in t,
        f"не оба источника в списке:\n{t[:400]}")
c.done()
