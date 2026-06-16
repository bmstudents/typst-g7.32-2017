"""pi п.7 listing-pagebreak-top (фикс B1): #v(700pt) перед #листинг -> листинг на стр.2,
первое слово стр.2 начинается от верхнего поля (yMin ≈ 56.25, ±2)."""
import helpers as h

c = h.Checks("pi_listing_pagebreak_top")
pdf = h.compile("pi_listing_pagebreak_top.typ")
t = h.text(pdf)

c.check("pushed_to_page2", h.page_count(pdf) >= 2,
        f"листинг не ушёл на 2-ю страницу: {h.page_count(pdf)} стр.")
c.check("caption_present", "Листинг 1 – Листинг на новой странице" in t,
        f"нет подписи листинга на новой странице в:\n{t}")

fw = h.first_word(pdf, 2)
y_top = fw[0] if fw else None
c.check("starts_at_top_margin", y_top is not None and abs(y_top - 56.25) <= 2,
        f"первое слово стр.2 yMin={y_top}, ожидалось ≈56.25 (это '{fw[1] if fw else None}') — фикс B1")
c.done()
