"""pl point 11: неразрывный пробел перед тире держит '—' на одной строке
с предшествующим словом. Функциональная проверка по координатам (poppler
нормализует nbsp в обычный пробел): в узком box 34pt 'тест' и '—' имеют
одинаковый yMin (одна строка), хотя без флага тире уехало бы вниз."""
import helpers as h

c = h.Checks("pl_typo_dash_nbsp")
pdf = h.compile("pl_typo_dash_nbsp.typ")
ws = [w for w in h.words(pdf) if not (w[5].isdigit() and w[2] > 700)]  # без футера

тест = next((w for w in ws if w[5] == "тест"), None)
тире = next((w for w in ws if w[5] == "—"), None)

c.check("both_present", тест is not None and тире is not None,
        f"нет 'тест' или '—': {[w[5] for w in ws]}")
if тест and тире:
    c.check("same_line", abs(тест[2] - тире[2]) < 1.0,
            f"тире на другой строке: yMin тест={тест[2]:.1f} тире={тире[2]:.1f}")
else:
    c.check("same_line", False, "нет слов для проверки")
c.done()
