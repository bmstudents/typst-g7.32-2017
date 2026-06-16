"""g4_enum_paren: нумерованный список рендерится со скобкой '1)' '2)', а не точкой '1.'."""
import helpers as h

c = h.Checks("g4_enum_paren")
pdf = h.compile("g4_enum_paren.typ")
t = h.text(pdf)

# Маркеры со скобкой присутствуют.
c.check("paren_1", "1)" in t, f"нет маркера '1)':\n{t!r}")
c.check("paren_2", "2)" in t, f"нет маркера '2)':\n{t!r}")

# Точечной нумерации быть не должно (ни '1.', ни '2.').
c.check("no_dot_numbering", ("1." not in t) and ("2." not in t),
        f"встречена точечная нумерация вместо скобки:\n{t!r}")

c.done()
