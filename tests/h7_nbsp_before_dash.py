"""h7_nbsp_before_dash: неразрывный пробел перед тире (правило русской
типографики / ГОСТ) удерживает тире на одной строке с предыдущим словом.

Ширина box (26pt) подобрана компиляцией так, что БЕЗ флага 'блок' и '—'
оказываются на разных строках (yMin 56.3 / 80.4), а С флагом — на одной
(оба yMin 56.3). Тк poppler нормализует U+00A0 → пробел, проверка чисто
ФУНКЦИОНАЛЬНАЯ: равенство yMin доказывает неразрывность, плюс порядок
(тире справа от слова) и одинаковый yMax (одна и та же базовая линия).
"""
import helpers as h

c = h.Checks("h7_nbsp_before_dash")
pdf = h.compile("h7_nbsp_before_dash.typ")
ws = [w for w in h.words(pdf) if not (w[5].isdigit() and w[2] > 700)]

блок = next((w for w in ws if w[5] == "блок"), None)
тире = next((w for w in ws if w[5] == "—"), None)

c.check("both_present", блок is not None and тире is not None,
        f"нет 'блок' или '—': {[w[5] for w in ws]}")

if блок and тире:
    # Одна строка: yMin совпадает (допуск < 0.5pt — у нас будет 0.0).
    c.check("dash_same_line",
            abs(блок[2] - тире[2]) < 0.5,
            f"тире ушло на другую строку: yMin блок={блок[2]:.3f} тире={тире[2]:.3f} "
            f"(Δ={abs(блок[2] - тире[2]):.3f})")
    # Та же базовая линия — yMax тоже совпадает.
    c.check("dash_same_baseline",
            abs(блок[4] - тире[4]) < 0.5,
            f"разные базовые линии: yMax блок={блок[4]:.3f} тире={тире[4]:.3f}")
    # Порядок сохранён: тире правее слова (не перепрыгнуло вперёд).
    c.check("dash_after_word",
            тире[1] > блок[3] - 0.5,
            f"тире не после слова: xMax блок={блок[3]:.2f} xMin тире={тире[1]:.2f}")
else:
    c.check("dash_same_line", False, "нет слов")
    c.check("dash_same_baseline", False, "нет слов")
    c.check("dash_after_word", False, "нет слов")

c.done()
