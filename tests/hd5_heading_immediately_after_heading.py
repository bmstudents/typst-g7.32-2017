"""hd5: заголовок сразу за заголовком + структурный впритык.

Инварианты:
- цепочка заголовков без текста между ними нумеруется A=1, A.1=1.1,
  A.1.1=1.1.1 (отсутствие тела не сдвигает счётчики);
- Раздел B = 2;
- ЗАКЛЮЧЕНИЕ между B и C не должно обнулять счётчик: Раздел C = 3,
  его подраздел = 3.1.
"""
import re
import helpers as h

c = h.Checks("hd5_heading_immediately_after_heading")
pdf = h.compile("hd5_heading_immediately_after_heading.typ")
t = h.text(pdf)
norm = re.sub(r"[ \t]+", " ", t)


def num_of(label):
    m = re.search(r"([\d.]+) " + re.escape(label) + r"\b", norm)
    return m.group(1).rstrip(".") if m else None


c.check("chain_without_body",
        num_of("Раздел A") == "1"
        and num_of("Подраздел A.1") == "1.1"
        and num_of("Пункт A.1.1") == "1.1.1",
        f"цепочка без тела: A={num_of('Раздел A')}, "
        f"A.1={num_of('Подраздел A.1')}, A.1.1={num_of('Пункт A.1.1')}; "
        f"ожидались 1, 1.1, 1.1.1")

c.check("section_B_is_2",
        num_of("Раздел B") == "2",
        f"'Раздел B' = {num_of('Раздел B')}, ожидался 2")

c.check("section_C_is_3_after_structural",
        num_of("Раздел C") == "3",
        f"'Раздел C' = {num_of('Раздел C')}, ожидался 3 "
        f"(ЗАКЛЮЧЕНИЕ между B и C обнулило счётчик)")

c.check("sub_C_is_3_1",
        num_of("Подраздел C.1") == "3.1",
        f"'Подраздел C.1' = {num_of('Подраздел C.1')}, ожидался 3.1")

c.done()
