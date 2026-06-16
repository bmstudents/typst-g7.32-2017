"""2 tab-caption-top: подпись СВЕРХУ относительно тела — y('Таблица') < y(первая ячейка)."""
import helpers as h

c = h.Checks("ph_tab_caption_top")
pdf = h.compile("ph_tab_caption_top.typ")

y_cap = h.y_of(pdf, "Таблица")
y_body = h.y_of(pdf, "Заголовок")
c.check("found_both", y_cap is not None and y_body is not None,
        f"yТаблица={y_cap} yЗаголовок={y_body}")
c.check("caption_above_body", y_cap is not None and y_body is not None and y_cap < y_body,
        f"подпись не выше тела: yТаблица={y_cap} yЗаголовок={y_body}")
c.done()
