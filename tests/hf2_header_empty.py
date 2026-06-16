"""hf2: ВЕРХНИЙ колонтитул пустой (header: none по факту default typst).

style_page НЕ задаёт header — значит он пустой. Верхнее поле 20мм=56.69pt.
Первое содержимое начинается на yMin≈56.25 (вплотную к границе верхнего поля).
В верхней зоне листа (выше первой строки тела) НЕ должно быть НИКАКИХ слов —
ни номера, ни текста колонтитула.
"""
import helpers as h

c = h.Checks("hf2_header_empty")
pdf = h.compile("hf2_header_empty.typ")

for p in (1, 2):
    pws = [w for w in h.words(pdf) if w[0] == p]
    c.check(f"p{p}_has_content", len(pws) > 0, f"стр.{p}: пусто")
    if not pws:
        continue

    top = h.first_word(pdf, p)
    ymin = top[0]

    # Первое содержимое стоит на границе верхнего поля (~56.25pt), а не ниже
    # из-за вытеснения колонтитулом.
    c.check(f"p{p}_content_top_at_margin",
            54.0 < ymin < 59.0,
            f"стр.{p}: верх содержимого yMin={ymin:.2f}, ждём ~56.25 (граница 20мм)")

    # В зоне колонтитула (выше границы верхнего поля, y<54) нет ни одного слова.
    in_header_zone = [w for w in pws if w[2] < 54.0]
    c.check(f"p{p}_no_words_in_header_zone",
            len(in_header_zone) == 0,
            f"стр.{p}: в верхней зоне есть слова: {[(w[5], round(w[2],1)) for w in in_header_zone]}")

c.done()
