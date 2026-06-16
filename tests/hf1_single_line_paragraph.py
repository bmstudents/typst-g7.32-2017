"""hf1 однострочный абзац: его единственная строка — она же последняя, поэтому
имеет красную строку (x0≈120.47), но НЕ растягивается выключкой (xMax < 552.76).
Контроль: следующий многострочный абзац всё же даёт ровный правый край ≈552.76.
"""
import helpers as h

c = h.Checks("hf1_single_line_paragraph")
pdf = h.compile("hf1_single_line_paragraph.typ")

REDLINE = 120.47
RIGHT = 552.76

ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 760]
lines = {}
for w in ws:
    lines.setdefault(round(w[2] / 3) * 3, []).append(w)

rows = []
for y, g in sorted(lines.items()):
    g = sorted(g, key=lambda t: t[1])
    rows.append((min(t[1] for t in g), max(t[3] for t in g),
                 " ".join(t[5] for t in g)))

short1 = next((r for r in rows if r[2].startswith("Короткий")), None)
short2 = next((r for r in rows if r[2].startswith("Ещё")), None)
long_first = next((r for r in rows if r[2].startswith("Длинный")), None)

c.check("all_three_found",
        all(x is not None for x in (short1, short2, long_first)),
        f"короткий1={short1 is not None} короткий2={short2 is not None} "
        f"длинный={long_first is not None}")

for name, r in (("short1", short1), ("short2", short2)):
    if r:
        c.check(f"{name}_redline", abs(r[0] - REDLINE) < 1.5,
                f"однострочный абзац {name} x0={r[0]:.2f}, ждём {REDLINE}")
        c.check(f"{name}_not_justified", r[1] < RIGHT - 80,
                f"однострочный абзац {name} дотянут до x1={r[1]:.2f} (≈{RIGHT}) — "
                f"единственная (=последняя) строка не должна выключаться")

# Многострочный абзац — его ПЕРВАЯ строка выключена по правому краю.
if long_first:
    c.check("multiline_first_line_justified",
            abs(long_first[1] - RIGHT) < 2.5,
            f"первая строка длинного абзаца x1={long_first[1]:.2f}, ждём {RIGHT}")

c.done()
