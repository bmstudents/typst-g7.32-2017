"""he3_table_caption_multiline_boundary: многострочная ПОДПИСЬ таблицы на
границе страницы (подпись = table.header).

Инварианты:
1. Подпись реально многострочная (>=3 строк по уникальным yMin).
2. Подпись целиком на одной странице со своей первой строкой тела:
   слово «N»/«Значение» (первая строка тела) на той же странице, что и
   «Таблица», и слова-хвост подписи («сироту»/«наверху»/«предыдущей»).
3. Нет «висячей» строки подписи на другой странице."""
import helpers as h

c = h.Checks("he3_table_caption_multiline_boundary")
pdf = h.compile("he3_table_caption_multiline_boundary.typ")
ws = h.words(pdf)

cap = [w for w in ws if w[5] == "Таблица"]
c.check("caption_present", bool(cap), "нет подписи 'Таблица'")

cap_page = cap[0][0] if cap else None

# Слова подписи на странице подписи (от подписи и ниже, без футера).
cap_words = [w for w in ws
             if cap and w[0] == cap_page and w[2] >= cap[0][2] and w[2] < 700]
uniq_y = sorted({round(w[2], 1) for w in cap_words})
c.check("caption_multiline",
        len(uniq_y) >= 3,
        f"подпись не на 3+ строки: уникальных yMin={len(uniq_y)} ({uniq_y})")

# Хвост подписи и первая строка тела — на той же странице, что и «Таблица».
tail = ("сироту", "наверху", "предыдущей")
stray_tail = [(w[5], w[0]) for w in ws if w[5] in tail and w[0] != cap_page]
c.check("caption_not_split",
        not stray_tail,
        f"часть подписи на другой странице: {stray_tail} (подпись на "
        f"стр.{cap_page})")

head_cells = [w for w in ws if w[5] in ("N", "Значение")]
c.check("first_body_row_with_caption",
        head_cells and all(w[0] == cap_page for w in head_cells),
        f"первая строка тела не на странице подписи: "
        f"{[(w[5], w[0]) for w in head_cells]} (подпись стр.{cap_page})")

c.done()
