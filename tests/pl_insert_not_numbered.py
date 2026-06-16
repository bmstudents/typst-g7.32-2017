"""pl point 8: лист с 'в-нумерации: нет' физически есть (3 страницы),
но вне сквозной нумерации — footer последней страницы = '2' (как будто
листа не было)."""
import helpers as h

c = h.Checks("pl_insert_not_numbered")
pdf = h.compile("pl_insert_not_numbered.typ")

# физически 3 страницы: Текст1 / лист / Текст2
c.check("physical_3_pages", h.page_count(pdf) == 3,
        f"ожидали 3 физ. страницы, получили {h.page_count(pdf)}")

# лист на стр.2
fw = h.first_word(pdf, 2)
c.check("sheet_on_page2", fw is not None and fw[1] == "скан",
        f"на стр.2 не лист: {fw}")

# лист вне сквозной нумерации: стр.3 ('Текст2') получает номер '2'
c.check("excluded_from_numbering", h.footer_word(pdf, 3) == "2",
        f"footer стр.3 = {h.footer_word(pdf, 3)!r}, ожидали '2' (лист вне нумерации)")
c.done()
