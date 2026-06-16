"""g8: заголовок 'ПРИЛОЖЕНИЕ А' + название из `содержание`."""
import helpers as h

c = h.Checks("g8_appendix_title")
pdf = h.compile("g8_appendix_title.typ")
t = h.text(pdf)

c.check("appendix_title", "ПРИЛОЖЕНИЕ А" in t, f"нет 'ПРИЛОЖЕНИЕ А' в:\n{t[:200]}")
c.check("appendix_name", "Исходный код программы" in t,
        f"нет названия из `содержание` в:\n{t[:200]}")
# Заголовок выше названия по странице (Y вниз).
y_title = h.y_of(pdf, "ПРИЛОЖЕНИЕ", page=1)
y_name = h.y_of(pdf, "Исходный", page=1)
c.check("title_above_name", y_title is not None and y_name is not None and y_title < y_name,
        f"порядок заголовок/название неверен: title={y_title} name={y_name}")
c.done()
