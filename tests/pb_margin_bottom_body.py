"""pb margin-bottom-20: на заполненной странице тело текста не опускается ниже
нижней границы полосы набора ≈785pt (841.89 - 20мм). Футер исключаем."""
import helpers as h

c = h.Checks("pb_margin_bottom_body")
pdf = h.compile("pb_margin_bottom_body.typ")

# Берём первую (заведомо полную) страницу.
ws = [w for w in h.words(pdf) if w[0] == 1]
# Футер (номер) живёт ниже полосы набора — отсекаем его (yMin>790).
body = [w for w in ws if w[2] < 790]

PH = 841.89
text_bottom = PH - 56.69  # ≈785.2
lowest = max(w[4] for w in body)

c.check("body_above_bottom_margin",
        lowest <= text_bottom + 2,
        f"низ тела текста yMax={lowest:.2f}pt опускается ниже полосы набора {text_bottom:.1f}")

# Страница реально заполнена (последняя строка близко к низу полосы, < 20pt зазор).
c.check("page_actually_full",
        lowest > text_bottom - 22,
        f"страница не заполнена: низ тела {lowest:.2f}, граница {text_bottom:.1f}")

c.done()
