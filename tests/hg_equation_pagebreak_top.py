"""Блочная формула, перетёкшая на новую страницу, начинается от верхнего
поля (yMin ≈ 56.25pt), а НЕ на 2.5em ниже.

styles/eq.typ оборачивает блочную формулу в block(above: 2.5em). Если этот
верхний отступ не схлопывается на стыке страниц (как было у таблиц/листингов
до фикса F1/B1), формула на новой странице съезжает вниз на ≈35pt. Тот же
класс бага, что чинили для figure, но в eq.typ его не трогали."""
import helpers as h

TOP = 56.25  # верхнее поле (20мм)

c = h.Checks("hg_equation_pagebreak_top")
pdf = h.compile("hg_equation_pagebreak_top.typ")

c.check("two_pages", h.page_count(pdf) == 2, f"страниц {h.page_count(pdf)}, ожидал 2")

# верхнее слово страницы 2 — это формула (E … или её номер)
fw = h.first_word(pdf, 2)
c.check("page2_has_content", fw is not None, "стр.2 пустая")
if fw:
    y = fw[0]
    c.check("equation_at_top_margin", abs(y - TOP) <= 6,
            f"формула на стр.2 начинается с yMin={y:.1f}, ожидалось ≈{TOP} "
            f"(верхнее поле). Лишний above-отступ {y - TOP:.1f}pt не схлопнулся "
            f"на стыке страниц — block(above: 2.5em) в styles/eq.typ.")
c.done()
