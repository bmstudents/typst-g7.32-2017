"""pj 6: буква-в-иллюстрациях:нет -> 'Рисунок 1' (без буквы)."""
import helpers as h

c = h.Checks("pj_app_figure_letter_off")
pdf = h.compile("pj_app_figure_letter_off.typ")
t = " ".join(h.text(pdf).split())

c.check("figure_no_letter", "Рисунок 1" in t,
        f"подпись не 'Рисунок 1':\n{t[:400]}")
c.check("no_letter_prefix", "Рисунок А.1" not in t,
        f"буква попала в подпись, хотя отключена:\n{t[:400]}")
c.check("caption_body", "Схема устройства" in t,
        f"нет тела подписи в:\n{t[:400]}")
c.done()
