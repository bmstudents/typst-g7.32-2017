"""g5 РИСУНКИ: подпись «Рисунок 1 — Подпись», разделитель, позиция под телом."""
import helpers as h

c = h.Checks("g5_figure_caption")
pdf = h.compile("g5_figure_caption.typ")
t = h.text(pdf)

c.check("supplement_number", "Рисунок 1" in t, f"нет 'Рисунок 1' в:\n{t}")
c.check("separator", "Рисунок 1 — Схема системы" in t,
        f"подпись с разделителем ' — ' не найдена в:\n{t}")

# Подпись рисунка стоит ПОД телом: «Рисунок» ниже верха прямоугольника.
y_cap = h.y_of(pdf, "Рисунок")
y_sect = h.y_of(pdf, "Раздел")
c.check("caption_below_body", y_cap is not None and y_sect is not None and y_cap > y_sect,
        f"yРисунок={y_cap} yРаздел={y_sect}")
c.done()
