"""pb margin-top-20: верхнее поле одинаково на КАЖДОЙ странице (первое слово
каждой страницы на yMin≈56.25)."""
import helpers as h

c = h.Checks("pb_margin_top_multipage")
pdf = h.compile("pb_margin_top_multipage.typ")

c.check("three_pages", h.page_count(pdf) == 3, f"страниц {h.page_count(pdf)}, ждём 3")

tops = [h.first_word(pdf, p) for p in (1, 2, 3)]
ys = [t[0] for t in tops if t]
c.check("all_pages_top_56",
        len(ys) == 3 and all(abs(y - 56.25) < 2 for y in ys),
        f"верх первых слов по страницам: {[round(y,2) for y in ys]}, ждём ~56.25")

# Поля стабильны между страницами (разброс < 1pt).
c.check("top_consistent",
        len(ys) == 3 and (max(ys) - min(ys)) < 1,
        f"верхнее поле гуляет между страницами: {[round(y,2) for y in ys]}")

c.done()
