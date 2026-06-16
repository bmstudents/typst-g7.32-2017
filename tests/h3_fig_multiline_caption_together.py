"""h3 РИСУНКИ: трёхстрочная подпись у низа страницы — ВСЕ её строки И тело на одной странице.

Длинная подпись переносится на 3 строки. В ней расставлены маркеры ОДИНLINE
(стр.1 подписи), ДВАLINE (стр.2), ТРИLINE (стр.3) — каждый падает на свою
строку (проверяем по различающимся yMin). Рисунок вытолкнут #v(15cm) к низу.

ИНВАРИАНТЫ:
  1. подпись реально трёхстрочная: yMin(ОДИНLINE) < yMin(ДВАLINE) < yMin(ТРИLINE);
  2. ни одна строка подписи не оторвана: все три маркера на одной странице;
  3. тело (ТЕЛОМЕТКА) на той же странице, что и подпись, и ВЫШЕ первой строки —
     подпись не разорвана сама и не разлучена с рисунком.
Если block(breakable) разрешит разрыв многострочной подписи на стыке страниц,
часть строк уедет на стр.2 → FAIL.
"""
import helpers as h

c = h.Checks("h3_fig_multiline_caption_together")
pdf = h.compile("h3_fig_multiline_caption_together.typ")
ws = h.words(pdf)


def one(word):
    hits = [w for w in ws if w[5] == word]
    return hits[0] if len(hits) == 1 else None


l1 = one("ОДИНLINE")
l2 = one("ДВАLINE")
l3 = one("ТРИLINE")
body = one("ТЕЛОМЕТКА")

c.check("all_markers_unique",
        all(x is not None for x in (l1, l2, l3, body)),
        f"маркеры найдены не по разу: l1={l1} l2={l2} l3={l3} body={body}")

if all(x is not None for x in (l1, l2, l3, body)):
    # 1. подпись действительно три РАЗНЫЕ строки (строго возрастающий y)
    c.check("caption_is_three_lines", l1[2] < l2[2] < l3[2],
            f"строки подписи не на трёх уровнях: y1={l1[2]:.1f} y2={l2[2]:.1f} y3={l3[2]:.1f}")
    # 2. все три строки подписи на одной странице (ни одна не оторвана)
    cap_pages = {l1[0], l2[0], l3[0]}
    c.check("caption_lines_same_page", len(cap_pages) == 1,
            f"строки подписи раскиданы по страницам {sorted(cap_pages)}: "
            f"ОДИНLINE→стр{l1[0]} ДВАLINE→стр{l2[0]} ТРИLINE→стр{l3[0]} (разрыв подписи)")
    # 3. тело на той же странице И выше первой строки подписи
    body_with_caption = (body[0] == l1[0] == l2[0] == l3[0])
    c.check("body_with_full_caption", body_with_caption and body[4] < l1[2],
            f"ОТРЫВ/неверный порядок: тело ТЕЛОМЕТКА стр{body[0]} yMax={body[4]:.1f}, "
            f"подпись стр{l1[0]} начинается y={l1[2]:.1f}")

c.done()
