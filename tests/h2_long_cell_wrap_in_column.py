"""h2 ТАБЛИЦЫ #7: длинный текст в колонке переносится и не вылезает за правую
границу таблицы.

columns: (3cm, 1fr). Длинный текст в правой (1fr) колонке должен переноситься
ВНУТРИ ячейки на несколько строк; ни одно слово не должно выходить за правую
границу таблицы (= правое поле страницы).

Геометрия: A4 ширина = 595.28pt, правое поле 15mm = 42.52pt → правый край
тела/таблицы ≈ 552.76pt. Допуск 1pt на округление bbox.

ИНВАРИАНТЫ:
  1) текст реально перенёсся: маркеры ВПРАВО (начало) и КОНЕЦ (конец) на РАЗНЫХ
     базовых линиях (>=3 строки в ячейке);
  2) max xMax всех слов правой колонки <= правая граница таблицы (552.76+1pt) —
     ничего не торчит вправо.
"""
import helpers as h

c = h.Checks("h2_long_cell_wrap_in_column")
pdf = h.compile("h2_long_cell_wrap_in_column.typ")
ws = h.words(pdf)

A4_W = 210 / 25.4 * 72.0
RIGHT_MARGIN = 15 / 25.4 * 72.0
RIGHT_BORDER = A4_W - RIGHT_MARGIN  # ≈ 552.76
TOL = 1.0

# слова правой колонки: на стр.1, в области тела (ниже подписи), x в правой части
y_first = h.y_of(pdf, "ВПРАВО")
y_last = h.y_of(pdf, "КОНЕЦ")

c.check("markers_present", y_first is not None and y_last is not None,
        f"маркеры ВПРАВО={y_first} КОНЕЦ={y_last} — текст не отрендерился целиком")

# многострочность: число различных базовых линий между ВПРАВО и КОНЕЦ
if y_first is not None and y_last is not None:
    cell_words = [w for w in ws if w[0] == 1 and w[2] >= y_first - 0.5 and w[2] <= y_last + 0.5
                  and w[1] > 150]  # правая колонка начинается далеко правее левого поля
    rows = sorted(set(round(w[4], 0) for w in cell_words))
    c.check("multiline_wrap", len(rows) >= 3,
            f"текст в ячейке занял {len(rows)} строк (<3) — перенос не сработал: {rows}")

    max_xmax = max(w[3] for w in cell_words)
    offenders = [(round(w[3], 1), w[5]) for w in cell_words if w[3] > RIGHT_BORDER + TOL]
    c.check("within_right_border", not offenders,
            f"ТЕКСТ ВЫЛЕЗ за правую границу таблицы {RIGHT_BORDER:.1f}pt: "
            f"max xMax={max_xmax:.1f}, нарушители={offenders}. "
            f"Файл: h2_long_cell_wrap_in_column.typ")

c.done()
