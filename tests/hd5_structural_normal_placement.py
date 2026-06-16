"""hd5 (контроль): штатное размещение структурных элементов.

ВВЕДЕНИЕ до разделов, ЗАКЛЮЧЕНИЕ после. Нумерация разделов 1,2,3.
Тест ДОЛЖЕН проходить — он подтверждает, что баг проявляется именно
в неоднозначной комбинации (структурный МЕЖДУ разделами), а не у
структурных элементов вообще.
"""
import re
import helpers as h

c = h.Checks("hd5_structural_normal_placement")
pdf = h.compile("hd5_structural_normal_placement.typ")
t = h.text(pdf)
norm = re.sub(r"[ \t]+", " ", t)

c.check("vvedenie_unnumbered",
        "ВВЕДЕНИЕ" in norm and not re.search(r"\d+ +ВВЕДЕНИЕ", norm),
        "ВВЕДЕНИЕ отсутствует или пронумеровано")

c.check("zaklyuchenie_unnumbered",
        "ЗАКЛЮЧЕНИЕ" in norm and not re.search(r"\d+ +ЗАКЛЮЧЕНИЕ", norm),
        "ЗАКЛЮЧЕНИЕ отсутствует или пронумеровано")

c.check("sections_1_2_3",
        "1 Первый раздел" in norm
        and "2 Второй раздел" in norm
        and "3 Третий раздел" in norm,
        f"нумерация разделов не 1,2,3:\n{norm[:400]}")

c.done()
