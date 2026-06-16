"""pi п.10 eq-number-right: номер блочной формулы прижат к правому краю (x номера > 540)."""
import helpers as h

c = h.Checks("pi_eq_number_right")
pdf = h.compile("pi_eq_number_right.typ")
ws = h.words(pdf)

nums = [w for w in ws if w[5] == "(1)"]
c.check("number_present", len(nums) >= 1,
        f"нет токена '(1)' в bbox: {[w[5] for w in ws]}")

if nums:
    x1 = max(w[3] for w in nums)
    c.check("x_gt_540", x1 > 540,
            f"x1 номера '(1)' = {x1:.1f}, ожидалось > 540 (правый край ≈552)")

    # Номер правее тела формулы (тело по центру/слева, номер справа)
    body = [w for w in ws if w[5] in ("=", "+", "kx") or w[5].startswith("y")]
    if body:
        x_body_max = max(w[3] for w in body)
        c.check("right_of_body", x1 > x_body_max,
                f"номер (x1={x1:.1f}) не правее тела формулы (x_max={x_body_max:.1f})")
    else:
        c.check("right_of_body", x1 > 540, "тело формулы не распознано — проверяем по краю")
else:
    c.check("x_gt_540", False, "нет токена '(1)'")
    c.check("right_of_body", False, "нет токена '(1)'")
c.done()
