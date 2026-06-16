"""pl point 7: вставить-лист с 'повернуто: да' (параметр БЕЗ ё) компилируется,
лист-страница есть, содержимое реально повёрнуто на 90° (bbox выше, чем шире)."""
import helpers as h

c = h.Checks("pl_insert_rotated")
pdf = h.compile("pl_insert_rotated.typ")

c.check("three_pages", h.page_count(pdf) == 3,
        f"ожидали 3 страницы, получили {h.page_count(pdf)}")

skan = [w for w in h.words(pdf) if w[0] == 2 and w[5] == "скан"]
c.check("sheet_on_page2", len(skan) == 1, f"на стр.2 нет слова 'скан': {skan}")

if skan:
    _, x0, y0, x1, y1, _ = skan[0]
    w, ht = x1 - x0, y1 - y0
    c.check("rotated_90", ht > w,
            f"bbox 'скан' не повёрнут: ширина={w:.1f} высота={ht:.1f}")
else:
    c.check("rotated_90", False, "нет слова для проверки поворота")
c.done()
