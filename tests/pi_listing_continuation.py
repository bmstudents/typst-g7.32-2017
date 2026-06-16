"""pi п.6 listing-continuation: длинный листинг -> 'Продолжение листинга 1' на новой странице."""
import helpers as h

c = h.Checks("pi_listing_continuation")
pdf = h.compile("pi_listing_continuation.typ")
t = h.text(pdf)

c.check("multipage", h.page_count(pdf) >= 2,
        f"листинг не перетёк на новую страницу: {h.page_count(pdf)} стр.")
c.check("first_caption", "Листинг 1" in t, "нет первой подписи 'Листинг 1'")
c.check("continuation", "Продолжение листинга 1" in t,
        f"нет 'Продолжение листинга 1' в тексте:\n{t[:500]}")

# 'Продолжение листинга 1' стоит на странице >= 2
ws = h.words(pdf)
pages_prod = [w[0] for w in ws if w[5] == "Продолжение"]
c.check("continuation_on_page2", any(p >= 2 for p in pages_prod),
        f"'Продолжение' не на 2-й странице: страницы={pages_prod}")
c.done()
