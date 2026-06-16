"""pb margin-left-30: левая граница текстового поля = 30мм = 85.04pt.
Меряем по левому краю строк-продолжений абзаца (без красной строки)."""
import helpers as h

c = h.Checks("pb_margin_left_border")
pdf = h.compile("pb_margin_left_border.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 700]  # без футера

# Сгруппируем по строкам (по yMin) и возьмём левый край каждой строки.
lines = {}
for w in ws:
    key = round(w[2])
    lines.setdefault(key, []).append(w[1])
left_edges = sorted(min(xs) for xs in lines.values())

# Левая граница поля = минимальный левый край среди строк-продолжений.
# Первая строка имеет красную строку (~120), продолжения — ровно поле 85.04.
border = min(left_edges)
c.check("left_margin_30mm",
        abs(border - 85.04) < 2,
        f"левая граница {border:.2f}pt, ждём ~85.04 (30мм); края строк={[round(x,1) for x in left_edges]}")

# Должно быть минимум 2 строки на одном уровне 85.04 (продолжения абзаца).
at_border = [x for x in left_edges if abs(x - 85.04) < 2]
c.check("multiple_lines_at_border",
        len(at_border) >= 2,
        f"строк-продолжений у поля 85.04: {len(at_border)} (ждём >=2)")

c.done()
