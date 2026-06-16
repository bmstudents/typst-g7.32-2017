"""g6 ТАБЛИЦЫ: подпись «Таблица 1 — ...» СВЕРХУ относительно тела таблицы."""
import helpers as h

c = h.Checks("g6_table_caption")
pdf = h.compile("g6_table_caption.typ")
t = h.text(pdf)

c.check("supplement_number", "Таблица 1" in t, f"нет 'Таблица 1' в:\n{t}")
c.check("separator", "Таблица 1 — Параметры системы" in t,
        f"подпись с разделителем ' — ' не найдена в:\n{t}")

# Подпись СВЕРХУ: «Таблица» выше первой ячейки тела «Заголовок».
y_cap = h.y_of(pdf, "Таблица")
y_body = h.y_of(pdf, "Заголовок")
c.check("caption_above_body", y_cap is not None and y_body is not None and y_cap < y_body,
        f"yТаблица={y_cap} yЗаголовок={y_body}")
c.done()
