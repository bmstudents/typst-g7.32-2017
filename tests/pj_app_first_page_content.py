"""pj 4: контент-первой-страницы:[Особый текст] -> текст появляется."""
import helpers as h

c = h.Checks("pj_app_first_page_content")
pdf = h.compile("pj_app_first_page_content.typ")
t = " ".join(h.text(pdf).split())

c.check("special_present", "Особый текст первой страницы" in t,
        f"нет контента первой страницы в:\n{t[:400]}")
c.check("title_present", "ПРИЛОЖЕНИЕ А" in t,
        f"нет 'ПРИЛОЖЕНИЕ А' в:\n{t[:400]}")
# Особый текст на той же (первой) странице приложения, ниже названия 'Листов'.
y_sheets = h.y_of(pdf, "Листов", page=1)
y_special = h.y_of(pdf, "Особый", page=1)
c.check("special_below_title",
        y_sheets is not None and y_special is not None and y_special > y_sheets,
        f"контент первой страницы не под шапкой: листов_y={y_sheets} особый_y={y_special}")
c.done()
