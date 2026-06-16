"""pk: 2 приложения + #колво-приложений выводит "2"."""
import re
import helpers as h

c = h.Checks("pk_cnt_appendices")
pdf = h.compile("pk_cnt_appendices.typ")
t = " ".join(h.text(pdf).split())

m = re.search(r"маркерприложений\s+(\d+)\s+маркерприложений", t)
val = int(m.group(1)) if m else None
c.check("counter_emitted", val is not None,
        f"маркер #колво-приложений не нашёлся в:\n{t[:200]}")
c.check("counter_eq_2", val == 2,
        f"#колво-приложений = {val}, ожидалось 2")
c.check("two_appendices_rendered",
        "ПРИЛОЖЕНИЕ А" in t and "ПРИЛОЖЕНИЕ Б" in t,
        f"в документе не два приложения:\n{t[:500]}")
c.done()
