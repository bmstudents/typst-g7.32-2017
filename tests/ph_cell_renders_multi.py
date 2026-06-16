"""7 cell-helper-renders (несколько ячеек): все четыре ячейки видны и стоят
на своих местах — две колонки (x различаются), две строки (y различаются)."""
import helpers as h

c = h.Checks("ph_cell_renders_multi")
pdf = h.compile("ph_cell_renders_multi.typ")
t = h.text(pdf)
ws = h.words(pdf)

for w in ("Альфа", "Бета", "Гамма", "Дельта"):
    c.check(f"visible_{w}", w in t, f"ячейка '{w}' не видна в:\n{t}")

def pos(word):
    hits = [w for w in ws if w[5] == word]
    return (hits[0][1], hits[0][2]) if hits else None

a, b = pos("Альфа"), pos("Бета")
g = pos("Гамма")
# Две колонки: x(Бета) > x(Альфа).
c.check("two_columns", a and b and b[0] > a[0],
        f"колонки не разнесены по x: Альфа={a} Бета={b}")
# Две строки: y(Гамма) > y(Альфа).
c.check("two_rows", a and g and g[1] > a[1],
        f"строки не разнесены по y: Альфа={a} Гамма={g}")
c.done()
