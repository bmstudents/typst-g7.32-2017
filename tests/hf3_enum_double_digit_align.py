"""hf3_enum_double_digit_align: ИНВАРИАНТ — текст пунктов нумерованного перечисления
должен начинаться на ОДНОЙ вертикали независимо от ширины маркера (1) … 12)).

ГОСТ 7.32 требует, чтобы текст перечисления был выровнен в единую колонку
(висячий отступ). Рукописная реализация в gost732-2017/styles/list.typ:

    for phase in it.children [
        #h(config.page.parIndent) #i) #phase.body \\
    ]

ставит маркер «N)» фиксированной шириной шрифта и затем body через обычный
пробел. У двузначных номеров маркер шире, поэтому текст уезжает вправо —
колонка текста НЕ выровнена. Это скрытый баг выравнивания.
"""
import helpers as h

c = h.Checks("hf3_enum_double_digit_align")
pdf = h.compile("hf3_enum_double_digit_align.typ")
W = h.words(pdf)

# Маркеры должны идти подряд 1)…12).
markers = {}
for w in W:
    m = w[5]
    if m.endswith(")") and m[:-1].isdigit():
        markers[int(m[:-1])] = w

c.check("all_12_markers", all(n in markers for n in range(1, 13)),
        f"не все маркеры найдены: {sorted(markers)}")

# Первое слово ТЕКСТА (не маркер) каждого пункта — ближайшее справа на той же строке.
def item_text_x(n):
    mk = markers[n]
    y = mk[2]
    same_line = [w for w in W if abs(w[2] - y) < 2 and w[1] > mk[3] and not (w[5].endswith(")") and w[5][:-1].isdigit())]
    if not same_line:
        return None
    return min(same_line, key=lambda w: w[1])[1]

single = item_text_x(1)   # текст после однозначного «1)»
ten = item_text_x(10)     # текст после двузначного «10)»
twelve = item_text_x(12)  # текст после двузначного «12)»

c.check("have_text_x", None not in (single, ten, twelve),
        f"не нашли x текста: 1)->{single} 10)->{ten} 12)->{twelve}")

# ГЛАВНЫЙ ИНВАРИАНТ: текст пунктов выровнен в колонку (допуск 1pt).
if None not in (single, ten, twelve):
    dmax = max(abs(ten - single), abs(twelve - single))
    c.check("text_column_aligned", dmax < 1.0,
            f"БАГ ВЫРАВНИВАНИЯ (list.typ, show enum): текст пунктов НЕ в одной колонке. "
            f"x после '1)'={single:.2f}, после '10)'={ten:.2f}, после '12)'={twelve:.2f}; "
            f"расхождение {dmax:.2f}pt. Рукописное '#i)#phase.body' не делает висячий отступ — "
            f"двузначные номера сдвигают текст вправо.")

# Маркеры при этом ВСЕ начинаются на одной вертикали (это рукописная реализация делает).
mxs = [markers[n][1] for n in range(1, 13)]
c.check("markers_left_aligned", max(mxs) - min(mxs) < 0.5,
        f"маркеры не на одной вертикали: {[round(x,1) for x in mxs]}")

c.done()
