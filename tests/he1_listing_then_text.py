"""he1 #3 — листинг + следующий текст: текст не наезжает на низ листинга.

С фичей низ листинга получает v(-0.5em) (figure.typ:84/85). Проверяем, что
первая строка текста ПОСЛЕ листинга (ХВОСТТЕКСТ) не наезжает на последнюю
строку тела листинга (КОДCТРОКАB).

ИНВАРИАНТ: yMin(ХВОСТТЕКСТ) − yMax(КОДCТРОКАB) > 0 при фиче. Сравниваем с
режимом без фичи (зазор только уменьшается). FAIL => наезд (figure.typ:84-85).
"""
import helpers as h

c = h.Checks("he1_listing_then_text")


def gap(typ):
    pdf = h.compile(typ)
    body_bottom = h.y_of(pdf, "КОДCТРОКАB")  # yMin; нужен yMax
    ws = h.words(pdf)
    bb = [w for w in ws if w[5] == "КОДCТРОКАB"]
    txt = [w for w in ws if w[5] == "ХВОСТТЕКСТ"]
    if not bb or not txt:
        return None, None, None
    return txt[0][2] - bb[0][4], bb[0][4], txt[0][2]


g_no, _, _ = gap("he1_listing_then_text_noflag.typ")
g_fl, ybot, ytxt = gap("he1_listing_then_text_flag.typ")

c.check("markers_present", g_no is not None and g_fl is not None,
        f"не нашёл маркеры тела/текста: noflag={g_no} flag={g_fl}")

c.check("noflag_positive", g_no is not None and g_no > 0,
        f"без фичи зазор листинг→текст={g_no} (должен быть >0)")

c.check("flag_no_overlap", g_fl is not None and g_fl > 0,
        f"НАЕЗД текста на низ листинга при фиче: низ тела yMax={ybot}, "
        f"текст yMin={ytxt}, зазор={g_fl} (>0). figure.typ:84-85")

if g_no is not None and g_fl is not None:
    c.check("shrink_bounded", (g_no - g_fl) < 11,
            f"усадка нижнего зазора = {g_no - g_fl:.2f}pt (> ~7pt ожидаемых): "
            f"лишний отрицательный v. figure.typ:84-85")

c.done()
