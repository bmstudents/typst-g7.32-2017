import helpers as h

c = h.Checks("xa_two_figs_boundary")
pdf = h.compile("xa_two_figs_boundary.typ")
ws = h.words(pdf)


def pg(word, nth=1):
    hh = [w for w in ws if w[5] == word]
    return (hh[nth - 1][0], round(hh[nth - 1][2], 1)) if len(hh) >= nth else (None, None)


# Первый рисунок (контроль): тело Н1тело и подпись "Рисунок" (1-е вхождение).
fig1_body_pg, _ = pg("Н1тело")
fig1_cap_pg, fig1_cap_y = pg("Рисунок", 1)

# Второй рисунок (на границе): тело В2тело/Н2тело и подпись (2-е вхождение).
fig2_top_pg, _ = pg("В2тело")
fig2_bot_pg, fig2_bot_y = pg("Н2тело")
fig2_cap_pg, fig2_cap_y = pg("Рисунок", 2)

c.check(
    "оба рисунка и обе подписи найдены",
    None not in (fig1_body_pg, fig1_cap_pg, fig2_bot_pg, fig2_cap_pg),
    f"f1body={fig1_body_pg} f1cap={fig1_cap_pg} f2bot={fig2_bot_pg} f2cap={fig2_cap_pg}",
)

# Первый рисунок: подпись с телом (контроль, что первый не сломан).
c.check(
    "первый рисунок: подпись с телом",
    fig1_body_pg == fig1_cap_pg,
    f"тело1 стр.{fig1_body_pg}, подпись1 стр.{fig1_cap_pg}",
)

# ГЛАВНОЕ: второй рисунок на границе — его подпись "Рисунок 2" должна
# остаться со своим телом.
c.check(
    "второй рисунок: подпись не оторвана от тела",
    fig2_bot_pg == fig2_cap_pg,
    f"тело второго рисунка (Н2тело) на стр.{fig2_bot_pg} (y={fig2_bot_y}), а его "
    f"подпись 'Рисунок 2' на стр.{fig2_cap_pg} (y={fig2_cap_y}) — подпись "
    f"оторвалась на следующую страницу одна, тело осталось внизу предыдущей. "
    f"Тот же баг styles/figure.typ (kind: image): тело и подпись не образуют "
    f"неразрывный блок, поэтому второй рисунок на границе теряет подпись.",
)

c.done()
