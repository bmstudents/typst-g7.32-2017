"""pe_bibheading_ru: русский алиас #список_использованных_источников_заголовок → 'СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ'."""
import helpers as h

c = h.Checks("pe_bibheading_ru")
pdf = h.compile("pe_bibheading_ru.typ")
norm = " ".join(h.text(pdf).split())

c.check("heading", "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ" in norm,
        f"нет заголовка в:\n{norm[:200]}")
c.done()
