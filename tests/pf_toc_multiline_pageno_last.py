"""pf_toc_multiline_pageno_last: длинный заголовок переносится; номер страницы на ПОСЛЕДНЕЙ строке, не на первой."""
import helpers as h
from collections import defaultdict

c = h.Checks("pf_toc_multiline_pageno_last")
pdf = h.compile("pf_toc_multiline_pageno_last.typ")

toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
toc = [w for w in h.words(pdf) if w[0] == toc_page]
lines = defaultdict(list)
for w in toc:
    lines[round(w[2], 1)].append(w)
ys = sorted(lines)

# Первая строка длинной записи — там, где слово 'Очень'.
i_first = next(i for i, y in enumerate(ys) if any(w[5] == "Очень" for w in lines[y]))
y_first = ys[i_first]
y_next = ys[i_first + 1]

# Заголовок реально перенёсся: вторая строка — продолжение того же заголовка.
c.check("wrapped",
        any(w[5] in ("следующую", "строку", "документа", "переносится") for w in lines[y_next]),
        f"вторая строка не похожа на продолжение: {[w[5] for w in lines[y_next]]}")

# На ПЕРВОЙ строке переноса нет номера страницы (последнее слово — не цифра у правого края).
first_right = max(lines[y_first], key=lambda w: w[3])
c.check("no_pageno_first_line",
        not (first_right[5].isdigit() and first_right[3] > 540),
        f"номер оказался на первой строке: {first_right[5]!r} x1={first_right[3]:.1f}")

# Номер страницы стоит справа на ПОСЛЕДНЕЙ строке заголовка.
next_right = max(lines[y_next], key=lambda w: w[3])
c.check("pageno_on_last_line",
        next_right[5].isdigit() and next_right[3] > 540,
        f"номер не у правого края последней строки: {next_right[5]!r} x1={next_right[3]:.1f}")

c.done()
