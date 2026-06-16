"""hf1 justify: внутренние строки абзаца выключены по правому краю (xMax≈552.76),
а ПОСЛЕДНЯЯ строка не растягивается (короткое слово остаётся у левого поля).

Баг был бы, если justify применяется и к последней строке (typst: justify
по умолчанию НЕ тянет последнюю строку; проверяем, что пакет не сломал это,
например через set par(justify) на блоках или линейку last-line).
"""
import helpers as h

c = h.Checks("hf1_justify_lastline_not_stretched")
pdf = h.compile("hf1_justify_lastline_not_stretched.typ")

RIGHT = 552.76

ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 760]
lines = {}
for w in ws:
    lines.setdefault(round(w[2] / 3) * 3, []).append(w)

# Строки контента — без заголовка (первая строка "Раздел").
rows = []
for y, g in sorted(lines.items()):
    g = sorted(g, key=lambda t: t[1])
    txt = " ".join(t[5] for t in g)
    rows.append((y, max(t[3] for t in g), txt))

# Заголовок — строка, содержащая "Раздел"; исключаем.
body = [r for r in rows if "Раздел" not in r[2]]

c.check("enough_body_lines", len(body) >= 3,
        f"строк тела {len(body)}, нужно >=3 (минимум 2 внутренних + последняя)")

inner = body[:-1]
last = body[-1]

# Все внутренние строки доходят до правого края.
flush = [r for r in inner if abs(r[1] - RIGHT) < 2.5]
c.check("inner_lines_flush_right",
        len(inner) >= 2 and len(flush) == len(inner),
        f"внутренние правые края {[round(r[1], 1) for r in inner]}, ждём все ≈{RIGHT}")

# Последняя строка — одно короткое слово, НЕ дотянута до правого края.
c.check("last_line_not_stretched",
        last[1] < RIGHT - 50,
        f"последняя строка дотянута до x1={last[1]:.2f} (≈{RIGHT}) — "
        f"последняя строка растянута выключкой (баг justify last-line): «{last[2]}»")

# Конкретно: разница между правым краем последней строки и внутренних велика.
gap = RIGHT - last[1]
c.check("last_line_short_margin",
        gap > 100,
        f"остаток правого поля у последней строки {gap:.2f}pt, ждём >100 "
        f"(короткое слово не должно занимать почти всю ширину)")

c.done()
