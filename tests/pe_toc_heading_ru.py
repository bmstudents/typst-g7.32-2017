"""pe_toc_heading_ru: русский алиас #содержание_заголовок даёт 'СОДЕРЖАНИЕ'."""
import helpers as h

c = h.Checks("pe_toc_heading_ru")
pdf = h.compile("pe_toc_heading_ru.typ")
norm = " ".join(h.text(pdf).split())

# В исходнике заголовок уже капсом; и белый список держит его в верхнем регистре.
c.check("heading", "СОДЕРЖАНИЕ" in norm,
        f"нет 'СОДЕРЖАНИЕ' в:\n{norm[:200]}")
c.done()
