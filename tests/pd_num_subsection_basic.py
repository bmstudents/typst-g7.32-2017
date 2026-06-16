"""pd num-subsection: '== Подраздел' -> '1.1 Подраздел' в тексте."""
import helpers as h

c = h.Checks("pd_num_subsection_basic")
pdf = h.compile("pd_num_subsection_basic.typ")
t = h.text(pdf)

c.check("subsection_numbered",
        "1.1 Подраздел" in t,
        f"нет '1.1 Подраздел' в:\n{t[:400]!r}")

# Раздел тоже на месте с номером '1'.
c.check("section_numbered",
        "1 Раздел" in t,
        f"нет '1 Раздел' в:\n{t[:400]!r}")

c.done()
