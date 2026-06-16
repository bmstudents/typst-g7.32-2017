"""h1 ТАБЛИЦЫ #1 — ЛЕВЫЙ КРАЙ ТЕЛА == ЛЕВЫЙ КРАЙ ПОДПИСИ.

ГОСТ 7.32: таблица и её подпись «Таблица N – …» начинаются от одной левой
границы (левое поле, x≈85). Узкое тело таблицы НЕ должно центрироваться
относительно полосы набора — его левая граница обязана стоять под началом
слова «Таблица».

Измеримый инвариант: левая ЛИНИЯ таблицы под началом слова «Таблица».
pdftotext видит только ТЕКСТ ячейки, который отстоит от линии на inset
ячейки (config.figure.inset = 10pt), поэтому текст ≈ подпись + 10pt, а сама
линия ≈ подпись.

ИСПРАВЛЕНО (styles/figure.typ): тело таблицы прижато влево
(h(-1.25cm)+align(left)) под подпись; раньше центрировалось (тело x0≈300).
"""
import helpers as h

c = h.Checks("h1_table_left_aligned")
pdf = h.compile("h1_table_left_aligned.typ")
ws = [w for w in h.words(pdf) if w[0] == 1]

cap = [w for w in ws if w[5] == "Таблица"]
c.check("caption_present", len(cap) == 1,
        f"подпись «Таблица» не найдена: {[w[5] for w in ws]}")

# Ячейки тела — буквы А и Б; берём их строго ниже подписи.
cap_y = cap[0][2] if cap else 0
body = [w for w in ws if w[5] in ("А", "Б") and w[2] > cap_y + 5]
c.check("body_cells_present", {w[5] for w in body} == {"А", "Б"},
        f"ячейки тела А/Б не найдены ниже подписи: {[(w[5], round(w[1])) for w in body]}")

if cap and body:
    cap_x0 = cap[0][1]
    body_x0 = min(w[1] for w in body)
    inset = 10  # config.figure.inset — отступ текста от линии ячейки
    line_x0 = body_x0 - inset  # реконструкция левой линии таблицы
    # ГЛАВНЫЙ инвариант ГОСТ: левая ЛИНИЯ таблицы под началом подписи (±4pt).
    c.check(
        "body_left_line_under_caption",
        abs(line_x0 - cap_x0) <= 4,
        f"левая линия таблицы НЕ под подписью: подпись x0={cap_x0:.2f}, "
        f"текст ячейки x0={body_x0:.2f}, линия≈{line_x0:.2f} (ожид≈{cap_x0:.2f}). "
        f"Тело должно быть прижато влево (figure.typ: h(-1.25cm)+align(left)).",
    )
    # Тело не центрировано (не уехало к середине полосы).
    c.check(
        "body_not_centered",
        body_x0 < cap_x0 + 30,
        f"тело смещено вправо на {body_x0 - cap_x0:+.2f}pt от подписи (тело x0={body_x0:.2f})",
    )

c.done()
