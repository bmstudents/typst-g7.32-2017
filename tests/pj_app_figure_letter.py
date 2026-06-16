"""pj 5: рис в приложении с буква-в-иллюстрациях:да -> 'Рисунок А.1'."""
import helpers as h

c = h.Checks("pj_app_figure_letter")
pdf = h.compile("pj_app_figure_letter.typ")
t = " ".join(h.text(pdf).split())

c.check("figure_letter", "Рисунок А.1" in t,
        f"подпись не пронумерована буквой 'А.1':\n{t[:400]}")
c.check("caption_body", "Схема устройства" in t,
        f"нет тела подписи в:\n{t[:400]}")
c.done()
