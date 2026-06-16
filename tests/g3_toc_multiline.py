"""g3_toc_multiline: длинный заголовок в оглавлении переносится, а номер страницы остаётся справа на последней строке."""
import helpers as h
from collections import defaultdict

c = h.Checks("g3_toc_multiline")
pdf = h.compile("g3_toc_multiline.typ")

# Группируем слова страницы оглавления по строкам (по yMin).
toc = [w for w in h.words(pdf) if w[0] == 1]
lines = defaultdict(list)
for w in toc:
    lines[round(w[2], 1)].append(w)

# Строка, начинающаяся с "1" (запись длинного раздела), и следующая за ней.
ys = sorted(lines)
# индекс первой строки записи раздела: где есть слово 'Очень'
i_first = next(i for i, y in enumerate(ys) if any(w[5] == "Очень" for w in lines[y]))
y_first = ys[i_first]
y_next = ys[i_first + 1]

# Перенос: первая строка НЕ содержит номера страницы (нет финальной цифры у правого края),
# а следующая строка — продолжение того же заголовка (есть слово 'строку'/'оглавления').
def rightmost(y):
    return max(lines[y], key=lambda w: w[3])

first_right = rightmost(y_first)
next_right = rightmost(y_next)

c.check("wrapped_second_line",
        any(w[5] in ("строку", "оглавления", "следующую") for w in lines[y_next]),
        "вторая строка не выглядит продолжением перенесённого заголовка")

# Номер страницы НЕ на первой строке переноса (последнее слово первой строки — не цифра).
c.check("no_pageno_on_first_line",
        not first_right[5].isdigit(),
        f"номер оказался на первой строке: {first_right[5]!r} x1={first_right[3]:.1f}")

# Номер страницы стоит справа на последней (второй) строке, у правого края ≈552pt.
c.check("pageno_right_on_last_line",
        next_right[5].isdigit() and next_right[3] > 540,
        f"номер не у правого края последней строки: word={next_right[5]!r} x1={next_right[3]:.1f}")

c.done()
