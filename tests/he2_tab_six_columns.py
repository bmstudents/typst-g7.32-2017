"""he2 EDGE-таблицы #4: МНОГО колонок (6×1fr) на всю ширину полосы.

Полоса набора A4: ширина 595.28pt, поля left=30мм right=15мм → тело от 85.04
до 552.76 (ширина 467.72pt). 6 равных 1fr-колонок → шаг 77.95pt.

ИНВАРИАНТЫ:
  1) все 12 маркеров присутствуют (к1..к6, я1..я6);
  2) РАВНОМЕРНОСТЬ: x-координаты колонок шапки идут с почти постоянным шагом
     (разброс соседних шагов <= 2pt) — fr-колонки равны;
  3) В ПОЛОСЕ: левый край первой колонки >= левого поля, правый край последней
     <= правого поля (с допуском);
  4) под-колонки выровнены: к-маркер и я-маркер одной колонки имеют один x0.

Файл пакета при провале: gost732-2017/styles/figure.typ (обёртка columns:(1fr)
+ h(-1.25cm)) / styles/table.typ.
"""
import helpers as h

c = h.Checks("he2_tab_six_columns")
pdf = h.compile("he2_tab_six_columns.typ")
t = h.text(pdf)
ws = h.words(pdf)

LEFT = 30 / 25.4 * 72.0          # 85.04
RIGHT = 595.28 - 15 / 25.4 * 72.0  # 552.76
TOL = 2.0

for i in range(1, 7):
    c.check(f"present_к{i}", f"к{i}" in t, f"нет маркера к{i}:\n{t}")

head = sorted([w for w in ws if w[0] == 1 and w[5] in {f"к{i}" for i in range(1, 7)}],
              key=lambda w: w[1])
c.check("six_head_cells", len(head) == 6, f"шапка: найдено {len(head)} маркеров (ожидали 6)")

if len(head) == 6:
    xs = [w[1] for w in head]
    steps = [round(xs[i + 1] - xs[i], 2) for i in range(5)]
    spread = max(steps) - min(steps)
    c.check("uniform_columns", spread <= TOL,
            f"шаги колонок неравномерны: steps={steps}, разброс={spread:.2f}pt (> {TOL}) — "
            f"fr-колонки не равны. Файл: gost732-2017/styles/figure.typ")

    left_x = min(w[1] for w in head)
    right_x = max(w[3] for w in ws if w[0] == 1 and w[5] in {f"я{i}" for i in range(1, 7)}
                  or (w[0] == 1 and w[5] in {f"к{i}" for i in range(1, 7)}))
    c.check("within_left_margin", left_x >= LEFT - TOL,
            f"левый край таблицы x={left_x:.1f} левее поля {LEFT:.1f}pt. "
            f"Файл: gost732-2017/styles/figure.typ")
    c.check("within_right_margin", right_x <= RIGHT + TOL,
            f"правый край таблицы x={right_x:.1f} правее поля {RIGHT:.1f}pt. "
            f"Файл: gost732-2017/styles/figure.typ")

# вертикальное выравнивание колонок: к-я одной колонки совпадают по x0
mis = []
for i in range(1, 7):
    xk = next((w[1] for w in ws if w[0] == 1 and w[5] == f"к{i}"), None)
    xy = next((w[1] for w in ws if w[0] == 1 and w[5] == f"я{i}"), None)
    if xk is None or xy is None or abs(xk - xy) > TOL:
        mis.append((i, xk, xy))
c.check("columns_vertically_aligned", not mis,
        f"колонки шапки/тела не выровнены по x: {mis}. Файл: gost732-2017/styles/table.typ")
c.done()
