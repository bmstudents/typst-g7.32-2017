"""hf3_list_multiline_hanging: то же, что hf3_enum_multiline_hanging, но для
МАРКИРОВАННОГО списка (show list). Перенесённые строки должны иметь висячий
отступ, а не уезжать к левому полю.

Рукописный show list:
    h(-config.page.parIndent)
    for phase ... [ #h(parIndent) -- #phase.body \\ ]
Та же конструкция «отрицательный отступ абзаца + ручной перенос» — вторая
строка пункта теряет отступ.
"""
import helpers as h

LEFT_MARGIN = 30 * 2.83464567
PAR_INDENT = 1.25 * 28.3464567
MARKER_X = LEFT_MARGIN + PAR_INDENT  # ~120.47

DASH = "–"

c = h.Checks("hf3_list_multiline_hanging")
pdf = h.compile("hf3_list_multiline_hanging.typ")
W = [w for w in h.words(pdf) if w[0] == 1]

dashes = [w for w in W if w[5] == DASH]
c.check("two_markers", len(dashes) == 2, f"ожидали 2 тире-маркера, нашли {len(dashes)}")

mk = dashes[0]
mk_y = mk[2]
first_line = [w for w in W if abs(w[2] - mk_y) < 2 and w[1] > mk[3]]
text_x = min(first_line, key=lambda w: w[1])[1] if first_line else None

# Перенесённые строки длинного пункта — между первым и вторым тире.
y_limit = dashes[1][2] - 2 if len(dashes) > 1 else 1e9
ys = sorted({round(w[2], 1) for w in W
             if w[2] > mk_y + 2 and w[2] < y_limit and w[5] != DASH})

c.check("wrapped_to_multiple_lines", len(ys) >= 1,
        f"пункт не перенёсся на 2+ строки (строк: {len(ys)})")

def line_start_x(y):
    return min((w[1] for w in W if abs(w[2] - y) < 2), default=None)

wrapped_xs = [line_start_x(y) for y in ys]
min_wrapped = min((x for x in wrapped_xs if x is not None), default=None)

c.check("found_wrapped", min_wrapped is not None, "нет перенесённых строк")

if min_wrapped is not None:
    c.check("wrap_not_at_left_margin", min_wrapped > MARKER_X - 1.0,
            f"БАГ ВИСЯЧЕГО ОТСТУПА (list.typ, show list): перенос пункта на x={min_wrapped:.2f} "
            f"левее маркера (x≈{MARKER_X:.2f}); строка уехала к полю ({LEFT_MARGIN:.2f}).")
    if text_x is not None:
        c.check("wrap_under_item_text", abs(min_wrapped - text_x) < 2.0,
                f"перенос x={min_wrapped:.2f} не под текстом пункта x={text_x:.2f}")

c.done()
