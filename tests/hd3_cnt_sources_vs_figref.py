"""hd3: #колво-источников не должен путать ссылку на рисунок с источником.

В тексте есть @myfig (ссылка на рисунок) + @aaa, @bbb (две цитаты).
В списке источников 2 записи, обе процитированы. Ссылка на рисунок
@myfig имеет element != none (это figure) и должна быть исключена.
Ожидаем #колво-источников == 2.
"""
import re
import helpers as h

c = h.Checks("hd3_cnt_sources_vs_figref")
pdf = h.compile("hd3_cnt_sources_vs_figref.typ")
t = " ".join(h.text(pdf).split())

m = re.search(r"маркеристочников\s+(\d+)\s+маркеристочников", t)
val = int(m.group(1)) if m else None
c.check("counter_emitted", val is not None,
        f"маркер не нашёлся:\n{t[:300]}")

# в списке источников 2 записи
printed = ("Алексеев" in t) + ("Борисов" in t)
c.check("two_entries_printed", printed == 2,
        f"в списке источников {printed} записей, ожидалось 2")

# рисунок отрендерился и ссылка на него есть
c.check("figref_present", "Рисунок" in t,
        f"рисунок не отрендерился:\n{t[:300]}")

# главный инвариант: ровно 2, ссылка на рисунок не посчитана как источник
c.check("counter_eq_2_no_figref", val == 2,
        f"#колво-источников = {val}, ожидалось 2 (ссылка на рисунок @myfig "
        f"не должна считаться источником)")
c.done()
