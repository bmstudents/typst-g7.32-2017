"""hd4 ДВУЗНАЧНЫЕ НОМЕРА: 12 блочных формул дают монотонные (1)..(12),
без пропусков и дублей. Двузначные '(10)','(11)','(12)' — корректный формат.
Правый край номеров одинаков для однозначных и двузначных (номер прижат к
правому полю, формат "(1)" => right-align по закрывающей скобке).
"""
import re
import helpers as h

c = h.Checks("hd4_eq_double_digit_align")
pdf = h.compile("hd4_eq_double_digit_align.typ")
t = " ".join(h.text(pdf).split())

nums = re.findall(r"\((\d+)\)", t)
expected = [str(i) for i in range(1, 13)]
c.check("seq_1_to_12",
        nums == expected,
        f"ожидали {expected}, получили {nums}.\nТекст:\n{t}")

c.check("has_double_digits",
        "(10)" in t and "(11)" in t and "(12)" in t,
        f"нет двузначных '(10)/(11)/(12)':\n{t}")

# Правый край: и однозначные, и двузначные номера прижаты к одному правому
# краю (x1 закрывающей скобки совпадает в пределах допуска).
ws = h.words(pdf)
def right_x(token):
    xs = [w[3] for w in ws if w[5] == token]
    return max(xs) if xs else None

x1 = right_x("(1)")
x10 = right_x("(10)")
x12 = right_x("(12)")
c.check("right_edges_aligned",
        None not in (x1, x10, x12) and abs(x1 - x10) < 2 and abs(x1 - x12) < 2,
        f"правые края номеров разъезжаются: x(1)={x1}, x(10)={x10}, x(12)={x12} "
        f"(номер должен быть прижат к правому полю независимо от числа цифр)")

c.done()
