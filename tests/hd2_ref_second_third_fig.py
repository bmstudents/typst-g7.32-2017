"""hd2: @ref на 2-й/3-й рисунок даёт '2'/'3', а не '1'. Повторная ссылка совпадает.

Инвариант: ссылка на N-й рисунок == его порядковый номер; несколько ссылок
на один объект одинаковы.
"""
import re
import helpers as h

c = h.Checks("hd2_ref_second_third_fig")
pdf = h.compile("hd2_ref_second_third_fig.typ")
t = " ".join(h.text(pdf).split())


def ref(pre, post):
    m = re.search(re.escape(pre) + r"\s+(.+?)\s+" + re.escape(post), t)
    return m.group(1) if m else "<нет>"


r1 = ref("м1до", "м1после")
r2 = ref("м2до", "м2после")
r3 = ref("м3до", "м3после")
r2b = ref("повтордо", "повторпосле")

c.check("ref_fig1_is_1", r1 == "1", f"ссылка на рис.1 = '{r1}', ожидалось '1'")
c.check("ref_fig2_is_2", r2 == "2", f"ссылка на рис.2 = '{r2}', ожидалось '2'")
c.check("ref_fig3_is_3", r3 == "3", f"ссылка на рис.3 = '{r3}', ожидалось '3'")
c.check("ref_fig2_repeat", r2b == r2 == "2",
        f"повторная ссылка на рис.2 = '{r2b}', ожидалось '2' (= '{r2}')")

c.done()
