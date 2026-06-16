"""pc footer-bottom: на каждой странице номер у нижнего поля (yMin>780) и ниже контента."""
import helpers as h

c = h.Checks("pc_footer_bottom_multi")
pdf = h.compile("pc_footer_bottom_multi.typ")

for p in range(1, 3):
    ws = [w for w in h.words(pdf) if w[0] == p]
    foot = max(ws, key=lambda t: t[2])
    others = [w for w in ws if w[2] < foot[2]]
    content_max_y = max((w[2] for w in others), default=0)
    c.check(f"page{p}_number_at_bottom",
            foot[5].isdigit() and foot[2] > 780 and foot[2] > content_max_y,
            f"стр.{p}: номер {foot[5]!r} yMin={foot[2]:.1f} (контент_maxY={content_max_y:.1f})")

c.done()
