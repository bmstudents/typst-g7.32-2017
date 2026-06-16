"""pc footer-bottom: номер ниже всего контента и близко к низу листа (yMin>780)."""
import helpers as h

c = h.Checks("pc_footer_bottom_below")
pdf = h.compile("pc_footer_bottom_below.typ")

ws = [w for w in h.words(pdf) if w[0] == 1]
foot = max(ws, key=lambda t: t[2])              # самое нижнее слово = номер
content = [w for w in ws if w[5] != foot[5] or w is not foot]
content_ymin = min(w[2] for w in ws if w[5] == "КОНТЕНТМАРКЕР")

c.check("footer_is_number", foot[5].isdigit(),
        f"нижнее слово {foot[5]!r} не число")

c.check("footer_below_content",
        foot[2] > content_ymin,
        f"yMin номера {foot[2]:.1f} не ниже контента {content_ymin:.1f}")

c.check("footer_near_bottom",
        foot[2] > 780,
        f"yMin номера {foot[2]:.1f}, ждём >780 (близко к низу A4 841.9)")

c.done()
