"""5 tab-breakable: длинная таблица (60 строк) разрывается на >1 страницу."""
import helpers as h

c = h.Checks("ph_tab_breakable_pages")
pdf = h.compile("ph_tab_breakable_pages.typ")

pc = h.page_count(pdf)
c.check("multipage", pc > 1, f"таблица не разорвалась: страниц {pc}")
c.done()
