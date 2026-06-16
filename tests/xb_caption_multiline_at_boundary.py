"""xb_caption_multiline_at_boundary: длинная многострочная подпись рисунка +
рисунок вытолкнут #v(560pt) к низу страницы. Граничный случай: figure
(image-kind) — единый неразрывный блок «тело + подпись». При нехватке места
весь блок переносится целиком, поэтому вся подпись (все строки) оказывается
на ОДНОЙ странице с рисунком, и ни одна строка подписи не отрывается
(сирота на предыдущей странице)."""
import helpers as h

c = h.Checks("xb_caption_multiline_at_boundary")
pdf = h.compile("xb_caption_multiline_at_boundary.typ")
ws = h.words(pdf)

sup = [w for w in ws if w[5] == "Рисунок"]
assert sup, "нет супплемента 'Рисунок'"
cap_page = sup[0][0]

# Слова подписи на странице рисунка (от 'Рисунок' и ниже, без футера).
caption_words = [w for w in ws
                 if w[0] == cap_page and w[2] >= sup[0][2] and w[2] < 700]
uniq_y = sorted({round(w[2], 1) for w in caption_words})

# «Хвост» подписи — характерные слова с конца длинной подписи.
tail_words = ("окружающей", "среды", "температур", "диапазоне")

# 1. Подпись действительно многострочная (>=3 строки).
c.check("caption_3plus_lines", len(uniq_y) >= 3,
        f"подпись не на 3+ строки: уникальных yMin={len(uniq_y)} ({uniq_y})")

# 2. Ни одно слово подписи (включая хвост) не осталось на другой странице:
#    все вхождения слов подписи — только на cap_page.
sup_word_set = {"Рисунок"} | set(tail_words) | {"Структурная", "схема"}
stray = [(w[0], w[5]) for w in ws
         if w[5] in sup_word_set and w[0] != cap_page]
c.check("no_orphan_caption_line", not stray,
        f"строки подписи оторваны на др. страницу: {stray} (ожидали все на "
        f"стр.{cap_page})")

# 3. Рисунок реально был вытолкнут на новую страницу (#v(560pt) → блок не
#    влез на стр.1 и переехал на стр.2 целиком), и хвост подписи там же.
tail_pages = {w[0] for w in ws if w[5] in tail_words}
c.check("figure_pushed_with_full_caption",
        h.page_count(pdf) == 2 and cap_page == 2 and tail_pages == {2},
        f"рисунок/подпись не на стр.2 целиком: страниц={h.page_count(pdf)}, "
        f"cap_page={cap_page}, хвост на стр.{tail_pages}")

c.done()
