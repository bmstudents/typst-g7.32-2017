"""hf1 красная строка: КАЖДЫЙ абзац (первый раздела, после заголовка, после
подзаголовка) начинается с красной строки ровно 1.25см от левого поля.

Инвариант координат: левое поле текста x0=85.04pt (поле 30мм).
Красная строка = 1.25cm = 35.433pt → первое слово абзаца на x≈120.47.
Заголовки идут с тем же отступом (в этом пакете), поэтому абзацы отбираем
как строки, чей текст НЕ совпадает с телом заголовка и начинаются с x≈120.47.
"""
import helpers as h

c = h.Checks("hf1_redline_first_after_heading")
pdf = h.compile("hf1_redline_first_after_heading.typ")

LEFT = 85.04          # левое поле текстового блока
INDENT_PT = 1.25 * 28.3464567  # 1.25см в pt = 35.433
REDLINE = LEFT + INDENT_PT     # 120.47

ws = [w for w in h.words(pdf) if w[2] < 760]

# Группируем в строки по yMin.
lines = {}
for w in ws:
    lines.setdefault(round(w[2] / 3) * 3, []).append(w)

# Для каждой строки — её левый край и текст.
rows = []
for y, g in sorted(lines.items()):
    g = sorted(g, key=lambda t: t[1])
    rows.append((y, min(t[1] for t in g), " ".join(t[5] for t in g)))

# Абзацы основного текста начинаются словами "Самый"/"Второй"/"Первый".
starts = {}
for y, x0, txt in rows:
    for key in ("Самый", "Второй", "Первый абзац подраздела"):
        if txt.startswith(key):
            starts[key] = x0

c.check("found_three_paragraph_starts",
        len(starts) == 3,
        f"ожидали 3 начала абзацев, нашли {list(starts.keys())}")

for key, x0 in starts.items():
    c.check(f"redline_{key.split()[0]}",
            abs(x0 - REDLINE) < 1.5,
            f"абзац «{key}»: левый край первой строки x0={x0:.2f}, "
            f"ждём {REDLINE:.2f} (1.25см от поля {LEFT}) — баг отступа красной строки")

# Точное значение отступа: x0_абзаца - x0_продолжения = 35.43pt.
# Левый край строк-продолжений = LEFT.
cont_lefts = [x0 for y, x0, txt in rows if abs(x0 - LEFT) < 1.0]
c.check("continuation_at_left_margin",
        len(cont_lefts) >= 3,
        f"строк-продолжений у левого поля {len(cont_lefts)}, ждём >=3")

if starts and cont_lefts:
    delta = min(starts.values()) - LEFT
    c.check("indent_is_exactly_125cm",
            abs(delta - INDENT_PT) < 1.0,
            f"отступ красной строки {delta:.2f}pt, ждём {INDENT_PT:.2f} (1.25см)")

c.done()
