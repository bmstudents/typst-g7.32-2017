"""pf_recog_normal_numbered: '= Обычный раздел' НЕ распознан как структурный — получает номер '1', далее '2'."""
import helpers as h

c = h.Checks("pf_recog_normal_numbered")
pdf = h.compile("pf_recog_normal_numbered.typ")
t = h.text(pdf)

# Обычные разделы получают последовательные номера.
c.check("first_numbered_1", "1 Обычный раздел" in t, "первый раздел не получил '1'")
c.check("second_numbered_2", "2 Второй обычный раздел" in t, "второй раздел не получил '2'")

# Не капсуется как структурный (в оглавлении 'Обычный', а не 'ОБЫЧНЫЙ').
toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
toc_words = [w[5] for w in h.words(pdf) if w[0] == toc_page]
c.check("not_uppercased", "Обычный" in toc_words and "ОБЫЧНЫЙ" not in toc_words,
        f"обычный раздел ошибочно капсован: {toc_words[:12]}")

# Запись начинается с числового префикса '1' в начале строки.
y = next(w[2] for w in h.words(pdf) if w[0] == toc_page and w[5] == "Обычный")
line = sorted([w for w in h.words(pdf) if w[0] == toc_page and abs(w[2] - y) < 1.0],
              key=lambda w: w[1])
c.check("line_starts_with_number", line[0][5] == "1" and line[0][1] < 110,
        f"строка не начинается с номера '1': {line[0][5]!r} x={line[0][1]:.1f}")

c.done()
