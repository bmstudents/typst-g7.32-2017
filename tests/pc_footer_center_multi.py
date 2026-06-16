"""pc footer-center: номер по центру на КАЖДОЙ из 3 страниц (cx≈319±5)."""
import helpers as h

c = h.Checks("pc_footer_center_multi")
pdf = h.compile("pc_footer_center_multi.typ")
cx_field = 319.0

for p in range(1, 4):
    foot = max((w for w in h.words(pdf) if w[0] == p), key=lambda t: t[2])
    cx = (foot[1] + foot[3]) / 2
    c.check(f"page{p}_centered",
            foot[5].isdigit() and abs(cx - cx_field) <= 5,
            f"стр.{p}: номер {foot[5]!r} cx={cx:.1f}, ждём {cx_field:.0f}±5")

c.done()
