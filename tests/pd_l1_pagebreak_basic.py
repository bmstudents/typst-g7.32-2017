"""pd l1-pagebreak: второй раздел уровня 1 начинается с новой страницы (page>1)."""
import helpers as h

c = h.Checks("pd_l1_pagebreak_basic")
pdf = h.compile("pd_l1_pagebreak_basic.typ")

p2 = h.y_of(pdf, "Основная", nth=1)  # просто чтобы убедиться слово есть
ws = h.words(pdf)

def page_of(word):
    hits = [w for w in ws if w[5] == word]
    return hits[0][0] if hits else None

c.check("two_pages",
        h.page_count(pdf) == 2,
        f"страниц {h.page_count(pdf)}, ждём 2 (второй раздел с новой страницы)")

c.check("first_on_page1",
        page_of("Введение") == 1,
        f"первый раздел не на стр.1: {page_of('Введение')}")

c.check("second_on_page2",
        page_of("Основная") == 2,
        f"второй раздел на стр.{page_of('Основная')}, ждём 2")

c.done()
