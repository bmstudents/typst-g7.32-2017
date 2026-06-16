"""pb margin-top-20: верх первого слова страницы yMin≈56.25pt (поле 20мм=56.69
минус приподнятость глиф-бокса над базовой линией)."""
import helpers as h

c = h.Checks("pb_margin_top_first")
pdf = h.compile("pb_margin_top_first.typ")

fw = h.first_word(pdf, 1)
c.check("top_word_y",
        fw is not None and abs(fw[0] - 56.25) < 2,
        f"верх первого слова y={None if fw is None else round(fw[0],2)}, ждём ~56.25")

# Граница поля 20мм = 56.69pt; первое слово не выше неё больше чем на ~1pt
# и не ниже чем на пару pt.
c.check("not_above_margin",
        fw is not None and fw[0] >= 56.69 - 2,
        f"первое слово выше верхнего поля: y={None if fw is None else round(fw[0],2)} (поле 56.69)")

c.done()
