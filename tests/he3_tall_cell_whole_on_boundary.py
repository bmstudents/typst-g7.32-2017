"""he3_tall_cell_whole_on_boundary: высокая НЕРАЗРЫВНАЯ ячейка (ячейка[] →
block breakable:false) на границе страницы.

Инварианты:
1. Все шесть строк ячейки («один.»..«шесть.») оказываются на ОДНОЙ
   странице — ячейка не разрезана посреди высокой строки.
2. Содержимое ячейки не наезжает на футер (нижний край текста выше
   области номера страницы).
3. Соседние строки таблицы (1 «Короткая…», 3 «Ещё…») и весь текст на
   месте — ничего не проглочено."""
import helpers as h

c = h.Checks("he3_tall_cell_whole_on_boundary")
pdf = h.compile("he3_tall_cell_whole_on_boundary.typ")
ws = h.words(pdf)

# Маркеры строк ячейки: «один.» … «шесть.» — последние слова каждой строки.
line_tokens = ["один.", "два.", "три.", "четыре.", "пять.", "шесть."]
pages_of = {}
for tok in line_tokens:
    pgs = sorted({w[0] for w in ws if w[5] == tok})
    pages_of[tok] = pgs

present = all(pages_of[tok] for tok in line_tokens)
c.check("all_cell_lines_present",
        present,
        f"не все строки ячейки отрисованы: {pages_of}")

all_pages = {p for pgs in pages_of.values() for p in pgs}
c.check("tall_cell_not_split",
        len(all_pages) == 1,
        f"высокая ячейка разрезана между страницами: {pages_of}")

# Контент ячейки не наезжает на футер. Нижний предел контента A4 при
# нижнем поле 20мм ≈ 842 − 56.7 = 785pt; футер ниже. Слова ячейки должны
# иметь yMax заметно выше футера.
cell_words = [w for w in ws if w[5] in line_tokens]
max_ymax = max((w[4] for w in cell_words), default=0)
c.check("cell_above_footer",
        max_ymax < 790,
        f"низ ячейки yMax={max_ymax:.1f} заходит в зону футера (>790)")

# Соседние строки и хвост текста присутствуют.
c.check("neighbors_present",
        any(w[5] == "Короткая" for w in ws)
        and any(w[5] == "после" for w in ws),
        "потеряны соседние строки таблицы")

c.done()
