"""he1 #6 — таблица + следующий текст: текст не наезжает на низ таблицы.

С фичей низ таблицы получает добавочный v(-0.5em) (figure.typ:48 поверх
figure.typ:47). Проверяем зазор низ тела (НИЗЯЧ) → текст (ПОСЛЕТАБ).

ИНВАРИАНТ: yMin(ПОСЛЕТАБ) − yMax(НИЗЯЧ) > 0 при фиче. Усадка относительно
noflag равна ровно одному дополнительному 0.5em (~7pt), не больше.
"""
import helpers as h

c = h.Checks("he1_table_then_text")


def gap(typ):
    pdf = h.compile(typ)
    ws = h.words(pdf)
    bot = [w for w in ws if w[5] == "НИЗЯЧ"]
    txt = [w for w in ws if w[5] == "ПОСЛЕТАБ"]
    if not bot or not txt:
        return None, None, None
    return txt[0][2] - bot[0][4], bot[0][4], txt[0][2]


g_no, _, _ = gap("he1_table_then_text_noflag.typ")
g_fl, ybot, ytxt = gap("he1_table_then_text_flag.typ")

c.check("found", g_no is not None and g_fl is not None,
        f"маркеры не найдены: noflag={g_no} flag={g_fl}")

c.check("noflag_positive", g_no is not None and g_no > 0,
        f"без фичи зазор таблица→текст={g_no}")

c.check("flag_no_overlap", g_fl is not None and g_fl > 0,
        f"НАЕЗД текста на низ таблицы при фиче: низ тела yMax={ybot}, "
        f"текст yMin={ytxt}, зазор={g_fl} (>0). figure.typ:47-48")

if g_no is not None and g_fl is not None:
    c.check("shrink_about_half_em", 3 < (g_no - g_fl) < 11,
            f"усадка нижнего зазора = {g_no - g_fl:.2f}pt; ожидалась ~7pt "
            f"(один доп. -0.5em). Больше => лишние отрицательные v. "
            f"figure.typ:47-48")

c.done()
