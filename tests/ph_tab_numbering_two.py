"""4 tab-numbering: две таблицы → 'Таблица 1' и 'Таблица 2'."""
import helpers as h

c = h.Checks("ph_tab_numbering_two")
pdf = h.compile("ph_tab_numbering_two.typ")
t = h.text(pdf)

c.check("table_1", "Таблица 1 – Первая" in t, f"нет 'Таблица 1 – Первая' в:\n{t}")
c.check("table_2", "Таблица 2 – Вторая" in t, f"нет 'Таблица 2 – Вторая' в:\n{t}")
c.done()
