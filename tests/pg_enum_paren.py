"""pg_enum_paren: нумерованный список — маркеры «1)» «2)» со скобкой, а НЕ «1.» с точкой."""
import helpers as h

c = h.Checks("pg_enum_paren")
pdf = h.compile("pg_enum_paren.typ")
W = h.words(pdf)
t = h.text(pdf)

# Маркеры со скобкой как отдельные «слова» координатного слоя.
toks = {w[5] for w in W}
c.check("paren_1", "1)" in toks, f"нет маркера «1)» среди токенов: {sorted(toks)}")
c.check("paren_2", "2)" in toks, f"нет маркера «2)» среди токенов: {sorted(toks)}")

# Точечной нумерации «1.»/«2.» быть не должно.
c.check("no_dot_numbering", ("1." not in t) and ("2." not in t),
        f"встречена точечная нумерация вместо скобки:\n{t!r}")

c.done()
