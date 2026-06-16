"""pb font-size-14: один и тот же набор глифов 'Hgxy' в основном тексте (14pt)
заметно выше, чем в листинге (12pt). Точное отношение 14/12 по глиф-боксам не
проверяем: высоты выносных у Times и Courier разные, поэтому отношение боксов
(~1.32) не совпадает с отношением кеглей — это нормально. Проверяем порядок
и правдоподобную величину разрыва."""
import helpers as h

c = h.Checks("pb_font_size14_vs_code")
pdf = h.compile("pb_font_size14_vs_code.typ")

hits = [w for w in h.words(pdf) if w[5] == "Hgxy"]
c.check("two_samples", len(hits) == 2, f"ждём 2 вхождения 'Hgxy', нашли {len(hits)}")

if len(hits) == 2:
    # верхнее по странице — основной текст, нижнее — листинг
    hits.sort(key=lambda t: t[2])
    body_h = hits[0][4] - hits[0][2]
    code_h = hits[1][4] - hits[1][2]

    c.check("body_taller",
            body_h > code_h,
            f"основной текст не выше кода: тело={body_h:.2f} код={code_h:.2f}")

    ratio = body_h / code_h
    # Разрыв правдоподобен для 14pt vs 12pt: не меньше отношения кеглей (1.167)
    # и не больше разумного потолка с учётом разных метрик шрифтов.
    c.check("gap_consistent_with_14_12",
            1.15 <= ratio <= 1.45,
            f"отношение высот {ratio:.3f} вне [1.15;1.45] для 14pt vs 12pt (тело={body_h:.2f} код={code_h:.2f})")

c.done()
