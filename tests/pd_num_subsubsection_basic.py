"""pd num-subsubsection: '=== Пункт' -> '1.1.1 Пункт' в тексте."""
import helpers as h

c = h.Checks("pd_num_subsubsection_basic")
pdf = h.compile("pd_num_subsubsection_basic.typ")
t = h.text(pdf)

c.check("point_1_1_1",
        "1.1.1 Пункт" in t,
        f"нет '1.1.1 Пункт' в:\n{t[:400]!r}")

c.check("subsection_1_1",
        "1.1 Подраздел" in t,
        f"нет '1.1 Подраздел' в:\n{t[:400]!r}")

c.done()
