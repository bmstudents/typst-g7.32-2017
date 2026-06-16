"""Smoke: пакет компилируется и базовый текст на месте."""
import helpers as h

c = h.Checks("g0_smoke")
pdf = h.compile("g0_smoke.typ")
t = h.text(pdf)

c.check("compiles", h.page_count(pdf) >= 1, "нет страниц")
c.check("section_numbered", "1 Раздел" in t, f"нет '1 Раздел' в:\n{t[:200]}")
c.check("subsection_numbered", "1.1 Подраздел" in t, "нет '1.1 Подраздел'")
c.done()
