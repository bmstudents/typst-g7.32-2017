"""Рисунки, таблицы и листинги имеют НЕЗАВИСИМЫЕ сквозные счётчики.

Порядок в документе: рис, табл, рис, лист, табл, рис, лист. Ожидаем:
Рисунок 1/2/3, Таблица 1/2, Листинг 1/2 — каждый тип нумеруется своим
счётчиком, не сбиваясь от соседних типов."""
import re
import helpers as h

c = h.Checks("hc_mixed_numbering")
pdf = h.compile("hc_mixed_numbering.typ")
norm = " ".join(h.text(pdf).split())

figs = re.findall(r"Рисунок (\d+)", norm)
tabs = re.findall(r"Таблица (\d+)", norm)
lists = re.findall(r"Листинг (\d+)", norm)

c.check("figures_1_2_3", figs == ["1", "2", "3"], f"рисунки: {figs} (ожид 1,2,3)")
c.check("tables_1_2", tabs == ["1", "2"], f"таблицы: {tabs} (ожид 1,2)")
c.check("listings_1_2", lists == ["1", "2"], f"листинги: {lists} (ожид 1,2)")
c.done()
