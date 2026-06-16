"""h2 ТАБЛИЦЫ #5: «Продолжение таблицы 1» на стр.2 с положительным зазором до тела.

Длинная таблица перетекает на следующую страницу. Там сверху печатается
«Продолжение таблицы 1», а ниже — продолжение строк данных. Между нижним краем
надписи и верхом первой строки тела на этой странице обязан быть зазор > 0
(надпись не наезжает на данные).

ИНВАРИАНТЫ:
  1) >=2 страниц и «Продолжение» присутствует на стр.2;
  2) на стр.2 это именно ПРОДОЛЖЕНИЕ — выше (на стр.1) уже были строки данных
     (в отличие от ложного случая в #2);
  3) зазор yMax(«…1») < yMin(первая строка тела на стр.2), зазор > 0.
"""
import helpers as h

c = h.Checks("h2_continuation_gap")
pdf = h.compile("h2_continuation_gap.typ")
ws = h.words(pdf)

c.check("multipage", h.page_count(pdf) >= 2,
        f"таблица не перетекла: {h.page_count(pdf)} стр.")

cont = [w for w in ws if w[5] == "Продолжение"]
cont_p2 = [w for w in cont if w[0] == 2]
c.check("continuation_on_p2", len(cont_p2) >= 1,
        f"«Продолжение» на стр.2 не найдено; найдено на стр {[w[0] for w in cont]}")

# на стр.1 должны быть данные (это настоящее продолжение, не сирота-шапка)
rows_p1 = [int(w[5][2:]) for w in ws if w[0] == 1 and w[5].startswith("СД")]
c.check("real_continuation", len(rows_p1) >= 1,
        f"на стр.1 нет строк данных ({len(rows_p1)}) — продолжать нечего, надпись ложна")

if cont_p2:
    cont_ymax = max(w[4] for w in cont_p2)
    # первая строка тела на стр.2 = самое верхнее слово стр.2 НИЖЕ надписи
    below = [w for w in ws if w[0] == 2 and w[2] > cont_ymax]
    assert below, "под надписью продолжения нет строк тела"
    first_body = min(below, key=lambda t: t[2])
    gap = first_body[2] - cont_ymax
    c.check("gap_positive", gap > 0,
            f"НАЕЗД «Продолжение» (yMax={cont_ymax:.1f}) на первую строку тела "
            f"«{first_body[5]}» (yMin={first_body[2]:.1f}), зазор={gap:.1f} (ожидал >0). "
            f"Файл: h2_continuation_gap.typ")
    # данные на стр.2 продолжают нумерацию (не начинаются заново с 1)
    rows_p2 = sorted(int(w[5][2:]) for w in ws if w[0] == 2 and w[5].startswith("СД"))
    c.check("numbering_continues", rows_p2 and min(rows_p2) == max(rows_p1) + 1,
            f"нумерация строк не продолжается: стр.1 заканчивается на {max(rows_p1)}, "
            f"стр.2 начинается с {min(rows_p2) if rows_p2 else None}")

c.done()
