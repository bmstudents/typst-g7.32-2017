"""pk: 2 таблицы + #колво-таблиц выводит "2"."""
import re
import helpers as h

c = h.Checks("pk_cnt_tables")
pdf = h.compile("pk_cnt_tables.typ")
t = " ".join(h.text(pdf).split())

m = re.search(r"маркертаблиц\s+(\d+)\s+маркертаблиц", t)
val = int(m.group(1)) if m else None
c.check("counter_emitted", val is not None,
        f"маркер #колво-таблиц не нашёлся в:\n{t[:200]}")
c.check("counter_eq_2", val == 2,
        f"#колво-таблиц = {val}, ожидалось 2")
c.check("two_tables_rendered",
        "Таблица 1" in t and "Таблица 2" in t,
        "в документе не две таблицы")
c.done()
