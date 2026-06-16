"""9 cell-align (left vs right): в одной колонке left-слово начинается левее,
чем right-слово (x0(left) < x0(right))."""
import helpers as h

c = h.Checks("ph_cell_align_left_right")
pdf = h.compile("ph_cell_align_left_right.typ")
ws = h.words(pdf)

def x0(word):
    hits = [w for w in ws if w[5] == word]
    return hits[0][1] if hits else None

x_left = x0("Лев")
x_right = x0("Пра")
c.check("found_both", x_left is not None and x_right is not None,
        f"xЛев={x_left} xПра={x_right}")
c.check("left_before_right", x_left is not None and x_right is not None and x_left < x_right,
        f"left не левее right: xЛев={x_left} xПра={x_right}")
c.done()
