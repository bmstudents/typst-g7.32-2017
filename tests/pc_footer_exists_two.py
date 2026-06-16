"""pc footer-number-exists: минимальный многостраничный документ — у обеих страниц числовой футер."""
import helpers as h

c = h.Checks("pc_footer_exists_two")
pdf = h.compile("pc_footer_exists_two.typ")

c.check("two_pages", h.page_count(pdf) == 2, f"страниц {h.page_count(pdf)}, ждём 2")

f1 = h.footer_word(pdf, 1)
f2 = h.footer_word(pdf, 2)
c.check("footer_p1_numeric", f1 is not None and f1.isdigit(),
        f"футер стр.1 не число: {f1!r}")
c.check("footer_p2_numeric", f2 is not None and f2.isdigit(),
        f"футер стр.2 не число: {f2!r}")

c.done()
