"""pl point 1: #bibliography печатает заголовок
'СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ' (ГОСТ 7.32-2017)."""
import helpers as h

c = h.Checks("pl_bib_heading")
pdf = h.compile("pl_bib_heading.typ")
t = " ".join(h.text(pdf).split())

c.check("heading_present", "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ" in t,
        f"нет заголовка списка источников в:\n{t[:400]}")
# заголовок именно прописными — нет смешанного регистра 'Список ...'
c.check("heading_upper", "Список использованных" not in t,
        "заголовок не прописными буквами (есть смешанный регистр)")
c.done()
