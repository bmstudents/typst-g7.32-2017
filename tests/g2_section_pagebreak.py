"""g2: раздел (ур.1) начинается с новой страницы — второй/третий раздел на page>1."""
import helpers as h

c = h.Checks("g2_section_pagebreak")
pdf = h.compile("g2_section_pagebreak.typ")
ws = h.words(pdf)


def page_of(word):
    hits = [w for w in ws if w[5] == word]
    return hits[0][0] if hits else None


# Три раздела -> три страницы (каждый ур.1 c новой страницы).
c.check("three_pages",
        h.page_count(pdf) == 3,
        f"страниц {h.page_count(pdf)}, ждём 3 (каждый раздел с новой страницы)")

# Номера разделов как первые слова страниц.
p_first = page_of("Первый")
p_second = page_of("Второй")
p_third = page_of("Третий")

c.check("first_on_page1",
        p_first == 1,
        f"'Первый' на странице {p_first}, ждём 1")

c.check("second_on_new_page",
        p_second is not None and p_second > 1,
        f"'Второй раздел' на странице {p_second}, ждём >1")

c.check("each_section_own_page",
        p_first == 1 and p_second == 2 and p_third == 3,
        f"страницы разделов: {p_first}/{p_second}/{p_third}, ждём 1/2/3")

c.done()
