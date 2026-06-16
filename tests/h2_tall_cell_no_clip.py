"""h2 ТАБЛИЦЫ #4: высокая ячейка (8 строк) вмещает весь текст, без обрезки.

Ячейка с 8 явными строками (ЛИН1..ЛИН8) рядом с одностраничной соседкой.
Ряд таблицы обязан вырасти под содержимое самой высокой ячейки.

ИНВАРИАНТЫ:
  1) все 8 строк ЛИН1..ЛИН8 присутствуют в текстовом слое (ничего не съедено);
  2) строки идут монотонно вниз и с равномерным шагом (~строка 12pt) — нет
     схлопывания/наложения;
  3) нижняя строка ЛИН8 расположена ВЫШЕ следующего ряда (НИЗ1) — высокая
     ячейка не залезла в соседний ряд и не обрезана его границей.
"""
import helpers as h

c = h.Checks("h2_tall_cell_no_clip")
pdf = h.compile("h2_tall_cell_no_clip.typ")
ws = h.words(pdf)

ys = []
missing = []
for i in range(1, 9):
    y = h.y_of(pdf, f"ЛИН{i}")
    if y is None:
        missing.append(i)
    else:
        ys.append((i, y))

c.check("all_lines_present", not missing,
        f"в текстовом слое нет строк {missing} из 8 — ячейка ОБРЕЗАНА. "
        f"Файл: h2_tall_cell_no_clip.typ")

# монотонность и равномерность шага
mono = all(ys[k][1] < ys[k + 1][1] for k in range(len(ys) - 1))
steps = [round(ys[k + 1][1] - ys[k][1], 1) for k in range(len(ys) - 1)]
uniform = mono and steps and (max(steps) - min(steps) < 2.0)
c.check("uniform_baselines", uniform,
        f"строки ячейки не монотонны/неравномерны (наложение?): y={[(i,round(y,1)) for i,y in ys]}, "
        f"шаги={steps}")

# ЛИН8 выше следующего ряда НИЗ1 (высокая ячейка не наехала на соседний ряд)
y8 = h.y_of(pdf, "ЛИН8")
y_next = h.y_of(pdf, "НИЗ1")
single_page = h.page_count(pdf) == 1
c.check("single_page", single_page, f"таблица неожиданно разорвалась: {h.page_count(pdf)} стр.")
c.check("no_clip_into_next_row",
        y8 is not None and y_next is not None and y8 < y_next,
        f"ЛИН8 (yMin={y8}) не выше следующего ряда НИЗ1 (yMin={y_next}) — "
        f"высокая ячейка обрезана/наехала на соседний ряд")

c.done()
