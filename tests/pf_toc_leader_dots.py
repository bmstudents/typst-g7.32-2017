"""pf_toc_leader_dots: между текстом записи и номером страницы — точки-заполнитель (leader dots)."""
import helpers as h

c = h.Checks("pf_toc_leader_dots")
pdf = h.compile("pf_toc_leader_dots.typ")

toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
toc = [w for w in h.words(pdf) if w[0] == toc_page]

# Строка записи раздела один.
y = next(w[2] for w in toc if w[5] == "один")
line = sorted([w for w in toc if abs(w[2] - y) < 1.0], key=lambda w: w[1])

# Много точек-заполнителей в строке (каждая точка отдельным "словом").
dots = [w for w in line if w[5] == "."]
c.check("many_leader_dots", len(dots) >= 10,
        f"точек-заполнителей в строке записи: {len(dots)} (ожидалось >=10)")

# Точки расположены между текстом ('один') и номером страницы (справа).
text_end = max(w[3] for w in line if w[5] in ("Раздел", "один"))
page_no = max(line, key=lambda w: w[3])
dots_between = [d for d in dots if d[1] > text_end and d[3] < page_no[1] + 0.5]
c.check("dots_between_text_and_pageno", len(dots_between) >= 10,
        f"точек между текстом и номером: {len(dots_between)}")

# Точки тянутся почти до правого края (последняя точка близко к номеру страницы).
if dots_between:
    last_dot = max(dots_between, key=lambda w: w[3])
    c.check("dots_reach_right", last_dot[3] > 530,
            f"заполнитель не доходит до правого края: x1={last_dot[3]:.1f}")

c.done()
