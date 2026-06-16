"""pe_bibheading_en: англ алиас #bibliography_heading → тот же 'СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ'."""
import helpers as h

c = h.Checks("pe_bibheading_en")
pdf = h.compile("pe_bibheading_en.typ")
norm = " ".join(h.text(pdf).split())

c.check("heading", "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ" in norm,
        f"нет заголовка (англ алиас) в:\n{norm[:200]}")
c.done()
