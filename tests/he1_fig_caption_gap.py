"""he1 #9 — рисунок при фиче: подпись «Рисунок N» не наезжает на тело снизу,
а текст после рисунка не наезжает на подпись.

У рисунка подпись стоит СНИЗУ; фича вставляет v(-0.5em) МЕЖДУ телом и
подписью (figure.typ:101). Тело — rect 8×4см с метками ВЕРХТЕЛА/НИЗТЕЛА.

ИНВАРИАНТЫ при фиче:
  yMin(«Рисунок») − yMax(НИЗТЕЛА) > 0   — подпись не наезжает на низ тела;
  yMin(ПОСЛЕРИС)  − yMax(«Рисунок») > 0 — текст после не наезжает на подпись.
Сравниваем с режимом без фичи (зазор тело→подпись только уменьшается).
"""
import helpers as h

c = h.Checks("he1_fig_caption_gap")


def measure(typ):
    pdf = h.compile(typ)
    ws = h.words(pdf)

    def one(word):
        hits = [w for w in ws if w[5] == word]
        return hits[0] if hits else None

    bot = one("НИЗТЕЛА")
    cap = one("Рисунок")
    after = one("ПОСЛЕРИС")
    if not (bot and cap):
        return None
    body_cap = cap[2] - bot[4]
    cap_text = (after[2] - cap[4]) if after else None
    return body_cap, cap_text, bot[4], cap[2], cap[4], (after[2] if after else None)


m_no = measure("he1_fig_caption_gap_noflag.typ")
m_fl = measure("he1_fig_caption_gap_flag.typ")

c.check("measured", m_no is not None and m_fl is not None,
        f"не измерил метки рисунка: noflag={m_no} flag={m_fl}")

if m_fl:
    body_cap, cap_text, ybot, ycap, ycapb, yaft = m_fl
    c.check("flag_body_to_caption_gap", body_cap > 0,
            f"НАЕЗД подписи «Рисунок» на низ тела при фиче: низ тела yMax={ybot:.1f}, "
            f"подпись yMin={ycap:.1f}, зазор={body_cap:.2f} (>0). figure.typ:101")
    if cap_text is not None:
        c.check("flag_caption_to_text_gap", cap_text > 0,
                f"НАЕЗД текста после рисунка на подпись при фиче: подпись yMax={ycapb:.1f}, "
                f"текст yMin={yaft:.1f}, зазор={cap_text:.2f} (>0). figure.typ")

if m_no and m_fl:
    c.check("shrink_about_half_em", 3 < (m_no[0] - m_fl[0]) < 11,
            f"усадка зазора тело→подпись = {m_no[0] - m_fl[0]:.2f}pt; "
            f"ожидалась ~7pt (0.5em@14pt). figure.typ:101")

c.done()
