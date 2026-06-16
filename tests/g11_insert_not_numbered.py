"""g11_insert_not_numbered: лист с в-нумерации:false физически есть (3 стр.),
но не увеличивает сквозной счётчик — footer последней страницы = '2'."""
import helpers as h

c = h.Checks("g11_insert_not_numbered")
pdf = h.compile("g11_insert_not_numbered.typ")

# физически 3 страницы: Текст1 / лист / Текст2
c.check("physical_3_pages", h.page_count(pdf) == 3, f"ожидали 3 физ. страницы, получили {h.page_count(pdf)}")

# лист на стр.2
c.check("sheet_page_2", h.first_word(pdf, 2)[1] == "скан", f"на стр.2 не лист: {h.first_word(pdf, 2)}")

# лист вне сквозной нумерации: стр.3 ('Текст2') получает номер '2', как будто листа не было
c.check("sheet_excluded_from_numbering", h.footer_word(pdf, 3) == "2",
        f"footer стр.3 = {h.footer_word(pdf, 3)!r}, ожидали '2' (лист вне нумерации)")

c.done()
