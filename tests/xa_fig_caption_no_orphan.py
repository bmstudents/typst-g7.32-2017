import helpers as h

c = h.Checks("xa_fig_caption_no_orphan")
pdf = h.compile("xa_fig_caption_no_orphan.typ")
ws = h.words(pdf)


def pg(word, nth=1):
    hh = [w for w in ws if w[5] == word]
    return (hh[nth - 1][0], round(hh[nth - 1][2], 1)) if len(hh) >= nth else (None, None)


body_top_pg, body_top_y = pg("ВЕРХрис")
body_bot_pg, body_bot_y = pg("НИЗрис")
cap_pg, cap_y = pg("Рисунок")

# Тело и подпись вообще должны присутствовать.
c.check(
    "элементы найдены",
    body_top_pg is not None and body_bot_pg is not None and cap_pg is not None,
    f"top={body_top_pg} bot={body_bot_pg} cap={cap_pg}",
)

# ГЛАВНОЕ: тело рисунка и подпись "Рисунок N" на ОДНОЙ странице.
# Тело — это блок box(8cm), его низ задаёт страницу тела.
c.check(
    "подпись не оторвана от тела (одна страница)",
    body_bot_pg == cap_pg,
    f"тело (НИЗрис) на стр.{body_bot_pg} y={body_bot_y}, "
    f"а подпись 'Рисунок' на стр.{cap_pg} y={cap_y} — "
    f"подпись оторвалась на следующую страницу (orphan). "
    f"Виноват styles/figure.typ: show figure.where(kind: image) выводит "
    f"`it.body` + v + `it.caption` отдельными блоками без block(breakable:false), "
    f"поэтому подпись может уехать на новую страницу одна.",
)

# Усиление: верх и низ тела рисунка тоже должны быть на одной странице
# (само тело не должно разрываться).
c.check(
    "тело рисунка не разорвано",
    body_top_pg == body_bot_pg,
    f"верх тела стр.{body_top_pg}, низ тела стр.{body_bot_pg}",
)

c.done()
