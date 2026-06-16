"""pb par-indent-125: красная строка = 1.25см = 35.43pt. Первое слово абзаца
сдвинуто на ~35.43 относительно левого края строк-продолжений."""
import helpers as h

c = h.Checks("pb_indent_125_offset")
pdf = h.compile("pb_indent_125_offset.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 700]

# Первая строка (самый верх) — её левый край.
ys = sorted(set(round(w[2]) for w in ws))
first_line_x = min(w[1] for w in ws if round(w[2]) == ys[0])
# Левый край строки-продолжения (поле).
cont_x = min(w[1] for w in ws if round(w[2]) != ys[0])

indent = first_line_x - cont_x
c.check("indent_35_43",
        abs(indent - 35.43) < 2,
        f"красная строка {indent:.2f}pt, ждём ~35.43 (1.25см); first={first_line_x:.2f} cont={cont_x:.2f}")

# Первая строка сдвинута вправо, продолжение прижато к полю 85.04.
c.check("cont_at_margin",
        abs(cont_x - 85.04) < 2,
        f"продолжение не у поля: {cont_x:.2f}, ждём 85.04")

c.done()
