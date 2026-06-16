"""pc footer-center: центр номера по X совпадает с центром текстового поля (cx≈319±5)."""
import helpers as h

c = h.Checks("pc_footer_center_p1")
pdf = h.compile("pc_footer_center_p1.typ")

cx_field = 319.0  # центр текстового поля A4 при полях 30мм/15мм

# Футер = самое нижнее слово страницы, оно же — номер "1".
foot = max((w for w in h.words(pdf) if w[0] == 1), key=lambda t: t[2])
c.check("footer_is_one", foot[5] == "1", f"нижнее слово = {foot[5]!r}, ждём '1'")

cx = (foot[1] + foot[3]) / 2
c.check("footer_cx_centered",
        abs(cx - cx_field) <= 5,
        f"центр номера x={cx:.1f}, ждём {cx_field:.0f}±5")

c.done()
