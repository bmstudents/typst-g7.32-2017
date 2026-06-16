"""g12_typo_nbsp_dash: неразрывный пробел перед тире держит тире на одной
строке с предшествующим словом. Функциональная проверка (poppler нормализует
nbsp в обычный пробел, поэтому проверяем по координатам, а не по байтам):
в узком box 'тест —' оба на одной строке (одинаковый yMin)."""
import helpers as h

c = h.Checks("g12_typo_nbsp_dash")
pdf = h.compile("g12_typo_nbsp_dash.typ")
ws = [w for w in h.words(pdf) if not (w[5].isdigit() and w[2] > 700)]  # без футера-номера

тест = next((w for w in ws if w[5] == "тест"), None)
тире = next((w for w in ws if w[5] == "—"), None)

c.check("both_present", тест is not None and тире is not None,
        f"нет 'тест' или '—': {[w[5] for w in ws]}")

# одинаковый yMin → одна строка (тире не уехало на следующую)
if тест and тире:
    c.check("same_line", abs(тест[2] - тире[2]) < 1.0,
            f"тире на другой строке: yMin тест={тест[2]:.1f} тире={тире[2]:.1f}")
    # тире стоит справа от слова (после него, а не перед — порядок сохранён)
    c.check("dash_after_word", тире[1] > тест[1],
            f"тире не после слова: x тест={тест[1]:.1f} тире={тире[1]:.1f}")
else:
    c.check("same_line", False, "нет слов для проверки")
    c.check("dash_after_word", False, "нет слов для проверки")

c.done()
