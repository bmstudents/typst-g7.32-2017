"""8 cell-12pt: кегль ячейки (12pt) меньше основного текста (14pt) —
высота глиф-бокса слова из ячейки < высоты слова обычного абзаца."""
import helpers as h

c = h.Checks("ph_cell_12pt")
pdf = h.compile("ph_cell_12pt.typ")
ws = h.words(pdf)

def gh(word):
    hits = [w for w in ws if w[5] == word]
    return (hits[0][4] - hits[0][2]) if hits else None

h_cell = gh("Ячейкатекст")       # содержимое ячейки → 12pt
h_body = gh("Обычныйабзац")      # обычный абзац → 14pt
c.check("found_both", h_cell is not None and h_body is not None,
        f"высота_ячейки={h_cell} высота_абзаца={h_body}")
c.check("cell_smaller", h_cell is not None and h_body is not None and h_cell < h_body,
        f"кегль ячейки не меньше основного: ячейка={h_cell} абзац={h_body}")
c.done()
