"""pd num-subsubsection: полная цепочка 1 / 1.1 / 1.1.1 / 1.1.2 нумеруется корректно."""
import helpers as h

c = h.Checks("pd_num_subsubsection_chain")
pdf = h.compile("pd_num_subsubsection_chain.typ")
t = h.text(pdf)

c.check("level1",
        "1 Альфа" in t,
        f"нет '1 Альфа':\n{t[:400]!r}")

c.check("level3_first",
        "1.1.1 Гамма" in t,
        f"нет '1.1.1 Гамма':\n{t[:400]!r}")

c.check("level3_second",
        "1.1.2 Дельта" in t,
        f"нет '1.1.2 Дельта' (счётчик 3-го уровня не инкрементнулся):\n{t[:400]!r}")

c.done()
