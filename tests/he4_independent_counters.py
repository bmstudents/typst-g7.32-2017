"""he4: рисунок, таблица, формула в ОДНОМ разделе, переплетённые ->
независимые счётчики (Рисунок 1..3, Таблица 1..2, формула (1)..(3)).
@ref на каждый объект печатает верный независимый номер.
"""
import re
import helpers as h

c = h.Checks("he4_independent_counters")
pdf = h.compile("he4_independent_counters.typ")
t = " ".join(h.text(pdf).split())

figs = re.findall(r"Рисунок (\d+) —", t)
tabs = re.findall(r"Таблица (\d+) —", t)
# номера формул в самом тексте (не ссылки): три блочные формулы -> (1)(2)(3)
c.check("fig_counter_independent", figs == ["1", "2", "3"],
        f"рисунки: {figs}, ожидалось 1,2,3 (счётчик не должен зависеть от таблиц/формул)")
c.check("tab_counter_independent", tabs == ["1", "2"],
        f"таблицы: {tabs}, ожидалось 1,2 (две таблицы, нумерация своя)")

# --- @ref проверки ---
m = re.search(r"рис=(\S+)\|(\S+)\|(\S+) таб=(\S+)\|(\S+) формулы=(\S+)\|(\S+)\|(\S+)", t)
c.check("refs_parsed", m is not None, f"строка ссылок не распознана: {t[-200:]}")
if m:
    r1, r2, r3, tb1, tb2, e1, e2, e3 = m.groups()
    c.check("ref_fig_numbers", (r1, r2, r3) == ("1", "2", "3"),
            f"ссылки на рисунки: {(r1,r2,r3)}, ожидалось 1,2,3")
    c.check("ref_tab_numbers", (tb1, tb2) == ("1", "2"),
            f"ссылки на таблицы: {(tb1,tb2)}, ожидалось 1,2")
    c.check("ref_eq_numbers", (e1, e2, e3) == ("(1)", "(2)", "(3)"),
            f"ссылки на формулы: {(e1,e2,e3)}, ожидалось (1),(2),(3)")

c.done()
