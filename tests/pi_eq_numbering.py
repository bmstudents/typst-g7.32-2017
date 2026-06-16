"""pi п.8 eq-numbering: блочная $ E=m c^2 $ -> '(1)' в тексте у правого края."""
import helpers as h

c = h.Checks("pi_eq_numbering")
pdf = h.compile("pi_eq_numbering.typ")
t = h.text(pdf)

c.check("eq_number", "(1)" in t, f"нет '(1)' в тексте:\n{t[:300]}")

# Номер '(1)' стоит как отдельный токен у правого края страницы.
nums = [w for w in h.words(pdf) if w[5] == "(1)"]
c.check("number_token", len(nums) >= 1, f"нет токена '(1)' в bbox: {[w[5] for w in h.words(pdf)]}")

if nums:
    x1 = max(w[3] for w in nums)
    c.check("right_edge", x1 > 540,
            f"номер '(1)' x1={x1:.1f} не у правого края (ожидалось > 540)")
else:
    c.check("right_edge", False, "нет токена '(1)'")
c.done()
