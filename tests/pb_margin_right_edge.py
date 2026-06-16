"""pb margin-right-15: правый край текста (max xMax заполненных строк) ≈552.76pt."""
import helpers as h

c = h.Checks("pb_margin_right_edge")
pdf = h.compile("pb_margin_right_edge.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 700]

max_x1 = max(w[3] for w in ws)
c.check("right_edge_552",
        abs(max_x1 - 552.76) < 2,
        f"правый край текста {max_x1:.2f}pt, ждём ~552.76")

# При выключке по ширине несколько строк дотягиваются почти до края.
# Сгруппируем строки и посмотрим правые края.
lines = {}
for w in ws:
    lines.setdefault(round(w[2]), []).append(w[3])
rights = sorted(max(xs) for xs in lines.values())
near = [r for r in rights if abs(r - 552.76) < 2]
c.check("justified_to_right",
        len(near) >= 2,
        f"строк, дотянутых до правого поля: {len(near)} (ждём >=2); края={[round(r,1) for r in rights]}")

c.done()
