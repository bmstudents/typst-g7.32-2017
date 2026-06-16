"""hf3_enum_multiline_hanging: ИНВАРИАНТ — перенесённые (вторая+) строки пункта
перечисления должны иметь ВИСЯЧИЙ отступ: начинаться под началом ТЕКСТА пункта
(или хотя бы не левее маркера), а НЕ уезжать к левому полю страницы.

Рукописный show enum (gost732-2017/styles/list.typ) делает:
    h(-config.page.parIndent)
    for phase ... [ #h(parIndent) #i) #phase.body \\ ]
То есть весь пункт — это один абзац с ведущим h(-parIndent). Когда body
переносится, вторая строка наследует отрицательный отступ абзаца и встаёт
на ЛЕВОЕ ПОЛЕ (левее маркера) — висячего отступа нет. Это скрытый баг.
"""
import helpers as h

LEFT_MARGIN = 30 * 2.83464567        # 30mm -> ~85.04 pt
PAR_INDENT = 1.25 * 28.3464567       # 1.25cm -> ~35.43 pt
MARKER_X = LEFT_MARGIN + PAR_INDENT  # ~120.47 pt

c = h.Checks("hf3_enum_multiline_hanging")
pdf = h.compile("hf3_enum_multiline_hanging.typ")
W = [w for w in h.words(pdf) if w[0] == 1]

# Маркер «1)» первого (длинного) пункта.
mk = next(w for w in W if w[5] == "1)")
mk_y = mk[2]
# x начала текста на ПЕРВОЙ строке (первое слово справа от маркера на его строке).
first_line = [w for w in W if abs(w[2] - mk_y) < 2 and w[1] > mk[3]]
text_x = min(first_line, key=lambda w: w[1])[1]

# Строки длинного пункта = группы слов по y, ниже маркера, до короткого пункта «2)».
mk2 = next((w for w in W if w[5] == "2)"), None)
y_limit = mk2[2] - 2 if mk2 else 1e9
ys = sorted({round(w[2], 1) for w in W
             if w[2] > mk_y + 2 and w[2] < y_limit
             and not (w[5].endswith(")") and w[5][:-1].isdigit())})

c.check("wrapped_to_multiple_lines", len(ys) >= 1,
        f"пункт не перенёсся на 2+ строки (строк ниже маркера: {len(ys)})")

# x начала каждой перенесённой строки.
def line_start_x(y):
    return min((w[1] for w in W if abs(w[2] - y) < 2), default=None)

wrapped_xs = [line_start_x(y) for y in ys]
min_wrapped = min(x for x in wrapped_xs if x is not None) if wrapped_xs else None

c.check("found_wrapped", min_wrapped is not None, "не нашли перенесённые строки")

if min_wrapped is not None:
    # ИНВАРИАНТ 1 (мягкий): перенос НЕ должен уезжать к левому полю страницы.
    c.check("wrap_not_at_left_margin", min_wrapped > MARKER_X - 1.0,
            f"БАГ ВИСЯЧЕГО ОТСТУПА (list.typ, show enum): перенесённая строка пункта "
            f"начинается на x={min_wrapped:.2f}, что ЛЕВЕЕ маркера (x≈{MARKER_X:.2f}) — "
            f"вторая строка уехала к левому полю ({LEFT_MARGIN:.2f}). h(-parIndent) у абзаца "
            f"тянет перенос к полю вместо висячего отступа.")

    # ИНВАРИАНТ 2 (строгий ГОСТ): перенос должен быть под началом ТЕКСТА пункта.
    c.check("wrap_under_item_text", abs(min_wrapped - text_x) < 2.0,
            f"перенесённая строка x={min_wrapped:.2f} не выровнена под текст пункта "
            f"x={text_x:.2f} (нет висячего отступа по ГОСТ)")

c.done()
