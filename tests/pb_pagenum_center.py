"""pb page-numbering-config: номер страницы выровнен по центру текстового поля
(cx ≈ 318.9 = центр между полями 30мм и 15мм)."""
import helpers as h

c = h.Checks("pb_pagenum_center")
pdf = h.compile("pb_pagenum_center.typ")

content_center = (85.04 + (595.276 - 42.52)) / 2  # ≈318.9

for page in (1, 2):
    foot = max((w for w in h.words(pdf) if w[0] == page), key=lambda t: t[2])
    cx = (foot[1] + foot[3]) / 2
    c.check(f"centered_p{page}",
            abs(cx - content_center) < 6,
            f"стр{page}: центр номера x={cx:.2f}, ждём ~{content_center:.1f}; слово={foot[5]!r}")

# Номер не прижат к левому/правому краю (явно не left/right alignNum).
foot1 = max((w for w in h.words(pdf) if w[0] == 1), key=lambda t: t[2])
c.check("not_left_aligned",
        foot1[1] > 85.04 + 100,
        f"номер у левого поля (x0={foot1[1]:.2f}) — не по центру")

c.done()
