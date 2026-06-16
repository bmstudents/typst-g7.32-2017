"""hd5: несколько структурных элементов, перемежающих разделы.

Инвариант: каждый следующий нумерованный раздел получает номер
на единицу больше предыдущего нумерованного раздела, СКОЛЬКО БЫ
структурных элементов между ними ни стояло. Ожидаем 1,2,3.
"""
import re
import helpers as h

c = h.Checks("hd5_multiple_structural_between")
pdf = h.compile("hd5_multiple_structural_between.typ")
t = h.text(pdf)
norm = re.sub(r"[ \t]+", " ", t)

a = re.search(r"(\d+) Раздел альфа", norm)
b = re.search(r"(\d+) Раздел бета", norm)
g = re.search(r"(\d+) Раздел гамма", norm)
na = int(a.group(1)) if a else None
nb = int(b.group(1)) if b else None
ng = int(g.group(1)) if g else None

c.check("alpha_is_1", na == 1, f"'Раздел альфа' получил {na}, ожидался 1")

c.check("beta_is_2", nb == 2,
        f"'Раздел бета' получил {nb}, ожидался 2 "
        f"(структурный ЗАКЛЮЧЕНИЕ обнулил счётчик)")

c.check("gamma_is_3", ng == 3,
        f"'Раздел гамма' получил {ng}, ожидался 3 "
        f"(структурный ТЕРМИНЫ обнулил счётчик)")

c.check("structural_present",
        "ЗАКЛЮЧЕНИЕ" in norm and "ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ" in norm,
        "не найдены оба структурных элемента")

c.done()
