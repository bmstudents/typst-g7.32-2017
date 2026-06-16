"""g6 ТАБЛИЦЫ: длинная таблица вытекает на >1 страницу и даёт «Продолжение таблицы 1»."""
import helpers as h

c = h.Checks("g6_table_continuation")
pdf = h.compile("g6_table_continuation.typ")
t = h.text(pdf)

c.check("multipage", h.page_count(pdf) >= 2, f"таблица не вытекла на 2-ю страницу: {h.page_count(pdf)} стр.")
c.check("first_caption", "Таблица 1 – Длинный перечень" in t,
        f"нет исходной подписи 'Таблица 1' в:\n{t[:300]}")
c.check("continuation", "Продолжение таблицы 1" in t,
        f"нет 'Продолжение таблицы 1' в:\n{t[:600]}")
c.done()
