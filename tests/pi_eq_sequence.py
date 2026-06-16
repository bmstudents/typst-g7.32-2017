"""pi п.9 eq-sequence: две блочные формулы нумеруются '(1)' и '(2)'."""
import helpers as h

c = h.Checks("pi_eq_sequence")
pdf = h.compile("pi_eq_sequence.typ")
t = h.text(pdf)

c.check("eq1", "(1)" in t, f"нет '(1)' в:\n{t[:300]}")
c.check("eq2", "(2)" in t, f"нет '(2)' в:\n{t[:300]}")

# Порядок по вертикали: '(1)' выше '(2)'
y1 = h.y_of(pdf, "(1)")
y2 = h.y_of(pdf, "(2)")
c.check("vertical_order", y1 is not None and y2 is not None and y1 < y2,
        f"'(1)' (y={y1}) не выше '(2)' (y={y2})")
c.done()
