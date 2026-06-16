"""he1 #2 — подпись «Таблица N» против тела таблицы (растровый инк).

В отличие от листинга, тело таблицы в figure.typ идёт со stroke:0em (без
рамки), поэтому верхняя граница — это инк ПЕРВОЙ СТРОКИ тела, а не линейка.
Проверяем, что с фичей подпись «Таблица N – ...» и первая строка тела
остаются РАЗНЫМИ полосами инка (зазор > 0) — нет вертикального наезда.

Сравниваем с режимом без фичи: зазор обязан только уменьшиться, но не
обнулиться/стать отрицательным.

ИНВАРИАНТ: с фичей >= 2 полос инка в окне «подпись + первая строка тела»,
зазор между ними > 0. Иначе FAIL (наезд). Файл: styles/figure.typ (v(-0.5em)
после подписи таблицы, строка 35).
"""
import he1_ink as ink
import helpers as h

c = h.Checks("he1_table_caption_ink")
Y_LO, Y_HI = 72.0, 170.0


def bands(typ):
    png, ppi = ink.render_png(typ)
    return ink.ink_bands(png, ppi, y_lo_pt=Y_LO, y_hi_pt=Y_HI), png


b_no, _ = bands("he1_table_caption_ink_noflag.typ")
b_fl, png_fl = bands("he1_table_caption_ink_flag.typ")

ok_no = len(b_no) >= 2
gap_no = (b_no[1][0] - b_no[0][1]) if ok_no else -1
c.check("noflag_caption_body_separate", ok_no and gap_no > 2,
        f"без фичи подпись и тело должны быть разными полосами с зазором>2pt; "
        f"полосы={[(round(a,1),round(b,1)) for a,b in b_no]} зазор={gap_no:.2f}")

ok_fl = len(b_fl) >= 2
gap_fl = (b_fl[1][0] - b_fl[0][1]) if ok_fl else -999
c.check("flag_no_overlap", ok_fl and gap_fl > 0,
        f"НАЕЗД подписи «Таблица» на первую строку тела при фиче: "
        f"полос={len(b_fl)} ({[(round(a,1),round(b,1)) for a,b in b_fl]}), "
        f"зазор={gap_fl:.2f}pt (>0 ожидался). figure.typ:35. PNG: {png_fl}")

# фича должна уменьшать зазор примерно на 0.5em (~7pt при 14pt), а не больше
if ok_no and ok_fl:
    shrink = gap_no - gap_fl
    c.check("shrink_about_half_em", 3 < shrink < 11,
            f"усадка зазора подпись→тело = {shrink:.2f}pt; ожидалась ~7pt "
            f"(0.5em@14pt). Больше => лишний отрицательный v. figure.typ:35")

c.done()
