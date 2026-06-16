"""pb page-numbering-config: нумерация арабская (1,2,3 — не I/II или a/b),
номера растут по страницам, формат '1'."""
import helpers as h

c = h.Checks("pb_pagenum_arabic")
pdf = h.compile("pb_pagenum_arabic.typ")

c.check("three_pages", h.page_count(pdf) == 3, f"страниц {h.page_count(pdf)}")

foots = [h.footer_word(pdf, p) for p in (1, 2, 3)]
c.check("all_arabic_digits",
        all(f is not None and f.isdigit() for f in foots),
        f"футеры не арабские цифры: {foots}")

c.check("sequence_1_2_3",
        foots == ["1", "2", "3"],
        f"номера не 1,2,3: {foots}")

# Никаких римских/буквенных форм в футере.
c.check("no_roman",
        all(f not in ("I", "II", "III", "a", "b", "c") for f in foots if f),
        f"похоже на не-арабскую нумерацию: {foots}")

c.done()
