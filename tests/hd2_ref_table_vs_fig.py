"""hd2: раздельные счётчики рисунков и таблиц.

Рисунок <f1> и таблица <t1> оба имеют номер 1. Ссылка @f1 должна вести на
рисунок (=1), @t1 — на таблицу (=1), @f2 -> 2, @t2 -> 2. Ссылка не должна
путать счётчики (например, дать таблице номер из общего сквозного счёта).
"""
import re
import helpers as h

c = h.Checks("hd2_ref_table_vs_fig")
pdf = h.compile("hd2_ref_table_vs_fig.typ")
t = " ".join(h.text(pdf).split())


def ref(pre, post):
    m = re.search(re.escape(pre) + r"\s+(.+?)\s+" + re.escape(post), t)
    return m.group(1) if m else "<нет>"


rf1 = ref("рисдо", "риспосле")
rt1 = ref("таблдо", "таблпосле")
rf2 = ref("рис2до", "рис2после")
rt2 = ref("табл2до", "табл2после")

c.check("ref_fig1_is_1", rf1 == "1", f"ссылка на рисунок1 = '{rf1}', ожидалось '1'")
c.check("ref_tab1_is_1", rt1 == "1", f"ссылка на таблицу1 = '{rt1}', ожидалось '1'")
c.check("ref_fig2_is_2", rf2 == "2", f"ссылка на рисунок2 = '{rf2}', ожидалось '2'")
c.check("ref_tab2_is_2", rt2 == "2", f"ссылка на таблицу2 = '{rt2}', ожидалось '2'")

# Подписи должны подтверждать раздельную нумерацию: 'Рисунок 1', 'Таблица 1'.
c.check("caption_fig1", re.search(r"Рисунок\s+1\b", t) is not None,
        "нет подписи 'Рисунок 1'")
c.check("caption_tab1", re.search(r"Таблица\s+1\b", t) is not None,
        "нет подписи 'Таблица 1'")

c.done()
