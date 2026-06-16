"""g8: рисунок внутри приложения нумеруется буквой приложения -> 'Рисунок А.1'."""
import helpers as h

c = h.Checks("g8_appendix_figure_letter")
pdf = h.compile("g8_appendix_figure_letter.typ")
t = h.text(pdf)

c.check("appendix_title", "ПРИЛОЖЕНИЕ А" in t, f"нет 'ПРИЛОЖЕНИЕ А' в:\n{t[:200]}")
c.check("figure_letter_number", "Рисунок А.1" in t,
        f"подпись рисунка не пронумерована буквой приложения 'А.1':\n{t[:300]}")
c.check("figure_caption_body", "Схема устройства" in t,
        f"нет текста подписи рисунка в:\n{t[:300]}")
c.done()
