"""xb_heading_multiline_text: длинный заголовок раздела в ТЕКСТЕ (не оглавление)
переносится на несколько строк. Номер «1» стоит в начале первой строки
заголовка, текст заголовка занимает >=2 строки (уникальных yMin >=2), и весь
заголовок (все строки) лежит на одной странице вместе с телом раздела."""
import helpers as h

c = h.Checks("xb_heading_multiline_text")
pdf = h.compile("xb_heading_multiline_text.typ")
ws = h.words(pdf)

# Номер заголовка "1" — самое верхнее слово страницы.
top = h.first_word(pdf, 1)
assert top is not None, "пустая страница"
num_y, num_word = top

# Первое слово текста заголовка.
first_body = [w for w in ws if w[5] == "Исследование"]
assert first_body, "нет первого слова заголовка 'Исследование'"
head_page = first_body[0][0]

# Слова заголовка: от строки номера до начала тела раздела ("Текст").
y_body = h.y_of(pdf, "Текст", page=head_page)
assert y_body is not None, "нет тела раздела (слово 'Текст')"
head_words = [w for w in ws
              if w[0] == head_page and num_y - 1 <= w[2] < y_body and w[2] < 700]
uniq_y = sorted({round(w[2], 1) for w in head_words})

# 1. Номер "1" в начале первой строки заголовка (самое верхнее, левее текста).
num_hit = [w for w in head_words if w[5] == "1"]
first_line_y = min(uniq_y)
c.check("number_at_start", num_word == "1"
        and num_hit and round(num_hit[0][2], 1) == first_line_y
        and num_hit[0][1] < first_body[0][1],
        f"номер '1' не в начале первой строки заголовка: top={top}, "
        f"номер={num_hit}, текст начин. x={round(first_body[0][1],1)}")

# 2. Заголовок переносится на >=2 строки.
c.check("heading_2plus_lines", len(uniq_y) >= 2,
        f"заголовок не на 2+ строки: уникальных yMin={len(uniq_y)} ({uniq_y})")

# 3. Все строки заголовка + тело раздела на одной странице.
pages = {w[0] for w in head_words} | {head_page}
c.check("all_on_one_page", pages == {head_page} and h.page_count(pdf) == 1,
        f"заголовок/раздел разъехались по страницам: {pages}, "
        f"всего страниц {h.page_count(pdf)}")

c.done()
