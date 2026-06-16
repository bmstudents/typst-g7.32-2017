"""g5 РИСУНКИ: сквозная нумерация — два рисунка дают «Рисунок 1» и «Рисунок 2»."""
import helpers as h

c = h.Checks("g5_figure_numbering")
pdf = h.compile("g5_figure_numbering.typ")
t = h.text(pdf)

c.check("figure_1", "Рисунок 1 – Первая схема" in t, f"нет 'Рисунок 1 – Первая схема' в:\n{t}")
c.check("figure_2", "Рисунок 2 – Вторая схема" in t, f"нет 'Рисунок 2 – Вторая схема' в:\n{t}")

# Порядок: подпись Рисунок 1 выше подписи Рисунок 2 по тексту.
y1 = h.y_of(pdf, "Рисунок", nth=1)
y2 = h.y_of(pdf, "Рисунок", nth=2)
c.check("order", y1 is not None and y2 is not None and y1 < y2,
        f"y1={y1} y2={y2}")
c.done()
