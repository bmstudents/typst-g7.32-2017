"""6 tab-continuation: длинная таблица → 'Продолжение таблицы 1' на след. странице,
исходная подпись 'Таблица 1 — Перечень' присутствует."""
import helpers as h

c = h.Checks("ph_tab_continuation_text")
pdf = h.compile("ph_tab_continuation_text.typ")
t = h.text(pdf)

c.check("multipage", h.page_count(pdf) > 1, f"таблица не вытекла: {h.page_count(pdf)} стр.")
c.check("original_caption", "Таблица 1 — Перечень" in t,
        f"нет исходной подписи в:\n{t[:300]}")
c.check("continuation", "Продолжение таблицы 1" in t,
        f"нет 'Продолжение таблицы 1' в:\n{t[:600]}")
c.done()
