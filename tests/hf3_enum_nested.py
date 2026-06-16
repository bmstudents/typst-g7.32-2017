"""hf3_enum_nested: ИНВАРИАНТ — вложенное перечисление должно (а) быть на
ОТДЕЛЬНЫХ строках от родителя и (б) иметь больший левый отступ (второй уровень).

Рукописный show enum (gost732-2017/styles/list.typ) перебирает it.children и
печатает «#h(parIndent) #i) #phase.body \\». Если phase.body САМ содержит
вложенный enum, он рендерится ВНУТРИ body inline — show-правило применяется
рекурсивно, но без увеличения отступа и без переноса перед вложенным списком.
Ожидаемый баг: вложенные пункты прилипают к строке родителя и/или не имеют
второго уровня отступа, нумерация второго уровня сливается с первым.
"""
import helpers as h

c = h.Checks("hf3_enum_nested")
pdf = h.compile("hf3_enum_nested.typ")
W = [w for w in h.words(pdf) if w[0] == 1]


def word_y(substr, nth=1):
    hits = [w for w in W if w[5] == substr]
    return hits[nth - 1][2] if len(hits) >= nth else None


def first_x_on_line_of(substr):
    hits = [w for w in W if w[5] == substr]
    if not hits:
        return None
    y = hits[0][2]
    return min((w[1] for w in W if abs(w[2] - y) < 2), default=None)


y_parent1 = word_y("первый")
y_childA = word_y("вложенный", 1)   # «вложенный А»
y_childB = word_y("вложенный", 2)   # «вложенный Б»

c.check("found_items", None not in (y_parent1, y_childA, y_childB),
        f"не нашли пункты: первый={y_parent1} childA={y_childA} childB={y_childB}")

if None not in (y_parent1, y_childA):
    # ИНВАРИАНТ 1: вложенный пункт «А» НЕ на одной строке с родителем «первый».
    c.check("nested_on_own_line", abs(y_childA - y_parent1) > 3.0,
            f"БАГ ВЛОЖЕННОСТИ (list.typ, show enum): вложенный пункт 'вложенный А' "
            f"(y={y_childA:.2f}) на ТОЙ ЖЕ строке, что родитель 'первый' (y={y_parent1:.2f}). "
            f"phase.body с вложенным enum рендерится inline без переноса.")

# ИНВАРИАНТ 2: вложенный уровень имеет БОЛЬШИЙ левый отступ, чем верхний.
x_top = first_x_on_line_of("первый")          # строка верхнего уровня (маркер 1))
x_nested = first_x_on_line_of("вложенный")     # строка вложенного уровня
if None not in (x_top, x_nested):
    c.check("nested_indent_deeper", x_nested > x_top + 5.0,
            f"БАГ ОТСТУПА ВЛОЖЕННОСТИ: второй уровень x={x_nested:.2f} не глубже "
            f"первого x={x_top:.2f} — отступ второго уровня не применён.")

c.done()
