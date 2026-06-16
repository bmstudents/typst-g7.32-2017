"""he1 #7 — две таблицы подряд при фиче не слипаются.

Между низом тела первой таблицы (ПЕРВНИЗ) и подписью второй («Таблица 2»)
должен быть положительный зазор. С фичей низ первой таблицы получает доп.
v(-0.5em) (figure.typ:48), а подпись второй — v(-0.5em) (figure.typ:35);
оба не должны схлопнуть стык в наезд.

ИНВАРИАНТ: yMin(подпись табл.2) − yMax(ПЕРВНИЗ) > 0 при фиче. Обе подписи
присутствуют (счётчик инкрементится).
"""
import helpers as h

c = h.Checks("he1_two_tables")


def gap(typ):
    pdf = h.compile(typ)
    ws = h.words(pdf)
    t = h.text(pdf)
    both = ("Таблица 1" in t) and ("Таблица 2" in t)
    caps = sorted([w for w in ws if w[5] == "Таблица"], key=lambda w: w[2])
    cap2 = caps[1][2] if len(caps) >= 2 else None
    bot1 = [w for w in ws if w[5] == "ПЕРВНИЗ"]
    bot1y = bot1[0][4] if bot1 else None
    g = (cap2 - bot1y) if (cap2 is not None and bot1y is not None) else None
    return both, g, bot1y, cap2


both_no, g_no, _, _ = gap("he1_two_tables_noflag.typ")
both_fl, g_fl, b1, c2 = gap("he1_two_tables_flag.typ")

c.check("both_captions_flag", both_fl,
        "при фиче нет обеих подписей «Таблица 1»/«Таблица 2»")

c.check("noflag_positive", g_no is not None and g_no > 0,
        f"без фичи зазор между таблицами={g_no}")

c.check("flag_no_overlap", g_fl is not None and g_fl > 0,
        f"таблицы СЛИПЛИСЬ при фиче: низ табл.1 yMax={b1}, подпись табл.2 "
        f"yMin={c2}, зазор={g_fl} (>0). figure.typ:35/48")

if g_no is not None and g_fl is not None:
    c.check("shrink_bounded", (g_no - g_fl) < 18,
            f"усадка стыка между таблицами = {g_no - g_fl:.2f}pt — слишком "
            f"большая, накопление отрицательных v. figure.typ:35/47/48")

c.done()
