"""pc ref-table: @t1 на таблицу печатает её номер (число '1')."""
import re
import helpers as h

c = h.Checks("pc_ref_table_number")
pdf = h.compile("pc_ref_table_number.typ")
t = " ".join(h.text(pdf).split())

m = re.search(r"ТАБДО\s+(.+?)\s+ТАБПОСЛЕ", t)
ref = m.group(1) if m else ""

c.check("ref_is_number", ref.isdigit(),
        f"ссылка на таблицу = {ref!r}, ожидалось число")

c.check("ref_is_one", ref == "1",
        f"номер таблицы в ссылке = {ref!r}, ожидалось '1'")

# Подпись 'Таблица' присутствует в документе, но не внутри ссылки.
c.check("supplement_not_in_ref",
        "Таблица" in t and "Таблица" not in ref,
        f"'Таблица' просочилось в ссылку: {ref!r}")

c.done()
