"""7 cell-helper-renders: ячейка[текст] компилируется и текст виден в pdf."""
import helpers as h

c = h.Checks("ph_cell_renders")
pdf = h.compile("ph_cell_renders.typ")
t = h.text(pdf)

c.check("cell_text_visible", "Видимыйтекст" in t,
        f"текст ячейки не виден в:\n{t}")
c.done()
