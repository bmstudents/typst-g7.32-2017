"""hd6: многократная цитата одного источника = одна запись, один номер.

src05 (Смирнов, «Машинное обучение») цитируется трижды, между ними —
src09 (Соколов, «Графика»).

Инварианты:
  * все три цитаты src05 печатают ОДИН и тот же номер [1];
  * src09 печатает [2];
  * в списке «Смирнов … Машинное обучение» встречается РОВНО один раз
    (повтор цитаты не плодит дублей записи);
  * номер записи Смирнова в списке == номеру его цитаты ([1] ↔ «1.»).
"""
import re
import helpers as h

c = h.Checks("hd6_bib_double_cite")
pdf = h.compile("hd6_bib_double_cite.typ")
t = " ".join(h.text(pdf).split())

# Текстовая часть до заголовка списка — там цитаты.
body = t.split("СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ", 1)[0]
tokens = re.findall(r"\[(\d+)\]", body)
c.check("three_plus_one_citations", len(tokens) == 4,
        f"ожидалось 4 цитаты в тексте, нашли {len(tokens)}: {tokens}")

# Первая, третья и четвёртая — это src05 (должны быть равны), вторая — src09.
c.check("src05_same_number_thrice",
        tokens[0] == tokens[2] == tokens[3] and tokens[0] == "1",
        f"три цитаты src05 дали разные номера: {tokens} (ожидалось [1] у 1,3,4)")
c.check("src09_is_two", tokens[1] == "2",
        f"src09 дал [{tokens[1]}], ожидалось [2]")

# В списке Смирнов ровно один раз.
list_part = t.split("СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ", 1)[-1]
c.check("smirnov_single_entry",
        list_part.count("Машинное обучение") == 1,
        f"запись Смирнова встречается {list_part.count('Машинное обучение')} раз, ожидалась 1")

# Номер записи Смирнова == 1.
m = re.search(r"(\d+)\.\s*Смирнов", t)
c.check("smirnov_list_number_one", m is not None and m.group(1) == "1",
        f"Смирнов в списке под номером {m.group(1) if m else None}, ожидался 1")
c.done()
