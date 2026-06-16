"""pb heading-numbering: два раздела получают сквозные номера '1' и '2',
и каждый раздел 1-го уровня начинается с новой страницы (pagebreak)."""
import helpers as h

c = h.Checks("pb_heading_two_sections")
pdf = h.compile("pb_heading_two_sections.typ")
t = h.text(pdf)

c.check("first_is_1",
        "1 Альфа раздел" in t,
        f"нет '1 Альфа раздел' в:\n{t[:200]}")

c.check("second_is_2",
        "2 Бета раздел" in t,
        f"нет '2 Бета раздел' в:\n{t[:200]}")

# Разделы 1-го уровня: pagebreak:true → второй раздел на отдельной странице.
pa = h.y_of(pdf, "Альфа")
pb_ = h.y_of(pdf, "Бета")
page_a = next((w[0] for w in h.words(pdf) if w[5] == "Альфа"), None)
page_b = next((w[0] for w in h.words(pdf) if w[5] == "Бета"), None)
c.check("sections_on_separate_pages",
        page_a is not None and page_b is not None and page_b > page_a,
        f"разделы не на разных страницах: Альфа стр{page_a}, Бета стр{page_b}")

c.done()
