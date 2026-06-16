"""g7: длинный листинг перетекает на новую страницу -> 'Продолжение листинга 1'."""
import helpers as h

c = h.Checks("g7_listing_continuation")
pdf = h.compile("g7_listing_continuation.typ")
t = h.text(pdf)

c.check("multipage", h.page_count(pdf) >= 2, f"листинг не перетёк на новую страницу: {h.page_count(pdf)} стр.")
c.check("first_caption", "Листинг 1" in t, "нет первой подписи 'Листинг 1'")
c.check("continuation", "Продолжение листинга 1" in t,
        f"нет 'Продолжение листинга 1' в тексте:\n{t[:400]}")
c.done()
