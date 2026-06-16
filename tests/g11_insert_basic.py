"""g11_insert_basic: вставить-лист компилится, создаёт отдельную страницу, page_count растёт."""
import helpers as h

c = h.Checks("g11_insert_basic")
pdf = h.compile("g11_insert_basic.typ")

# 3 физ. страницы: текст до листа / лист / текст после
c.check("compiles_3_pages", h.page_count(pdf) == 3, f"ожидали 3 страницы, получили {h.page_count(pdf)}")

# лист — отдельная страница 2, на ней содержимое "скан"
c.check("sheet_on_own_page", h.first_word(pdf, 2)[1] == "скан",
        f"на стр.2 не лист: {h.first_word(pdf, 2)}")

# в-нумерации по умолчанию true → сквозной счётчик растёт: footer стр.3 = '3'
c.check("numbered_by_default", h.footer_word(pdf, 3) == "3",
        f"footer стр.3 = {h.footer_word(pdf, 3)!r}, ожидали '3'")

c.done()
