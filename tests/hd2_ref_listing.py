"""hd2: @ref на листинг (kind: raw) даёт номер листинга, раздельный счётчик.

Инвариант: ссылка на 1-й листинг = '1', на 2-й = '2'; совпадает с подписью
'Листинг N'. Раздельный счётчик от рисунков/таблиц.
"""
import re
import helpers as h

c = h.Checks("hd2_ref_listing")
pdf = h.compile("hd2_ref_listing.typ")
t = " ".join(h.text(pdf).split())


def ref(pre, post):
    m = re.search(re.escape(pre) + r"\s+(.+?)\s+" + re.escape(post), t)
    return m.group(1) if m else "<нет>"


r1 = ref("л1до", "л1после")
r2 = ref("л2до", "л2после")

c.check("listing_caption1", re.search(r"Листинг\s+1\b", t) is not None,
        f"нет подписи 'Листинг 1'; текст: {t[:300]}")
c.check("ref_listing1_is_1", r1 == "1", f"ссылка на листинг1 = '{r1}', ожидалось '1'")
c.check("ref_listing2_is_2", r2 == "2", f"ссылка на листинг2 = '{r2}', ожидалось '2'")

c.done()
