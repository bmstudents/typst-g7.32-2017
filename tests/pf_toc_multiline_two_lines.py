"""pf_toc_multiline_two_lines: длинная запись занимает >=2 строки; первая строка начинается с номера '1', номер страницы только в конце записи."""
import helpers as h
from collections import defaultdict

c = h.Checks("pf_toc_multiline_two_lines")
pdf = h.compile("pf_toc_multiline_two_lines.typ")

toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
toc = [w for w in h.words(pdf) if w[0] == toc_page]
lines = defaultdict(list)
for w in toc:
    lines[round(w[2], 1)].append(w)
ys = sorted(lines)

# Строка, где начинается запись (содержит номер '1' и слово 'Чрезвычайно').
i_first = next(i for i, y in enumerate(ys)
               if any(w[5] == "Чрезвычайно" for w in lines[y]))
y_first = ys[i_first]

# Запись занимает не менее двух строк: между первой строкой записи и строкой
# с заключительным словом 'перенеслось' есть промежуточная строка.
i_last = next(i for i, y in enumerate(ys)
              if any(w[5] == "перенеслось" for w in lines[y]))
c.check("entry_multiline", i_last - i_first >= 1,
        f"заголовок не перенёсся: строка начала={i_first}, строка конца={i_last}")

# Номер раздела '1' — на первой строке записи, у левого поля.
prefix = next((w for w in lines[y_first] if w[5] == "1"), None)
c.check("prefix_on_first_line", prefix is not None and prefix[1] < 110,
        f"номер '1' не в начале первой строки записи: {prefix}")

# Ровно один числовой номер страницы у правого края во ВСЕХ строках записи
# (от первой строки до завершающей включительно) — и он на последней строке.
entry_ys = ys[i_first:i_last + 1]
right_pagenos = [w for y in entry_ys for w in lines[y]
                 if w[5].isdigit() and w[3] > 540]
c.check("single_pageno", len(right_pagenos) == 1,
        f"номеров страницы у правого края: {len(right_pagenos)} (ожидался 1): "
        f"{[(w[5], round(w[2],1)) for w in right_pagenos]}")
if right_pagenos:
    y_last = ys[i_last]
    c.check("pageno_on_last", abs(right_pagenos[0][2] - y_last) < 1.0,
            f"единственный номер не на последней строке записи: "
            f"y={right_pagenos[0][2]} y_last={y_last}")

c.done()
