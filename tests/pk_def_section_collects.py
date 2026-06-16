"""pk: два #определение(...) — оба текста определений попадают в раздел."""
import helpers as h

c = h.Checks("pk_def_section_collects")
pdf = h.compile("pk_def_section_collects.typ")
norm = " ".join(h.text(pdf).split())

c.check("first_definition",
        "промежуточный буфер быстрого доступа к данным" in norm,
        f"нет первого определения (кэш) в:\n{norm[:500]}")
c.check("second_definition",
        "программа управления устройством" in norm,
        f"нет второго определения (драйвер) в:\n{norm[:500]}")
c.check("heading_present",
        "ОПРЕДЕЛЕНИЯ, ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ" in norm,
        "нет заголовка раздела")
c.done()
