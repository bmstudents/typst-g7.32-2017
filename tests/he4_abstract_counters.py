"""he4: счётчики в реферате (#колво-рисунков и т.д.) == фактическому
числу элементов в документе. Реферат идёт ПЕРВЫМ, значения берутся
через context/final, поэтому это сквозной инвариант на весь док.
"""
import re
import helpers as h

c = h.Checks("he4_abstract_counters")
pdf = h.compile("he4_abstract_counters.typ")
t = " ".join(h.text(pdf).split())

# Значения из реферата
def marker(tag):
    m = re.search(rf"{tag} (\d+) {tag}", t)
    return int(m.group(1)) if m else None

abs_figs = marker("РИС")
abs_tabs = marker("ТАБ")
abs_pages = marker("СТР")
abs_src = marker("ИСТ")
abs_app = marker("ПРИЛ")

# Фактические числа из тела документа
actual_figs = len(re.findall(r"Рисунок \d+ –", t))
actual_tabs = len(re.findall(r"Таблица \d+ –", t))
actual_pages = h.page_count(pdf)
# источники: пронумерованные записи в списке "N. Фамилия"
actual_src = len(re.findall(r"\b(\d+)\. [А-ЯЁ][а-яё]+ [А-ЯЁ]\.", t))

c.check("abstract_markers_present",
        None not in (abs_figs, abs_tabs, abs_pages, abs_src, abs_app),
        f"не все маркеры реферата найдены: {(abs_figs,abs_tabs,abs_pages,abs_src,abs_app)}")

c.check("figs_match", abs_figs == actual_figs == 3,
        f"реферат рисунков={abs_figs}, фактически={actual_figs}, ожидалось 3")
c.check("tabs_match", abs_tabs == actual_tabs == 3,
        f"реферат таблиц={abs_tabs}, фактически={actual_tabs}, ожидалось 3")
c.check("pages_match", abs_pages == actual_pages,
        f"реферат страниц={abs_pages}, фактически={actual_pages}")
c.check("src_match", abs_src == actual_src == 2,
        f"реферат источников={abs_src}, фактически={actual_src}, ожидалось 2")
c.check("app_zero", abs_app == 0,
        f"приложений нет, но реферат показал {abs_app}")

c.done()
