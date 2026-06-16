"""he1 #8 — многострочная подпись таблицы: последняя строка не наезжает на тело.

Подпись «Таблица N – ...» переносится на 3+ строки; v(-0.5em) ставится ПОСЛЕ
всей подписи (figure.typ:35), поэтому важна именно ПОСЛЕДНЯЯ строка подписи.
Проверяем зазор: yMin(МЛЦЕЛЛ1/МЛЦЕЛЛ2) − yMax(последней строки подписи) > 0.

ИНВАРИАНТ: подпись заняла >=3 строки; зазор последняя строка подписи → тело
> 0 при фиче. FAIL => наезд многострочной подписи.
"""
import helpers as h

c = h.Checks("he1_multiline_caption")


def measure(typ):
    pdf = h.compile(typ)
    ws = h.words(pdf)
    y_body = min(h.y_of(pdf, "МЛЦЕЛЛ1") or 1e9, h.y_of(pdf, "МЛЦЕЛЛ2") or 1e9)
    if y_body >= 1e9:
        return None
    y_head = h.y_of(pdf, "Раздел") or 0
    cap = [w for w in ws if w[0] == 1 and w[2] > y_head and w[2] < y_body]
    if not cap:
        return None
    rows = sorted(set(round(w[4], 0) for w in cap))
    cap_last = max(w[4] for w in cap)
    return len(rows), y_body - cap_last, cap_last, y_body


m_no = measure("he1_multiline_caption_noflag.typ")
m_fl = measure("he1_multiline_caption_flag.typ")

c.check("measured", m_no is not None and m_fl is not None,
        f"не удалось измерить: noflag={m_no} flag={m_fl}")

if m_fl:
    n_lines, gap_fl, capb, ybody = m_fl
    c.check("multiline", n_lines >= 3,
            f"подпись заняла {n_lines} строк (<3) — тест не проверяет многострочность")
    c.check("flag_no_overlap", gap_fl > 0,
            f"НАЕЗД последней строки многострочной подписи на тело при фиче: "
            f"подпись yMax={capb:.1f}, тело yMin={ybody:.1f}, зазор={gap_fl:.2f} "
            f"(>0). figure.typ:35")

if m_no and m_fl:
    c.check("shrink_about_half_em", 3 < (m_no[1] - m_fl[1]) < 11,
            f"усадка зазора = {m_no[1] - m_fl[1]:.2f}pt; ожидалась ~7pt. "
            f"figure.typ:35")

c.done()
