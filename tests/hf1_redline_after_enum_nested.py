"""hf1 красная строка восстанавливается у абзаца после нумерованного списка
(enum) и после вложенного маркированного списка. Оба абзаца (AENUM, BNEST)
начинаются с x0≈120.47.

list/enum show-rule в пакете манипулирует горизонтальным отступом
(h(-parIndent)/h(+parIndent)) — проверяем, что это не «протекает» в
следующий абзац и first-line-indent восстановлен.
"""
import helpers as h

c = h.Checks("hf1_redline_after_enum_nested")
pdf = h.compile("hf1_redline_after_enum_nested.typ")

REDLINE = 120.47
LEFT = 85.04
ws = [w for w in h.words(pdf) if w[2] < 760]

lines = {}
for w in ws:
    lines.setdefault((w[0], round(w[2] / 3) * 3), []).append(w)

starts = {}
for (pg, y), g in sorted(lines.items()):
    g = sorted(g, key=lambda t: t[1])
    txt = " ".join(t[5] for t in g)
    for tag in ("AENUM", "BNEST"):
        if txt.startswith(tag) and tag not in starts:
            starts[tag] = (min(t[1] for t in g), max(t[3] for t in g))

c.check("both_paragraphs_found", len(starts) == 2,
        f"нашли {sorted(starts)}, ждём AENUM и BNEST")

c.check("redline_after_enum",
        "AENUM" in starts and abs(starts["AENUM"][0] - REDLINE) < 1.5,
        f"абзац после enum x0={starts.get('AENUM')}, ждём {REDLINE}")

c.check("redline_after_nested_list",
        "BNEST" in starts and abs(starts["BNEST"][0] - REDLINE) < 1.5,
        f"абзац после вложенного списка x0={starts.get('BNEST')}, ждём {REDLINE}")

# Эти абзацы — многострочные и выключены по правому краю (xMax≈552.76),
# т.е. красная строка не «съела» justify.
RIGHT = 552.76
for tag in ("AENUM", "BNEST"):
    if tag in starts:
        c.check(f"{tag}_first_line_justified",
                abs(starts[tag][1] - RIGHT) < 2.5,
                f"первая строка {tag} правый край {starts[tag][1]:.2f}, ждём {RIGHT}")

c.done()
