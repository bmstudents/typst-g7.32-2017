"""pe_intro_ru: русский алиас #введение даёт заголовок 'ВВЕДЕНИЕ'."""
import helpers as h

c = h.Checks("pe_intro_ru")
pdf = h.compile("pe_intro_ru.typ")
norm = " ".join(h.text(pdf).split())

c.check("heading", "ВВЕДЕНИЕ" in norm,
        f"нет 'ВВЕДЕНИЕ' в:\n{norm[:200]}")
c.done()
