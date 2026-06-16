"""pk: раздел определений выводит заголовок ОПРЕДЕЛЕНИЯ, ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ."""
import helpers as h

c = h.Checks("pk_def_section_heading")
pdf = h.compile("pk_def_section_heading.typ")
t = h.text(pdf)
norm = " ".join(t.split())

c.check("heading_present",
        "ОПРЕДЕЛЕНИЯ, ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ" in norm,
        f"нет заголовка раздела в:\n{norm[:400]}")
c.done()
