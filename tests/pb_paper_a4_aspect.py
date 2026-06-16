"""pb paper-a4: соотношение сторон A4 (~1.414) и текст укладывается в лист
(по координатам слов через h.words, без pdfinfo)."""
import subprocess

import helpers as h

c = h.Checks("pb_paper_a4_aspect")
pdf = h.compile("pb_paper_a4_aspect.typ")

ws = h.words(pdf)
PW, PH = 595.276, 841.89

# Все слова лежат внутри листа A4.
inside = all(0 <= w[1] and w[3] <= PW + 1 and 0 <= w[2] and w[4] <= PH + 1 for w in ws)
c.check("words_inside_page", inside,
        f"есть слово вне границ A4: "
        f"maxX={max(w[3] for w in ws):.1f} maxY={max(w[4] for w in ws):.1f}")

# Соотношение сторон A4 = sqrt(2) ≈ 1.4142.
aspect = PH / PW
c.check("aspect_sqrt2", abs(aspect - 1.41421) < 0.005,
        f"соотношение {aspect:.4f}, ждём ~1.4142")

# Номер страницы (футер) тоже в пределах листа по X и в нижней части.
foot = max((w for w in ws if w[0] == 1), key=lambda t: t[2])
c.check("footer_within_width",
        0 <= foot[1] and foot[3] <= PW,
        f"футер вне ширины листа: x0={foot[1]:.1f} x1={foot[3]:.1f}")

c.done()
