"""pa_alias-da-net (аспект 2): значение 'да' принимается флагом и документ
компилируется."""
import helpers as h

c = h.Checks("pa_alias_da_compiles")
pdf = h.compile("pa_alias_da_compiles.typ")
t = h.text(pdf)

c.check("compiles", h.page_count(pdf) >= 1, "не скомпилировалось / нет страниц")
c.check("body_rendered", "флагом" in t, f"нет тела в:\n{t[:200]!r}")
c.done()
