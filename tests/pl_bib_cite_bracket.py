"""pl point 3: цитата @key в тексте печатается как '[1]'."""
import re
import helpers as h

c = h.Checks("pl_bib_cite_bracket")
pdf = h.compile("pl_bib_cite_bracket.typ")
t = " ".join(h.text(pdf).split())

# между маркерами должна стоять именно '[1]'
m = re.search(r"цитатадо\s+(.+?)\s+цитатапосле", t)
cite = m.group(1) if m else ""
c.check("cite_is_bracket_1", cite == "[1]",
        f"цитата = '{cite}', ожидалось '[1]'")
c.check("bracket_in_doc", "[1]" in t, f"нет '[1]' в документе:\n{t[:300]}")
c.done()
