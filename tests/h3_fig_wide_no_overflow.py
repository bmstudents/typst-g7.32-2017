"""h3 РИСУНКИ: широкий rect(17cm) не должен вылезать за правое поле страницы.

Геометрия (config): A4 595.28pt; поля left=30mm=85.04pt, right=15mm=42.52pt.
Полоса набора: x ∈ [85.04, 552.76]. Тело рисунка обязано умещаться в эту полосу.
17cm = 481.9pt — это ШИРЕ полосы набора (552.76−85.04 = 467.72pt), поэтому
центрированный rect рискует вылезти за оба поля.

Тело rect бестекстовое, поэтому в него #place'ом вбиты маркеры у самых краёв:
ПРАВКРАЙ (правый край тела) и ЛЕВКРАЙ (левый). Их bbox даёт фактические границы.

ИНВАРИАНТЫ (с допуском 1pt на округление pdftotext):
  1. правый край тела (xMax ПРАВКРАЙ) ≤ 552.76 — не вылезает вправо;
  2. левый край тела (xMin ЛЕВКРАЙ) ≥ 85.04 − 1 — не вылезает влево;
  3. ни одно слово страницы (тело+подпись) не пересекает правое поле 552.76.
"""
import helpers as h

c = h.Checks("h3_fig_wide_no_overflow")
pdf = h.compile("h3_fig_wide_no_overflow.typ")
ws = h.words(pdf)

LEFT = 85.04      # 30mm
RIGHT = 552.76    # 595.28 − 15mm
TOL = 1.0


def one(word):
    hits = [w for w in ws if w[5] == word]
    return hits[0] if len(hits) == 1 else None


lm = one("ЛЕВКРАЙ")
rm = one("ПРАВКРАЙ")

c.check("edge_markers_present", lm is not None and rm is not None,
        f"краевые маркеры тела не найдены: left={lm} right={rm}")

if lm and rm:
    # 1. правый край тела не за правым полем
    c.check("body_right_within_margin", rm[3] <= RIGHT + TOL,
            f"ПЕРЕПОЛНЕНИЕ ВПРАВО: правый край тела xMax={rm[3]:.2f} > поле {RIGHT} "
            f"(на {rm[3] - RIGHT:.2f}pt). rect 17cm шире полосы набора 467.7pt и вылез.")
    # 2. левый край тела не за левым полем
    c.check("body_left_within_margin", lm[1] >= LEFT - TOL,
            f"ПЕРЕПОЛНЕНИЕ ВЛЕВО: левый край тела xMin={lm[1]:.2f} < поле {LEFT} "
            f"(на {LEFT - lm[1]:.2f}pt)")

# 3. вообще НИ ОДНО слово не пересекает правое поле
over = [w for w in ws if w[3] > RIGHT + TOL]
c.check("no_word_crosses_right_margin", not over,
        f"за правым полем {RIGHT}: " +
        "; ".join(f"'{w[5]}' xMax={w[3]:.2f} (стр{w[0]})" for w in over))

c.done()
