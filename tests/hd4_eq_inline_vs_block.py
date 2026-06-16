"""hd4 INLINE vs BLOCK: только блочные формулы $ ... $ нумеруются, инлайн $...$
номера НЕ получают. В тексте есть инлайн-формулы и обычные числа 1,2 — они не
должны порождать номера формул. Ровно 2 блочные → ровно (1) и (2), и не больше.
Номер должен стоять у блочной формулы, а не у инлайна (проверяем правый край).
"""
import re
import helpers as h

c = h.Checks("hd4_eq_inline_vs_block")
pdf = h.compile("hd4_eq_inline_vs_block.typ")
t = " ".join(h.text(pdf).split())

# Номера формул в круглых скобках = именно номера, появляются ровно как (1),(2).
nums = re.findall(r"\((\d+)\)", t)
c.check("exactly_two_numbers",
        nums == ["1", "2"],
        f"ожидали ровно два номера блочных формул [1,2], получили {nums}.\n"
        f"Лишние номера = инлайн-формула или число посчитаны как блочные.\nТекст:\n{t}")

# Должны присутствовать (1) и (2).
c.check("has_1_and_2",
        "(1)" in t and "(2)" in t,
        f"нет '(1)'/'(2)':\n{t}")

# Номер блочной формулы прижат к правому краю (инлайн бы стоял в потоке текста,
# не у края). Правое поле A4 при margin right=15mm → x1 ≈ 552.
ws = h.words(pdf)
page_right = max((w[3] for w in ws), default=0)
for token in ("(1)", "(2)"):
    xs = [w[3] for w in ws if w[5] == token]
    x1 = max(xs) if xs else 0
    c.check(f"num_{token}_right_aligned",
            x1 > 0 and abs(x1 - page_right) < 6,
            f"номер {token} x1={x1:.1f} не у правого края (max x1={page_right:.1f}) — "
            f"возможно это инлайн, а не блочная формула")

c.done()
