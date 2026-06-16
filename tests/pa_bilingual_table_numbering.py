"""pa_bilingual-table (аспект 2): таблицы от #table_figure и #таблица делят общий
счётчик и формат подписи 'Таблица N – подпись'. Первая (#table_figure) →
'Таблица 1', вторая (#таблица) → 'Таблица 2'. Подпись стоит НАД телом таблицы
(position: top)."""
import helpers as h

c = h.Checks("pa_bilingual_table_numbering")
pdf = h.compile("pa_bilingual_table_numbering.typ")
t = h.text(pdf)

c.check("first_is_1", "Таблица 1 – Первая" in t,
        f"подпись #table_figure не 'Таблица 1 – Первая':\n{t!r}")
c.check("second_is_2", "Таблица 2 – Вторая" in t,
        f"подпись #таблица не 'Таблица 2 – Вторая' (общий счётчик):\n{t!r}")

# Подпись 'Таблица' стоит выше первой ячейки тела таблицы 'A' (caption top).
y_cap = h.y_of(pdf, "Таблица", nth=1)
y_body = h.y_of(pdf, "A", nth=1)
c.check("caption_above_body",
        y_cap is not None and y_body is not None and y_cap < y_body,
        f"подпись не над телом: yТаблица={y_cap} yA={y_body}")
c.done()
