"""pd num-multi-section: два раздела -> '1 Первый' и '2 Второй'."""
import helpers as h

c = h.Checks("pd_num_multi_section_basic")
pdf = h.compile("pd_num_multi_section_basic.typ")
t = h.text(pdf)

c.check("section_1",
        "1 Первый" in t,
        f"нет '1 Первый':\n{t[:400]!r}")

c.check("section_2",
        "2 Второй" in t,
        f"нет '2 Второй' (счётчик разделов не дошёл до 2):\n{t[:400]!r}")

c.done()
