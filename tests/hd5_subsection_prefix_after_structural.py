"""hd5: префикс подраздела после структурного элемента.

Инвариант: первый раздел = 1 (подраздел 1.1); после ВВЕДЕНИЯ второй
раздел = 2, его подразделы = 2.1 и 2.2. Если структурный элемент
обнуляет счётчик раздела, подразделы станут 1.1/1.2 — это ловит баг
ещё и на уровне подразделов.
"""
import re
import helpers as h

c = h.Checks("hd5_subsection_prefix_after_structural")
pdf = h.compile("hd5_subsection_prefix_after_structural.typ")
t = h.text(pdf)
norm = re.sub(r"[ \t]+", " ", t)

# Первый раздел и его подраздел — эталон до структурного.
c.check("first_section_1_1",
        "1 Первый раздел" in norm and "1.1 Подраздел первого" in norm,
        f"нет '1 Первый раздел'/'1.1 Подраздел первого':\n{norm[:400]}")

# Второй раздел должен быть номером 2.
m2 = re.search(r"(\d+) Второй раздел", norm)
n2 = int(m2.group(1)) if m2 else None
c.check("second_section_is_2", n2 == 2,
        f"'Второй раздел' получил {n2}, ожидался 2")

# Подразделы второго раздела должны иметь префикс 2.
pa = re.search(r"(\d+)\.(\d+) Подраздел второго A", norm)
pb = re.search(r"(\d+)\.(\d+) Подраздел второго B", norm)
c.check("sub_a_is_2_1",
        pa is not None and (int(pa.group(1)), int(pa.group(2))) == (2, 1),
        f"'Подраздел второго A' = {pa.group(0) if pa else None}, ожидался '2.1 …'")
c.check("sub_b_is_2_2",
        pb is not None and (int(pb.group(1)), int(pb.group(2))) == (2, 2),
        f"'Подраздел второго B' = {pb.group(0) if pb else None}, ожидался '2.2 …'")

c.done()
