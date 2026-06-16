"""pc page-justify: у абзаца из >2 строк правый край внутренних строк ровный (xMax≈552)."""
import helpers as h

c = h.Checks("pc_justify_rightedge")
pdf = h.compile("pc_justify_rightedge.typ")

right_edge = 552.76  # правый край текстового поля (A4, поле 15мм)

# Группируем слова страницы 1 по строкам (по yMin с допуском).
ws = sorted((w for w in h.words(pdf) if w[0] == 1), key=lambda t: (round(t[2]), t[1]))
lines = {}
for w in ws:
    key = round(w[2] / 3) * 3      # бакетизация по строкам
    lines.setdefault(key, []).append(w)

# Правый край каждой строки = max xMax её слов. Берём строки контента,
# исключая футер (самое нижнее слово).
foot_y = max(w[2] for w in ws)
line_rights = [max(g, key=lambda t: t[3])[3]
               for y, g in sorted(lines.items()) if y < foot_y - 5]

c.check("more_than_two_lines", len(line_rights) > 2,
        f"строк контента {len(line_rights)}, нужно >2 для проверки выключки")

# Внутренние строки (все кроме последней неполной) выровнены вправо ≈552.
inner = line_rights[:-1]
near = [r for r in inner if abs(r - right_edge) < 3]
c.check("inner_lines_flush_right",
        len(inner) >= 2 and len(near) >= len(inner) - 0,
        f"правые края внутренних строк {[round(r,1) for r in inner]}, ждём все ≈{right_edge}")

# Разброс правых краёв внутренних строк мал (ровный край).
spread = max(inner) - min(inner) if inner else 999
c.check("right_edge_even", spread < 3,
        f"разброс правых краёв {spread:.2f}pt, ждём <3 (ровный)")

c.done()
