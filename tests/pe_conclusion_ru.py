"""pe_conclusion_ru: русский алиас #заключение даёт заголовок 'ЗАКЛЮЧЕНИЕ'."""
import helpers as h

c = h.Checks("pe_conclusion_ru")
pdf = h.compile("pe_conclusion_ru.typ")
norm = " ".join(h.text(pdf).split())

c.check("heading", "ЗАКЛЮЧЕНИЕ" in norm,
        f"нет 'ЗАКЛЮЧЕНИЕ' в:\n{norm[:200]}")
c.done()
