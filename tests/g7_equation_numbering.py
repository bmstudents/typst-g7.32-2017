"""g7: две блочные формулы нумеруются '(1)' и '(2)', номер у правого края."""
import helpers as h

c = h.Checks("g7_equation_numbering")
pdf = h.compile("g7_equation_numbering.typ")
t = h.text(pdf)

c.check("eq1_number", "(1)" in t, f"нет '(1)' в тексте:\n{t[:200]}")
c.check("eq2_number", "(2)" in t, f"нет '(2)' в тексте:\n{t[:200]}")

# Номер формулы прижат к правому краю: x1 номера '(1)' больше, чем у обычного
# текста абзаца (например слова 'формула:'). Правое поле A4 = 15mm.
x1_num = max((w[3] for w in h.words(pdf) if w[5] == "(1)"), default=0)
ws = h.words(pdf)
page_right = max((w[3] for w in ws), default=0)
c.check("number_right_aligned", x1_num > 0 and abs(x1_num - page_right) < 5,
        f"номер '(1)' x1={x1_num} не у правого края (max x1={page_right})")
c.done()
