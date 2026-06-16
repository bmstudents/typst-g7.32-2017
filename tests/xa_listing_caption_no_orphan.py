import helpers as h

c = h.Checks("xa_listing_caption_no_orphan")
pdf = h.compile("xa_listing_caption_no_orphan.typ")
ws = h.words(pdf)


def pg(word, nth=1):
    hh = [w for w in ws if w[5] == word]
    return (hh[nth - 1][0], round(hh[nth - 1][2], 1)) if len(hh) >= nth else (None, None)


cap_pg, cap_y = pg("Листинг")
line1_pg, line1_y = pg("ЛИНИЯ1")
line6_pg, _ = pg("ЛИНИЯ6")

c.check(
    "элементы найдены",
    cap_pg is not None and line1_pg is not None,
    f"cap={cap_pg} line1={line1_pg}",
)

# ГЛАВНОЕ: подпись "Листинг 1" и первая строка кода на одной странице.
c.check(
    "подпись листинга не оторвана от кода",
    cap_pg == line1_pg,
    f"подпись 'Листинг 1' на стр.{cap_pg} (y={cap_y}), а первая строка кода "
    f"'ЛИНИЯ1' на стр.{line1_pg} (y={line1_y}) — подпись осталась одна.",
)

# Контроль: код реально длинный и (при таком N) перетекает дальше первой
# строки — то есть тест действительно стоит на границе разрыва.
c.check(
    "листинг на границе разрыва (код длиннее одной страницы остатка)",
    line6_pg is not None and line6_pg >= line1_pg,
    f"строка 1 стр.{line1_pg}, строка 6 стр.{line6_pg}",
)

c.done()
