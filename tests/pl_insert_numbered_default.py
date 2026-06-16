"""pl point 9: по умолчанию (в-нумерации: да) лист считается в сквозной
нумерации — счётчик растёт нормально: footer стр.3 = '3'."""
import helpers as h

c = h.Checks("pl_insert_numbered_default")
pdf = h.compile("pl_insert_numbered_default.typ")

c.check("physical_3_pages", h.page_count(pdf) == 3,
        f"ожидали 3 физ. страницы, получили {h.page_count(pdf)}")

# лист посчитан: footer стр.2 = '2', footer стр.3 = '3'
c.check("sheet_counted", h.footer_word(pdf, 2) == "2",
        f"footer стр.2 (листа) = {h.footer_word(pdf, 2)!r}, ожидали '2'")
c.check("number_grows", h.footer_word(pdf, 3) == "3",
        f"footer стр.3 = {h.footer_word(pdf, 3)!r}, ожидали '3' (лист в нумерации)")
c.done()
