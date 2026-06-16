"""g5 РИСУНКИ: повёрнуто:true — тело на 90°, подпись «Рисунок N» в тексте горизонтально."""
import helpers as h

c = h.Checks("g5_figure_rotated")
pdf = h.compile("g5_figure_rotated.typ")  # компилируется без ошибки
t = h.text(pdf)

c.check("compiles", h.page_count(pdf) >= 1, "нет страниц")
c.check("supplement", "Рисунок 1" in t, f"нет 'Рисунок 1' в:\n{t}")
# Подпись остаётся читаемой горизонтально в текстовом слое.
c.check("caption_text", "Рисунок 1 – Альбомная схема" in t,
        f"подпись повёрнутого рисунка не найдена в:\n{t}")
c.done()
