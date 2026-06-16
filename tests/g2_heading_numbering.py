"""g2: нумерация заголовков — 1, 1.1, 1.1.1, 1.2; структурный ВВЕДЕНИЕ без номера."""
import helpers as h

c = h.Checks("g2_heading_numbering")
pdf = h.compile("g2_heading_numbering.typ")
t = h.text(pdf)

c.check("section_1",
        "1 Первый раздел" in t,
        f"нет '1 Первый раздел' в:\n{t[:300]}")

c.check("sub_1_1_and_1_2",
        "1.1 Подраздел один" in t and "1.2 Подраздел два" in t,
        "нет '1.1 Подраздел один' или '1.2 Подраздел два'")

c.check("point_1_1_1",
        "1.1.1 Пункт уровня" in t,
        "нет пункта 3-го уровня '1.1.1 Пункт уровня'")

# Структурный заголовок ВВЕДЕНИЕ — капсом и БЕЗ номера.
c.check("vvedenie_unnumbered",
        "ВВЕДЕНИЕ" in t and "1 ВВЕДЕНИЕ" not in t and "2 ВВЕДЕНИЕ" not in t,
        "ВВЕДЕНИЕ отсутствует или пронумеровано")

# ВВЕДЕНИЕ выровнен по центру текстового поля (cx ≈ 318.9).
vv = [w for w in h.words(pdf) if w[5] == "ВВЕДЕНИЕ"]
content_center = (85.04 + (595.276 - 42.52)) / 2
c.check("vvedenie_centered",
        len(vv) == 1 and abs((vv[0][1] + vv[0][3]) / 2 - content_center) < 15,
        f"ВВЕДЕНИЕ не по центру: {[(round(w[1],1),round(w[3],1)) for w in vv]}, ждём cx~{content_center:.0f}")

c.done()
