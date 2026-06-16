"""hf2: многостраничная нумерация 1..11 — монотонна, без пропусков/дублей,
двузначные номера остаются по центру полосы набора.
"""
import helpers as h

c = h.Checks("hf2_multipage_monotonic")
pdf = h.compile("hf2_multipage_monotonic.typ")

n = h.page_count(pdf)
c.check("eleven_pages", n == 11, f"страниц {n}, ждём 11")

# Нижний номер каждой страницы.
foots = [h.footer_word(pdf, p) for p in range(1, n + 1)]

c.check("all_digits",
        all(f is not None and f.isdigit() for f in foots),
        f"не все футеры — числа: {foots}")

# Строгая монотонность 1,2,...,11.
expected = [str(i) for i in range(1, n + 1)]
c.check("strict_sequence",
        foots == expected,
        f"последовательность {foots}, ждём {expected}")

# Двузначные (10, 11) центрированы так же, как однозначные.
CONTENT_CX = (85.04 + (595.276 - 42.52)) / 2  # 318.9
cxs = {}
for p in range(1, n + 1):
    nums = [w for w in h.words(pdf) if w[0] == p and w[2] > 700 and w[5].isdigit()]
    if nums:
        f = max(nums, key=lambda t: t[2])
        cxs[foots[p - 1]] = (f[1] + f[3]) / 2

bad = {k: round(v, 1) for k, v in cxs.items() if abs(v - CONTENT_CX) >= 5}
c.check("double_digits_centered",
        not bad,
        f"номера не по центру {CONTENT_CX:.1f}: {bad}")

# Конкретно проверяем, что 1 и 11 имеют одинаковый центр (двузначное не сместило).
if "1" in cxs and "11" in cxs:
    c.check("single_vs_double_same_center",
            abs(cxs["1"] - cxs["11"]) < 2,
            f"центр '1'={cxs['1']:.2f} != центр '11'={cxs['11']:.2f}")

c.done()
