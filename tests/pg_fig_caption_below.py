"""pg_fig_caption_below: подпись рисунка стоит НИЖЕ тела — y подписи > y текста-якоря над рисунком.

Тело рисунка — rect() без текстового слоя, поэтому нижнюю границу проверяем
относительно текста-якоря над рисунком: подпись должна быть ещё ниже, причём
с зазором, превышающим высоту прямоугольника (4см ≈ 113pt).
"""
import helpers as h

c = h.Checks("pg_fig_caption_below")
pdf = h.compile("pg_fig_caption_below.typ")

y_cap = h.y_of(pdf, "Рисунок")          # подпись
y_anchor = h.y_of(pdf, "Текст-якорь")    # текст над рисунком (одно слово до дефиса? проверим)

# pdftotext делит на слова по пробелам; «Текст-якорь» — одно слово.
if y_anchor is None:
    y_anchor = h.y_of(pdf, "над")        # запасной якорь из той же строки

c.check("caption_exists", y_cap is not None, "подпись «Рисунок» не найдена")
c.check("anchor_exists", y_anchor is not None, "текст-якорь над рисунком не найден")

if y_cap is not None and y_anchor is not None:
    # Подпись ниже якоря.
    c.check("caption_below_anchor", y_cap > y_anchor,
            f"yподпись={y_cap:.1f} не ниже yякорь={y_anchor:.1f}")
    # Между якорем и подписью помещается прямоугольник (зазор > 90pt).
    c.check("body_between", (y_cap - y_anchor) > 90,
            f"зазор {y_cap - y_anchor:.1f}pt мал — тело рисунка не между якорем и подписью")

c.done()
