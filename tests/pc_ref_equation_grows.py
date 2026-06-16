"""pc ref-equation: две формулы → ссылки '(1)' и '(2)' в скобках, номера растут."""
import re
import helpers as h

c = h.Checks("pc_ref_equation_grows")
pdf = h.compile("pc_ref_equation_grows.typ")
t = " ".join(h.text(pdf).split())

r1 = re.search(r"ПЕРВ\s+(.+?)\s+ПЕРВК", t)
r2 = re.search(r"ВТОР\s+(.+?)\s+ВТОРК", t)
v1 = r1.group(1) if r1 else ""
v2 = r2.group(1) if r2 else ""

c.check("eq_ref1", v1 == "(1)", f"ссылка 1 = {v1!r}, ждём '(1)'")
c.check("eq_ref2", v2 == "(2)", f"ссылка 2 = {v2!r}, ждём '(2)'")

c.done()
