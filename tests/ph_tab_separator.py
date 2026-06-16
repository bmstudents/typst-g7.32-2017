"""3 tab-caption-separator: цельная строка подписи 'Таблица 1 — Параметры'
(supplement, номер, разделитель-тире, подпись в одну строку)."""
import helpers as h

c = h.Checks("ph_tab_separator")
pdf = h.compile("ph_tab_separator.typ")
t = h.text(pdf)

c.check("full_caption_line", "Таблица 1 — Параметры" in t,
        f"нет цельной подписи с разделителем ' — ' в:\n{t}")
c.done()
