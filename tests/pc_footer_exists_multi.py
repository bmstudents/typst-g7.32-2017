"""pc footer-number-exists: на каждой из 4 страниц нижнее слово — числовой колонтитул."""
import helpers as h

c = h.Checks("pc_footer_exists_multi")
pdf = h.compile("pc_footer_exists_multi.typ")

n = h.page_count(pdf)
c.check("four_pages", n == 4, f"страниц {n}, ждём 4")

footers = [h.footer_word(pdf, p) for p in range(1, n + 1)]
c.check("footer_present_each_page",
        all(f is not None for f in footers),
        f"на какой-то странице нет нижнего слова: {footers!r}")

c.check("footer_numeric_each_page",
        all(f is not None and f.isdigit() for f in footers),
        f"футеры не все числовые: {footers!r}")

c.done()
