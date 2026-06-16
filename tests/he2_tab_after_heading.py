"""he2 EDGE-таблицы #5: таблица СРАЗУ после заголовка раздела (= Раздел \\n #таблица).

ИНВАРИАНТЫ:
  1) заголовок и подпись таблицы оба отрендерились;
  2) подпись «Таблица 1» строго НИЖЕ заголовка (y подписи > y заголовка) —
     не наезжает, порядок сохранён;
  3) есть положительный вертикальный зазор между низом заголовка и подписью
     (>= 6pt) — подпись не прилипла к заголовку;
  4) левый край подписи == левому полю (85pt) — left-выравнивание под подписью
     сохраняется даже сразу после заголовка (h(-1.25cm) не сбит).

Файл пакета при провале: gost732-2017/styles/figure.typ / styles/heading.typ.
"""
import helpers as h

c = h.Checks("he2_tab_after_heading")
pdf = h.compile("he2_tab_after_heading.typ")
ws = h.words(pdf)

LEFT = 30 / 25.4 * 72.0
TOL = 1.5

y_head = next((w[2] for w in ws if w[5] == "ЗАГОЛОВОКРАЗДЕЛА"), None)
yb_head = next((w[4] for w in ws if w[5] == "ЗАГОЛОВОКРАЗДЕЛА"), None)
y_cap = next((w[2] for w in ws if w[5] == "Таблица"), None)
x_cap = next((w[1] for w in ws if w[5] == "Таблица"), None)

c.check("heading_present", y_head is not None, "заголовок не отрендерился")
c.check("caption_present", y_cap is not None, "подпись 'Таблица' не отрендерилась")

if y_head is not None and y_cap is not None:
    c.check("caption_below_heading", y_cap > y_head,
            f"подпись (y={y_cap}) не ниже заголовка (y={y_head}) — наезд. "
            f"Файл: gost732-2017/styles/figure.typ")
    gap = y_cap - yb_head
    c.check("positive_gap", gap >= 6.0,
            f"зазор заголовок→подпись {gap:.1f}pt < 6pt — подпись прилипла к заголовку. "
            f"Файл: gost732-2017/styles/figure.typ")

c.check("caption_left_aligned", x_cap is not None and abs(x_cap - LEFT) <= TOL,
        f"левый край подписи x={x_cap} != левому полю {LEFT:.1f}pt сразу после заголовка. "
        f"Файл: gost732-2017/styles/figure.typ")
c.done()
