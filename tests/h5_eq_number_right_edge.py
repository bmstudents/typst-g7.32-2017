"""h5_eq_number_right_edge: блочная формула $E=m c^2$ → номер «(1)» прижат к правому
краю текстового блока (x правого края > 540, ≈552), и номер ПРАВЕЕ тела формулы.

Жёсткость: измеряем абсолютный правый край (x1) токена «(1)» против правого поля
A4 (210мм − 15мм = 552.76pt) и против правого края тела формулы. Не «номер есть»,
а его геометрическое положение.
"""
import helpers as h

c = h.Checks("h5_eq_number_right_edge")
pdf = h.compile("h5_eq_number_right_edge.typ")
W = h.words(pdf)

# Правый край печатной области A4: 210мм − 15мм правое поле ≈ 552.76pt.
RIGHT_EDGE = (210 - 15) * 2.83464567  # ≈ 552.76

nums = [w for w in W if w[5] == "(1)"]
c.check("number_present", len(nums) == 1,
        f"ожидали ровно один токен «(1)», нашли {len(nums)}: {[w[5] for w in W]}")

if nums:
    x1 = max(w[3] for w in nums)
    # 1) Правый край номера за 540pt.
    c.check("x_gt_540", x1 > 540,
            f"правый край «(1)» x1={x1:.2f} ≤ 540 — номер не прижат к полю")
    # 2) Правый край номера совпадает с правым полем A4 ±3pt.
    c.check("x_at_right_margin", abs(x1 - RIGHT_EDGE) < 3,
            f"правый край «(1)» x1={x1:.2f} ≠ правому полю {RIGHT_EDGE:.2f} (±3)")

    # 3) Номер строго правее всего тела формулы (E, =, m, c, …).
    body = [w for w in W if w[5] not in ("(1)", "Раздел")
            and w[2] < 800 and abs(w[2] - nums[0][2]) < 60 and w is not nums[0]]
    body = [w for w in body if w[5] != "(1)"]
    if body:
        x_body_max = max(w[3] for w in body if w[1] < x1)
        c.check("right_of_body", x1 > x_body_max,
                f"номер (x1={x1:.2f}) не правее тела формулы (x_max={x_body_max:.2f})")
    else:
        c.check("right_of_body", False, "тело формулы не распознано в координатном слое")

c.done()
