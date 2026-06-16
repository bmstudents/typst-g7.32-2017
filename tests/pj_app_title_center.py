"""pj 8: 'ПРИЛОЖЕНИЕ А' по центру текстового поля (cx ~ 319 +- 20)."""
import helpers as h

c = h.Checks("pj_app_title_center")
pdf = h.compile("pj_app_title_center.typ")

# Центр поля набора A4: (left 30mm .. right=210-15=195mm) -> середина 112.5mm
# в pt: 112.5 * 72 / 25.4 ~ 318.9.
CX = 319
ws = [w for w in h.words(pdf) if w[5] in ("ПРИЛОЖЕНИЕ", "А") and w[0] == 1]
c.check("title_words_found", len(ws) >= 2,
        f"не нашлись слова заголовка: {ws}")

if len(ws) >= 2:
    x0 = min(w[1] for w in ws)
    x1 = max(w[3] for w in ws)
    cx = (x0 + x1) / 2
    c.check("title_centered", abs(cx - CX) <= 20,
            f"центр заголовка cx={cx:.1f}, ожидался ~{CX}+-20 (x0={x0}, x1={x1})")
else:
    c.check("title_centered", False, "слов заголовка недостаточно для центра")
c.done()
