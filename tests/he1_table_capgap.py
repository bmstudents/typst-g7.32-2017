"""he1 #4 — подпись «Таблица N» не наезжает на первую строку тела (bbox).

Проверка по словам: yMin(ТЕЛОВЕРХ) − yMax(последнего слова подписи) > 0.
С фичей зазор подпись→тело уменьшается на ~0.5em (figure.typ:35); обязан
остаться положительным.

ИНВАРИАНТ: gap_flag > 0; и усадка относительно noflag в разумных пределах.
"""
import helpers as h

c = h.Checks("he1_table_capgap")


def gap(typ):
    pdf = h.compile(typ)
    ws = h.words(pdf)
    body = [w for w in ws if w[5] == "ТЕЛОВЕРХ"]
    if not body:
        return None, None, None
    y_body = body[0][2]
    y_head = h.y_of(pdf, "Раздел") or 0
    # слова подписи: между заголовком и телом, на стр.1
    cap = [w for w in ws if w[0] == 1 and w[2] > y_head and w[2] < y_body]
    if not cap:
        return None, None, None
    cap_last = max(w[4] for w in cap)
    return y_body - cap_last, cap_last, y_body


g_no, _, _ = gap("he1_table_capgap_noflag.typ")
g_fl, capb, ybody = gap("he1_table_capgap_flag.typ")

c.check("found", g_no is not None and g_fl is not None,
        f"не нашёл подпись/тело: noflag={g_no} flag={g_fl}")

c.check("noflag_positive", g_no is not None and g_no > 0,
        f"без фичи зазор подпись→тело={g_no}")

c.check("flag_no_overlap", g_fl is not None and g_fl > 0,
        f"НАЕЗД подписи «Таблица» на тело при фиче: подпись yMax={capb}, "
        f"тело yMin={ybody}, зазор={g_fl} (>0). figure.typ:35")

if g_no is not None and g_fl is not None:
    c.check("shrink_about_half_em", 3 < (g_no - g_fl) < 11,
            f"усадка = {g_no - g_fl:.2f}pt, ожидалась ~7pt. figure.typ:35")

c.done()
