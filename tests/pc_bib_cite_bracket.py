"""pc bib-cite-bracket: цитата @key печатает '[1]' (стиль gost-r-705-2008-numeric)."""
import re
import helpers as h

c = h.Checks("pc_bib_cite_bracket")
pdf = h.compile("pc_bib_cite_bracket.typ")
t = " ".join(h.text(pdf).split())

m = re.search(r"ЦИТДО\s+(.+?)\s+ЦИТПОСЛЕ", t)
cite = m.group(1) if m else ""

c.check("cite_is_bracket_one", cite == "[1]",
        f"цитата = {cite!r}, ожидалось '[1]'")

c.check("bracket_in_text", "[1]" in t,
        f"в тексте нет '[1]':\n{t[:300]}")

# Источник попал в список (фамилия автора присутствует).
c.check("source_listed", "Смирнов" in t,
        f"автора 'Смирнов' нет в выводе:\n{t[:400]}")

c.done()
