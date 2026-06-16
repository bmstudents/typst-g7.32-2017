import helpers as h

c = h.Checks("xa_fig_caption_not_alone")
pdf = h.compile("xa_fig_caption_not_alone.typ")
ws = h.words(pdf)


def pg(word, nth=1):
    hh = [w for w in ws if w[5] == word]
    return (hh[nth - 1][0], round(hh[nth - 1][2], 1)) if len(hh) >= nth else (None, None)


body_top_pg, body_top_y = pg("ВЕРХрис")
body_bot_pg, body_bot_y = pg("НИЗрис")
cap_pg, cap_y = pg("Рисунок")

c.check(
    "элементы найдены",
    body_top_pg is not None and cap_pg is not None,
    f"top={body_top_pg} cap={cap_pg}",
)

# На странице, где оказалась подпись "Рисунок", должно присутствовать
# и тело рисунка (хотя бы его низ). Иначе подпись стоит одна.
cap_page_words = [w[5] for w in ws if w[0] == cap_pg]
body_on_cap_page = (body_top_pg == cap_pg) or (body_bot_pg == cap_pg)

c.check(
    "подпись не одна на своей странице (тело рядом)",
    body_on_cap_page,
    f"подпись 'Рисунок' на стр.{cap_pg} (y={cap_y}), но тело рисунка на "
    f"стр.{body_top_pg}..{body_bot_pg}. Подпись стоит одна — содержимое стр.{cap_pg} "
    f"начинается с {cap_page_words[:5]}. Рисунок и подпись должны были перейти "
    f"на новую страницу ВМЕСТЕ. Баг в styles/figure.typ (kind: image): тело и "
    f"подпись не сгруппированы в неразрывный блок.",
)

# Дополнительно: тело рисунка целиком на одной странице.
c.check(
    "тело рисунка не разорвано между страницами",
    body_top_pg == body_bot_pg,
    f"верх тела стр.{body_top_pg}, низ тела стр.{body_bot_pg}",
)

c.done()
