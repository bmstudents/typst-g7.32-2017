"""8 cell-12pt (параметр размер): ячейка(размер:) масштабирует глифы —
ячейка 10pt даёт меньшую высоту глиф-бокса, чем ячейка 14pt."""
import helpers as h

c = h.Checks("ph_cell_size_param")
pdf = h.compile("ph_cell_size_param.typ")
ws = h.words(pdf)

def gh(word):
    hits = [w for w in ws if w[5] == word]
    return (hits[0][4] - hits[0][2]) if hits else None

h_big = gh("Крупно")   # 14pt
h_sm = gh("Мелко")     # 10pt
c.check("found_both", h_big is not None and h_sm is not None,
        f"h_big={h_big} h_sm={h_sm}")
c.check("smaller_size_smaller_glyph", h_big is not None and h_sm is not None and h_sm < h_big,
        f"10pt не меньше 14pt: 14pt={h_big} 10pt={h_sm}")
c.done()
