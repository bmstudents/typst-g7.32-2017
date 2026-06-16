"""hf4_razmer_value: точные значения утилиты размер(n) = 14pt*n - 3pt.

размер(n) задаёт высоту прямоугольника-«ячейки» в строках. Формула
(gost732-2017/utils/image.typ): 14pt * n - 3pt. Печатаем repr(размер(n))
и сверяем с точным ожидаемым значением для n=0,1,2,5,10.
"""
import helpers as h

c = h.Checks("hf4_razmer_value")
pdf = h.compile("hf4_razmer_value.typ")
norm = " ".join(h.text(pdf).split())

expected = {
    1: "11pt",   # 14 - 3
    2: "25pt",   # 28 - 3
    5: "67pt",   # 70 - 3
    10: "137pt", # 140 - 3
    0: "-3pt",   # 0 - 3
}
for n, val in expected.items():
    c.check(
        f"size_{n}",
        f"R{n}={val}" in norm,
        f"размер({n}) != {val} (ожидалось 14pt*{n}-3pt).\n  Текст PDF: {norm[:220]}",
    )

c.done()
