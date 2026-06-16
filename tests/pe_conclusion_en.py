"""pe_conclusion_en: англ алиас #conslusion (имя с опечаткой в пакете) даёт тот же 'ЗАКЛЮЧЕНИЕ'."""
import helpers as h

c = h.Checks("pe_conclusion_en")
pdf = h.compile("pe_conclusion_en.typ")
norm = " ".join(h.text(pdf).split())

c.check("heading", "ЗАКЛЮЧЕНИЕ" in norm,
        f"нет 'ЗАКЛЮЧЕНИЕ' (англ алиас #conslusion) в:\n{norm[:200]}")
c.done()
