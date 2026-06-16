"""hf3_marker_baseline: ИНВАРИАНТ — маркер пункта и его текст лежат на ОДНОЙ
базовой линии (одинаковый yMin), и каждый пункт — на отдельной строке.

Проверяем как enum (N)), так и list (тире). Если рукописный «#h(...) #i) #body \\»
случайно сбивает вертикаль (например, маркер и текст оказались на разных
строках), это поймается. Базовый sanity-инвариант для перечислений.
"""
import helpers as h

c = h.Checks("hf3_marker_baseline")
pdf = h.compile("hf3_marker_baseline.typ")
W = [w for w in h.words(pdf) if w[0] == 1]


def baseline_pair(marker, text):
    mk = next((w for w in W if w[5] == marker), None)
    tx = next((w for w in W if w[5] == text), None)
    return mk, tx


for marker, text in [("1)", "первый"), ("2)", "второй"), ("–", "альфа"), ("–", "бета")]:
    mk = next((w for w in W if w[5] == marker and any(
        abs(t[2] - w[2]) < 2 and t[5] == text for t in W)), None)
    tx = next((w for w in W if w[5] == text), None)
    ok = mk is not None and tx is not None and abs(mk[2] - tx[2]) < 1.0
    detail = ""
    if mk is None or tx is None:
        detail = f"не нашли маркер '{marker}' или текст '{text}'"
    elif abs(mk[2] - tx[2]) >= 1.0:
        detail = (f"маркер '{marker}' yMin={mk[2]:.2f} и текст '{text}' yMin={tx[2]:.2f} "
                  f"на РАЗНЫХ базовых линиях (Δ={abs(mk[2]-tx[2]):.2f}pt)")
    c.check(f"baseline_{text}", ok, detail)

# Каждый из 4 пунктов на своей строке: 4 различных yMin у маркеров.
mk_ys = sorted({round(w[2], 1) for w in W if w[5] in ("1)", "2)", "–")})
c.check("four_distinct_rows", len(mk_ys) == 4,
        f"ожидали 4 строки с маркерами, нашли {len(mk_ys)}: {mk_ys}")

c.done()
