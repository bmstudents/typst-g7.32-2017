"""pi п.1 listing-caption: #листинг(raw(...))[Код] -> 'Листинг 1' + текст подписи."""
import helpers as h

c = h.Checks("pi_listing_caption")
pdf = h.compile("pi_listing_caption.typ")
t = h.text(pdf)

c.check("supplement_number", "Листинг 1" in t,
        f"нет 'Листинг 1' в тексте:\n{t[:300]}")
c.check("caption_body", "Простой код" in t,
        f"нет текста подписи 'Простой код' в:\n{t[:300]}")
# Тело листинга присутствует
c.check("listing_body", "def" in t and "return" in t,
        f"нет тела листинга (def/return) в:\n{t[:300]}")
c.done()
