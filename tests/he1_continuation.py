"""he1 #5 — «Продолжение таблицы N» на стр.2 не наезжает на тело.

Таблица перетекает на 2-ю страницу; в шапке стр.2 печатается
«Продолжение таблицы N», за которым с фичей идёт v(-0.5em) (figure.typ:38).
Проверяем, что первая строка тела на стр.2 (стрNN) не наезжает на заголовок
продолжения.

ИНВАРИАНТ: на каждой странице >=2, где есть «Продолжение», зазор
yMin(первой строки тела) − yMax(«Продолжение»/«таблицы»/номер) > 0.
Сравниваем с режимом без фичи.
"""
import helpers as h

c = h.Checks("he1_continuation")


def cont_gaps(typ):
    pdf = h.compile(typ)
    ws = h.words(pdf)
    npages = h.page_count(pdf)
    res = []
    for pg in range(2, npages + 1):
        pw = [w for w in ws if w[0] == pg]
        cont = [w for w in pw if w[5] in ("Продолжение", "таблицы")]
        if not cont:
            continue
        cont_ymax = max(w[4] for w in cont)
        body = [w for w in pw if w[5].startswith("стр")]
        if not body:
            continue
        first_body = min(w[2] for w in body)
        res.append((pg, first_body - cont_ymax, cont_ymax, first_body))
    return npages, res


np_no, g_no = cont_gaps("he1_continuation_noflag.typ")
np_fl, g_fl = cont_gaps("he1_continuation_flag.typ")

c.check("breaks_to_page2", np_fl >= 2 and len(g_fl) >= 1,
        f"таблица не перетекла на стр.2 или нет «Продолжение»: "
        f"страниц={np_fl}, найдено продолжений={len(g_fl)}")

c.check("noflag_positive", all(g > 0 for _, g, _, _ in g_no) and len(g_no) >= 1,
        f"без фичи зазоры продолжение→тело: {[(p, round(g,2)) for p,g,_,_ in g_no]}")

bad = [(p, round(g, 2), round(cy, 2), round(fb, 2))
       for p, g, cy, fb in g_fl if g <= 0]
c.check("flag_no_overlap", len(bad) == 0,
        f"НАЕЗД «Продолжение таблицы» на тело при фиче на стр: {bad} "
        f"(зазор<=0). figure.typ:38. Все зазоры: "
        f"{[(p, round(g,2)) for p,g,_,_ in g_fl]}")

c.done()
