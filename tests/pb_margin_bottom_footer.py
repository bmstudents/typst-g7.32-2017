"""pb margin-bottom-20: номер страницы (футер) лежит в нижнем поле — ниже
полосы набора (≈785) и при этом не вылезает за нижний край листа."""
import helpers as h

c = h.Checks("pb_margin_bottom_footer")
pdf = h.compile("pb_margin_bottom_footer.typ")

PH = 841.89
foot = max((w for w in h.words(pdf) if w[0] == 1), key=lambda t: t[2])

c.check("footer_is_number",
        foot[5].isdigit(),
        f"нижнее слово не номер: {foot[5]!r}")

# Футер в полосе нижнего поля: между низом полосы набора (785.2) и краем листа.
c.check("footer_in_bottom_margin",
        785.2 - 2 < foot[2] and foot[4] < PH,
        f"футер yMin={foot[2]:.2f} yMax={foot[4]:.2f}, ждём в полосе 785.2..{PH}")

# И не упирается в самый край листа (есть зазор > 20pt снизу).
c.check("footer_has_clearance",
        PH - foot[4] > 20,
        f"футер слишком близко к краю: зазор снизу {PH - foot[4]:.2f}pt")

c.done()
