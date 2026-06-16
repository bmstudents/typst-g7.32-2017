"""pb margin-right-15: само правое поле = ширина листа - правый край ≈42.52pt (15мм),
и оно ровно вдвое меньше левого (30мм)."""
import helpers as h

c = h.Checks("pb_margin_right_value")
pdf = h.compile("pb_margin_right_value.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 700]

PW = 595.276
max_x1 = max(w[3] for w in ws)
min_x0 = min(w[1] for w in ws)  # = левое поле (продолжения строк)

right_margin = PW - max_x1
c.check("right_margin_15mm",
        abs(right_margin - 42.52) < 2,
        f"правое поле {right_margin:.2f}pt, ждём ~42.52 (15мм)")

# 15мм vs 30мм: правое поле примерно вдвое меньше левого.
c.check("right_half_of_left",
        abs(min_x0 - 2 * right_margin) < 5,
        f"левое {min_x0:.2f} != 2*правое {2*right_margin:.2f}")

c.done()
