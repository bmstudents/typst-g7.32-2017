"""pj 10: два приложения 'А' и 'Б' (scope) -> оба заголовка корректны."""
import helpers as h

c = h.Checks("pj_app_letter_different")
pdf = h.compile("pj_app_letter_different.typ")
t = " ".join(h.text(pdf).split())

c.check("title_a", "ПРИЛОЖЕНИЕ А" in t,
        f"нет 'ПРИЛОЖЕНИЕ А' в:\n{t[:400]}")
c.check("title_b", "ПРИЛОЖЕНИЕ Б" in t,
        f"нет 'ПРИЛОЖЕНИЕ Б' в:\n{t[:400]}")
c.check("name_a", "Первое приложение" in t,
        f"нет названия 'Первое приложение' в:\n{t[:400]}")
c.check("name_b", "Второе приложение" in t,
        f"нет названия 'Второе приложение' в:\n{t[:400]}")

# Порядок: А раньше Б по документу.
y_a = None
y_b = None
for (p, x0, y0, x1, y1, w) in h.words(pdf):
    if w == "А" and y_a is None:
        # ищем строку 'ПРИЛОЖЕНИЕ А' — нужна страница, где есть ПРИЛОЖЕНИЕ
        pass
# Проще: первое появление 'ПРИЛОЖЕНИЕ' раньше первого 'Б'-заголовка.
import re
flat = h.text(pdf)
ia = flat.find("ПРИЛОЖЕНИЕ А")
ib = flat.find("ПРИЛОЖЕНИЕ Б")
c.check("order_a_before_b", ia != -1 and ib != -1 and ia < ib,
        f"порядок приложений неверен: idx_A={ia} idx_B={ib}")
c.done()
