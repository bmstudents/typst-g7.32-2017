"""pe_intro_en: англ алиас #introduction даёт тот же заголовок 'ВВЕДЕНИЕ'."""
import helpers as h

c = h.Checks("pe_intro_en")
pdf = h.compile("pe_intro_en.typ")
norm = " ".join(h.text(pdf).split())

c.check("heading", "ВВЕДЕНИЕ" in norm,
        f"нет 'ВВЕДЕНИЕ' (англ алиас) в:\n{norm[:200]}")
c.done()
