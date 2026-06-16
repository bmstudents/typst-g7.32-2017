"""pg_fig_numbering_sequential: два рисунка → сквозная нумерация «Рисунок 1» и «Рисунок 2» по порядку."""
import helpers as h

c = h.Checks("pg_fig_numbering_sequential")
pdf = h.compile("pg_fig_numbering_sequential.typ")
t = h.text(pdf)

c.check("figure_1", "Рисунок 1 – Первая" in t, f"нет «Рисунок 1 – Первая» в:\n{t}")
c.check("figure_2", "Рисунок 2 – Вторая" in t, f"нет «Рисунок 2 – Вторая» в:\n{t}")

# Порядок: первая подпись «Рисунок» выше второй (Y растёт вниз).
y1 = h.y_of(pdf, "Рисунок", nth=1)
y2 = h.y_of(pdf, "Рисунок", nth=2)
c.check("order", y1 is not None and y2 is not None and y1 < y2,
        f"порядок подписей нарушен: y1={y1} y2={y2}")

c.done()
