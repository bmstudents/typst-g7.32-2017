"""g6 ТАБЛИЦЫ: таблица, вытолкнутая на новую страницу (#v(700pt)), начинается
от верхнего поля — первое слово стр. 2 имеет yMin ≈ 56.25 (допуск ±2)."""
import helpers as h

c = h.Checks("g6_table_pagebreak_top")
pdf = h.compile("g6_table_pagebreak_top.typ")
t = h.text(pdf)

c.check("pushed_to_page2", h.page_count(pdf) >= 2,
        f"таблица не ушла на 2-ю страницу: {h.page_count(pdf)} стр.")
c.check("caption_present", "Таблица 1 — Параметры на новой странице" in t,
        f"нет подписи на новой странице в:\n{t}")

fw = h.first_word(pdf, 2)
y_top = fw[0] if fw else None
c.check("starts_at_top_margin", y_top is not None and abs(y_top - 56.25) <= 2,
        f"первое слово стр.2 yMin={y_top}, ожидалось ≈56.25 (это '{fw[1] if fw else None}')")
c.done()
