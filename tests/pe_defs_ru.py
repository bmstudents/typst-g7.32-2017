"""pe_defs_ru: русский алиас #определения_обозначения_сокращения[..] даёт заголовок + переданный текст."""
import helpers as h

c = h.Checks("pe_defs_ru")
pdf = h.compile("pe_defs_ru.typ")
norm = " ".join(h.text(pdf).split())

c.check("heading", "ОПРЕДЕЛЕНИЯ, ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ" in norm,
        f"нет заголовка раздела в:\n{norm[:200]}")
c.check("body_text", "Тело раздела определений мармеладной системы" in norm,
        "нет переданного текста тела раздела")
c.done()
