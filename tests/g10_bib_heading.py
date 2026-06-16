"""g10: заголовок списка источников и запись источника видны."""
import helpers as h

c = h.Checks("g10_bib_heading")
pdf = h.compile("g10_bib_heading.typ")
t = " ".join(h.text(pdf).split())

c.check("heading", "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ" in t,
        f"нет заголовка списка в:\n{t[:400]}")
c.check("entry_author", "Кузнецов" in t,
        "нет автора источника (запись не отрендерилась)")
c.check("cite_in_text", "[1]" in t,
        "ссылка @kuznetsov2021 не дала [1] в тексте")
c.done()
