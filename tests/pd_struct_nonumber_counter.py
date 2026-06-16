"""pd struct-no-number: структурный ВВЕДЕНИЕ не тратит счётчик —
следующий нумерованный раздел остаётся '1 Анализ'."""
import helpers as h

c = h.Checks("pd_struct_nonumber_counter")
pdf = h.compile("pd_struct_nonumber_counter.typ")
t = h.text(pdf)

c.check("vvedenie_unnumbered",
        "ВВЕДЕНИЕ" in t and "1 ВВЕДЕНИЕ" not in t,
        f"ВВЕДЕНИЕ отсутствует или пронумеровано:\n{t[:400]!r}")

c.check("analysis_is_1",
        "1 Анализ" in t,
        f"раздел после ВВЕДЕНИЕ не получил номер 1:\n{t[:400]!r}")

# Нет '2 Анализ' — счётчик не унаследовал номер от структурного.
c.check("not_2",
        "2 Анализ" not in t,
        f"раздел получил номер 2 (структурный съел счётчик):\n{t[:400]!r}")

c.done()
