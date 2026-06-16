"""pd num-multi-section: три раздела -> номера 1, 2, 3 идут по порядку."""
import helpers as h

c = h.Checks("pd_num_multi_section_three")
pdf = h.compile("pd_num_multi_section_three.typ")
t = h.text(pdf)

c.check("section_1",
        "1 Аналитика" in t,
        f"нет '1 Аналитика':\n{t[:500]!r}")

c.check("section_2",
        "2 Проектирование" in t,
        f"нет '2 Проектирование':\n{t[:500]!r}")

c.check("section_3",
        "3 Реализация" in t,
        f"нет '3 Реализация':\n{t[:500]!r}")

c.done()
