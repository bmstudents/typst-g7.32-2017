"""hf1 два абзаца подряд: у ОБОИХ красная строка (x0≈120.47), и интервал между
абзацами РАВЕН межстрочному (config: spacing == leading == 1.06em).

По ГОСТ 7.32 пустой строки между абзацами быть не должно — абзацы различаются
только красной строкой. Поэтому шаг от последней строки 1-го абзаца к первой
строке 2-го = обычный шаг базовых линий ≈24.1pt, НЕ удвоенный.
"""
import helpers as h

c = h.Checks("hf1_two_paragraphs_spacing")
pdf = h.compile("hf1_two_paragraphs_spacing.typ")

REDLINE = 120.47
PITCH = 24.11

ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 760]
lines = {}
for w in ws:
    lines.setdefault(round(w[2] / 3) * 3, []).append(w)

rows = []
for y, g in sorted(lines.items()):
    g = sorted(g, key=lambda t: t[1])
    rows.append((min(t[2] for t in g), min(t[1] for t in g),
                 " ".join(t[5] for t in g)))

# Красная строка у обоих абзацев.
p1 = next((r for r in rows if r[2].startswith("Первый")), None)
p2 = next((r for r in rows if r[2].startswith("Второй")), None)

c.check("both_paragraphs_found", p1 is not None and p2 is not None,
        f"абзацы: p1={p1 is not None}, p2={p2 is not None}")

if p1 and p2:
    c.check("par1_redline", abs(p1[1] - REDLINE) < 1.5,
            f"1-й абзац x0={p1[1]:.2f}, ждём {REDLINE}")
    c.check("par2_redline", abs(p2[1] - REDLINE) < 1.5,
            f"2-й абзац x0={p2[1]:.2f}, ждём {REDLINE}")

    # Последняя строка 1-го абзаца = строка прямо перед p2.
    before_p2 = [r for r in rows if r[0] < p2[0]]
    last_of_p1 = before_p2[-1]
    gap = p2[0] - last_of_p1[0]

    # Интервал между абзацами равен межстрочному (не удвоен, нет пустой строки).
    c.check("inter_paragraph_gap_equals_leading",
            abs(gap - PITCH) < 1.5,
            f"интервал между абзацами {gap:.2f}pt, ждём {PITCH} (= межстрочный). "
            f"Если ~{2*PITCH:.0f} — между абзацами вставлена пустая строка (баг spacing)")

c.done()
