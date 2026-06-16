"""pc bib-cite-bracket: две разные цитаты дают '[1]' и '[2]' в квадратных скобках."""
import re
import helpers as h

c = h.Checks("pc_bib_cite_two")
pdf = h.compile("pc_bib_cite_two.typ")
t = " ".join(h.text(pdf).split())

a = re.search(r"АДО\s+(.+?)\s+АК", t)
b = re.search(r"БДО\s+(.+?)\s+БК", t)
va = a.group(1) if a else ""
vb = b.group(1) if b else ""

c.check("cite1_bracket", va == "[1]", f"первая цитата {va!r}, ждём '[1]'")
c.check("cite2_bracket", vb == "[2]", f"вторая цитата {vb!r}, ждём '[2]'")

c.check("both_authors_listed",
        "Смирнов" in t and "Петрова" in t,
        f"в списке нет обоих авторов:\n{t[:500]}")

c.done()
