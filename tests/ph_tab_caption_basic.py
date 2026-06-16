"""1 tab-caption: #таблица(table(...))[Параметры] → видны 'Таблица 1' и 'Параметры'."""
import helpers as h

c = h.Checks("ph_tab_caption_basic")
pdf = h.compile("ph_tab_caption_basic.typ")
t = h.text(pdf)

c.check("supplement_number", "Таблица 1" in t,
        f"нет 'Таблица 1' в тексте:\n{t}")
c.check("caption_word", "Параметры" in t,
        f"нет подписи 'Параметры' в тексте:\n{t}")
c.done()
