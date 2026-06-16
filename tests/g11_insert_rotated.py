"""g11_insert_rotated: повернуто:true компилится без ошибок, page_count ок,
содержимое листа реально повёрнуто на 90° (bbox выше, чем шире)."""
import helpers as h

c = h.Checks("g11_insert_rotated")
pdf = h.compile("g11_insert_rotated.typ")

# компиляция и количество страниц: текст / повёрнутый лист / текст
c.check("compiles_3_pages", h.page_count(pdf) == 3, f"ожидали 3 страницы, получили {h.page_count(pdf)}")

# лист на стр.2
skan = [w for w in h.words(pdf) if w[0] == 2 and w[5] == "скан"]
c.check("sheet_on_page_2", len(skan) == 1, f"на стр.2 нет слова 'скан': {skan}")

# поворот на 90°: bbox слова выше, чем шире (высота > ширины)
if skan:
    _, x0, y0, x1, y1, _ = skan[0]
    w, hgt = x1 - x0, y1 - y0
    c.check("rotated_90", hgt > w, f"bbox 'скан' не повёрнут: ширина={w:.1f} высота={hgt:.1f}")
else:
    c.check("rotated_90", False, "нет слова для проверки поворота")

c.done()
