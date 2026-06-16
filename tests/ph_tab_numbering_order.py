"""4 tab-numbering (порядок по странице): 'Таблица' встречается ровно дважды,
и подпись №1 ('Первая') расположена выше подписи №2 ('Вторая')."""
import helpers as h

c = h.Checks("ph_tab_numbering_order")
pdf = h.compile("ph_tab_numbering_order.typ")
t = h.text(pdf)

c.check("two_supplements", t.count("Таблица") == 2,
        f"ожидалось два 'Таблица', нашлось {t.count('Таблица')}")

y1 = h.y_of(pdf, "Первая")
y2 = h.y_of(pdf, "Вторая")
c.check("first_above_second", y1 is not None and y2 is not None and y1 < y2,
        f"подпись 1 не выше подписи 2: yПервая={y1} yВторая={y2}")
c.done()
