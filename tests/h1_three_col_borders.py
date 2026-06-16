"""h1 ТАБЛИЦЫ #6 — ТРИ КОЛОНКИ: ЛЕВЫЙ КРАЙ У ПОЛЯ + РАВНОМЕРНОСТЬ.

Таблица из 3 колонок (columns: 3 → auto-ширина). Проверяем два независимых
свойства:
  A) ЛЕВЫЙ КРАЙ тела ≈ левое поле (x0 первой колонки близко к 85). По ГОСТ
     таблица идёт от левого поля. — ОЖИДАЕМЫЙ БАГ: auto-таблица центрируется
     блоком, левый край уезжает к ~274.
  B) РАВНОМЕРНОСТЬ: при равной ширине ячеек центры трёх колонок
     равноотстоят (шаг между центрами col1→col2 ≈ col2→col3, ±3pt). Это
     свойство сохраняется даже у центрированной таблицы — отдельный
     инвариант сетки.

Колонки идентифицируем по верхней строке К1/К2/К3 (и проверяем, что нижняя
строка a/b/c стоит под теми же центрами).
"""
import helpers as h

c = h.Checks("h1_three_col_borders")
pdf = h.compile("h1_three_col_borders.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and 95 < w[2] < 700]

LEFT = 85.04

def cx(word):
    hit = [w for w in ws if w[5] == word]
    return None if not hit else (hit[0][1] + hit[0][3]) / 2

def x0(word):
    hit = [w for w in ws if w[5] == word]
    return None if not hit else hit[0][1]

cols = [cx("К1"), cx("К2"), cx("К3")]
c.check("three_columns_present", all(v is not None for v in cols),
        f"не все заголовки колонок найдены: {[(w[5]) for w in ws]}")

if all(v is not None for v in cols):
    # A) левый край у поля.
    left_x0 = x0("К1")
    c.check(
        "left_edge_near_margin",
        left_x0 < LEFT + 30,
        f"левый край тела (К1 x0={left_x0:.2f}) далеко от поля {LEFT} "
        f"(отрыв {left_x0 - LEFT:.1f}pt > 30). Auto-таблица центрирована блоком. "
        f"Файл: gost732-2017/styles/figure.typ — it.body без align(left).",
    )

    # B) равномерность шага центров колонок.
    step1 = cols[1] - cols[0]
    step2 = cols[2] - cols[1]
    c.check(
        "columns_evenly_spaced",
        abs(step1 - step2) <= 3,
        f"колонки неравномерны: шаг1={step1:.2f}, шаг2={step2:.2f}, "
        f"|Δ|={abs(step1 - step2):.2f} > 3pt (центры {[round(v, 1) for v in cols]}).",
    )

    # C) нижняя строка под теми же центрами (сетка вертикальна).
    bot = [cx("a"), cx("b"), cx("c")]
    if all(v is not None for v in bot):
        max_dev = max(abs(b - t) for b, t in zip(bot, cols))
        # допуск 7pt: cx() меряет центр СЛОВА, а метки верх/низ разной ширины
        # («К1»=2 симв. vs «a»=1), их центры расходятся на ~5pt даже при
        # идеально ровной сетке колонок — это не перекос таблицы
        c.check(
            "second_row_under_columns",
            max_dev <= 7,
            f"вторая строка не под центрами колонок: верх={[round(v,1) for v in cols]}, "
            f"низ={[round(v,1) for v in bot]}, max отклонение {max_dev:.2f}pt > 7.",
        )

c.done()
