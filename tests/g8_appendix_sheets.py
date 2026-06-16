"""g8: на титуле приложения печатается 'Листов N' (число страниц приложения)."""
import helpers as h

c = h.Checks("g8_appendix_sheets")
pdf = h.compile("g8_appendix_sheets.typ")
t = h.text(pdf)

c.check("appendix_title", "ПРИЛОЖЕНИЕ Б" in t, f"нет 'ПРИЛОЖЕНИЕ Б' в:\n{t[:200]}")
c.check("sheets_present", "Листов" in t, f"нет 'Листов' в:\n{t[:200]}")
# Приложение из двух страниц контента -> 'Листов 2'.
c.check("sheets_count", "Листов 2" in t, f"ожидалось 'Листов 2' в:\n{t[:200]}")
c.done()
