"""pj 7: приложение на 2 страницы контента -> 'Листов 2'."""
import helpers as h

c = h.Checks("pj_app_sheets")
pdf = h.compile("pj_app_sheets.typ")
t = " ".join(h.text(pdf).split())

c.check("title_present", "ПРИЛОЖЕНИЕ Б" in t,
        f"нет 'ПРИЛОЖЕНИЕ Б' в:\n{t[:200]}")
c.check("sheets_present", "Листов" in t,
        f"нет 'Листов' в:\n{t[:200]}")
c.check("sheets_count", "Листов 2" in t,
        f"ожидалось 'Листов 2' в:\n{t[:200]}")
c.done()
