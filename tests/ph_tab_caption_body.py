"""1 tab-caption (другой аспект): подпись и тело таблицы сосуществуют —
видны и слово подписи, и содержимое ячеек таблицы; ровно одна 'Таблица'."""
import helpers as h

c = h.Checks("ph_tab_caption_body")
pdf = h.compile("ph_tab_caption_body.typ")
t = h.text(pdf)

c.check("caption_visible", "Параметры" in t, f"нет подписи в:\n{t}")
c.check("body_cells_visible", "Альфа" in t and "Бета" in t,
        f"содержимое ячеек не видно в:\n{t}")
# Ровно одна таблица — слово 'Таблица' встречается один раз.
c.check("single_supplement", t.count("Таблица") == 1,
        f"ожидалось одно слово 'Таблица', нашлось {t.count('Таблица')}")
c.done()
