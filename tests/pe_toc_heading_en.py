"""pe_toc_heading_en: англ алиас #toc_heading даёт тот же 'СОДЕРЖАНИЕ'."""
import helpers as h

c = h.Checks("pe_toc_heading_en")
pdf = h.compile("pe_toc_heading_en.typ")
norm = " ".join(h.text(pdf).split())

c.check("heading", "СОДЕРЖАНИЕ" in norm,
        f"нет 'СОДЕРЖАНИЕ' (англ алиас) в:\n{norm[:200]}")
c.done()
