"""h4_long_heading_number_first_line: очень длинный заголовок раздела
переносится на несколько строк, а его номер «1» стоит в начале ПЕРВОЙ строки.

«В начале первой строки» = на первой (самой верхней) строке заголовка номер
«1» имеет минимальный x среди слов этой строки, и стоит левее первого слова
текста заголовка («Исследование»).

Жёсткость:
  1) Заголовок реально многострочный: >=2 уникальных yMin у слов заголовка.
  2) Номер «1» — на верхней строке заголовка (его yMin == минимальному yMin
     слов заголовка) и его x0 < x0 слова «Исследование».
  3) Координату «1» берём именно из строки заголовка (y у верха страницы),
     отсекая омоним «1» в нижнем колонтитуле (номер страницы, большой y).
"""
import helpers as h

c = h.Checks("h4_long_heading_number_first_line")
pdf = h.compile("h4_long_heading_number_first_line.typ")
ws = [w for w in h.words(pdf) if w[0] == 1]

iss = [w for w in ws if w[5] == "Исследование"]
y_body = h.y_of(pdf, "Текст", page=1)  # начало тела раздела
assert iss, "нет первого слова заголовка 'Исследование'"
assert y_body is not None, "нет тела раздела (слово 'Текст')"

# Слова заголовка: от верха страницы до начала тела раздела (по yMin).
head_words = [w for w in ws if w[2] < y_body]
uniq_y = sorted({round(w[2], 1) for w in head_words})
first_line_y = min(uniq_y)

# Номер заголовка: «1» на первой строке заголовка (не колонтитул).
num_on_first = [w for w in head_words if w[5] == "1" and round(w[2], 1) == first_line_y]

c.check("heading_multiline",
        len(uniq_y) >= 2,
        f"заголовок не перенёсся: уникальных yMin={len(uniq_y)} ({uniq_y})")

c.check("number_on_first_line",
        len(num_on_first) == 1,
        f"'1' не найден на первой строке заголовка (y={first_line_y}); "
        f"строки заголовка: {uniq_y}")

if num_on_first:
    n = num_on_first[0]
    # Номер левее первого слова текста и является минимальным x на строке.
    line_min_x = min(w[1] for w in head_words if round(w[2], 1) == first_line_y)
    c.check("number_leftmost_before_text",
            n[1] < iss[0][1] and abs(n[1] - line_min_x) < 0.5,
            f"'1' не в начале строки: x0(1)={n[1]:.1f}, "
            f"x0(Исследование)={iss[0][1]:.1f}, min_x строки={line_min_x:.1f}")
else:
    c.check("number_leftmost_before_text", False, "нет '1' на первой строке")

c.done()
