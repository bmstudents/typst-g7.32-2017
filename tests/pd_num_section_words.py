"""pd num-section: координатно — номер '1' стоит отдельным словом слева от 'Анализ'."""
import helpers as h

c = h.Checks("pd_num_section_words")
pdf = h.compile("pd_num_section_words.typ")
ws = [w for w in h.words(pdf) if w[0] == 1]

num = [w for w in ws if w[5] == "1"]
title = [w for w in ws if w[5] == "Анализ"]

# Номер '1' присутствует как отдельное слово (footer-номер страницы тоже '1',
# но он внизу; берём верхний — заголовок в начале страницы).
num_top = sorted(num, key=lambda t: t[2])[:1]

c.check("number_word_exists",
        len(num_top) == 1,
        f"нет отдельного слова-номера '1' в заголовке: {num}")

c.check("title_exists",
        len(title) == 1,
        f"нет слова 'Анализ': {title}")

# Номер стоит левее заголовка на той же строке (одинаковый yMin).
if num_top and title:
    n = num_top[0]
    a = title[0]
    c.check("number_left_of_title",
            n[1] < a[1] and abs(n[2] - a[2]) < 3,
            f"номер x={n[1]:.1f} y={n[2]:.1f}, заголовок x={a[1]:.1f} y={a[2]:.1f}")
else:
    c.check("number_left_of_title", False, "нет номера или заголовка для сравнения")

c.done()
