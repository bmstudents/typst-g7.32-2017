"""pd num-subsection: два подраздела в разделе -> '1.1' и '1.2' (счётчик инкрементится)."""
import helpers as h

c = h.Checks("pd_num_subsection_multi")
pdf = h.compile("pd_num_subsection_multi.typ")
t = h.text(pdf)

c.check("sub_1_1",
        "1.1 Первый" in t,
        f"нет '1.1 Первый' в:\n{t[:400]!r}")

c.check("sub_1_2",
        "1.2 Второй" in t,
        f"нет '1.2 Второй' в:\n{t[:400]!r}")

# Номер второго подраздела не сбросился в 1.1.
c.check("no_double_1_1",
        t.count("1.1 ") == 1,
        f"'1.1 ' встречается {t.count('1.1 ')} раз, ждём 1")

c.done()
