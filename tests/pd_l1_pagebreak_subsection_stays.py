"""pd l1-pagebreak: разрыв только у уровня 1 — подраздел остаётся на стр.1,
второй раздел уходит на стр.2."""
import helpers as h

c = h.Checks("pd_l1_pagebreak_subsection_stays")
pdf = h.compile("pd_l1_pagebreak_subsection_stays.typ")
ws = h.words(pdf)

def page_of(word):
    hits = [w for w in ws if w[5] == word]
    return hits[0][0] if hits else None

# Подраздел (уровень 2) НЕ ломает страницу — остаётся с разделом 1.
c.check("subsection_same_page_as_section1",
        page_of("Подраздел") == 1,
        f"подраздел на стр.{page_of('Подраздел')}, ждём 1 (l2 без разрыва)")

# Раздел два (уровень 1) — на новой странице.
c.check("section2_new_page",
        page_of("два") == 2,
        f"раздел два на стр.{page_of('два')}, ждём 2")

c.check("total_two_pages",
        h.page_count(pdf) == 2,
        f"страниц {h.page_count(pdf)}, ждём 2")

c.done()
