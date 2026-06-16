"""pc ref-equation: @e1 на блочную формулу печатает '(1)' в тексте."""
import re
import helpers as h

c = h.Checks("pc_ref_equation_parens")
pdf = h.compile("pc_ref_equation_parens.typ")
t = " ".join(h.text(pdf).split())

m = re.search(r"ЭКВДО\s+(.+?)\s+ЭКВПОСЛЕ", t)
ref = m.group(1) if m else ""

c.check("ref_in_parens", ref == "(1)",
        f"ссылка на формулу = {ref!r}, ожидалось '(1)'")

c.check("text_contains_paren_one", "(1)" in t,
        f"в тексте нет '(1)':\n{t[:300]}")

c.done()
