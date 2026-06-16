"""9 cell-align: ячейка(выравнивание: center) и (right) в одной колонке дают
разные x — правое слово начинается правее центрированного."""
import helpers as h

c = h.Checks("ph_cell_align")
pdf = h.compile("ph_cell_align.typ")
ws = h.words(pdf)

def x0(word):
    hits = [w for w in ws if w[5] == word]
    return hits[0][1] if hits else None

x_center = x0("Цент")
x_right = x0("Прав")
c.check("found_both", x_center is not None and x_right is not None,
        f"xЦент={x_center} xПрав={x_right}")
c.check("right_further_right", x_center is not None and x_right is not None and x_right > x_center,
        f"right не правее center: xЦент={x_center} xПрав={x_right}")
c.done()
