"""xb_fig_caption_multiline: рисунок с очень длинной подписью (~200 символов).
Подпись переносится на >=3 строки (уникальных yMin у слов подписи >=3), все
строки подписи лежат на той же странице, что и рисунок, и набраны justify
(строки кроме последней дотягиваются до правого поля ~545-552)."""
import helpers as h

c = h.Checks("xb_fig_caption_multiline")
pdf = h.compile("xb_fig_caption_multiline.typ")
ws = h.words(pdf)

# Слова подписи — всё, что между "Рисунок" и концом, на той же странице.
# Берём страницу, где стоит "Рисунок".
sup = [w for w in ws if w[5] == "Рисунок"]
assert sup, "нет супплемента 'Рисунок' в подписи"
cap_page = sup[0][0]

# Подпись: от слова "Рисунок" и ниже по y на этой странице, исключая футер
# (футер — одинокая цифра внизу, y > 700).
caption_words = [w for w in ws
                 if w[0] == cap_page and w[2] >= sup[0][2] and w[2] < 700]
uniq_y = sorted({round(w[2], 1) for w in caption_words})

# 1. Подпись реально многострочная: >=3 уникальных yMin.
c.check("caption_3plus_lines", len(uniq_y) >= 3,
        f"подпись не на 3+ строки: уникальных yMin={len(uniq_y)} ({uniq_y})")

# 2. Все строки подписи на одной странице с рисунком (рисунок=cap_page, т.к.
#    figure image-kind — единый блок: тело и подпись неразрывны). Проверяем,
#    что слова подписи не разбежались по разным страницам.
cap_pages = {w[0] for w in caption_words}
c.check("caption_single_page", cap_pages == {cap_page},
        f"строки подписи на разных страницах: {cap_pages}, ожидали {{{cap_page}}}")

# 3. Justify: каждая строка подписи КРОМЕ последней дотягивается до правого
#    поля (xMax >= 543; правый край текста ≈552, поле справа 15мм).
lines = {}
for w in caption_words:
    lines.setdefault(round(w[2], 1), []).append(w)
ordered = sorted(lines)
non_last = ordered[:-1]
right_edges = {y: max(w[3] for w in lines[y]) for y in non_last}
all_justified = all(e >= 543 for e in right_edges.values())
c.check("caption_justified", len(non_last) >= 2 and all_justified,
        f"строки подписи (кроме последней) не выровнены по правому полю: "
        f"{ {y: round(e,1) for y,e in right_edges.items()} } (ожидали все xMax>=543)")

c.done()
