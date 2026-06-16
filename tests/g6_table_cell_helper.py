"""g6 ТАБЛИЦЫ: ячейка() компилируется, текст виден, кегль 12pt < основного,
переносы в ячейке выключены (длинное слово не разрывается)."""
import helpers as h

c = h.Checks("g6_table_cell_helper")
pdf = h.compile("g6_table_cell_helper.typ")
t = h.text(pdf)
ws = h.words(pdf)

c.check("cell_text_visible", "Тип" in t, f"текст ячейки 'Тип' не виден в:\n{t}")

# Перенос в ячейке выключен: длинное слово остаётся целым (без дефиса/разрыва).
long = "Значениетипаоченьдлинноесловобезпробелов"
c.check("no_hyphenation", long in t,
        f"длинное слово разорвалось переносом, в тексте нет '{long}':\n{t}")

# Кегль ячейки (12pt) меньше основного текста заголовка-таблицы (14pt):
# высота глифов слова из ячейки меньше, чем у обычной ячейки тела.
def gh(word):
    hits = [w for w in ws if w[5] == word]
    return (hits[0][4] - hits[0][2]) if hits else None
h_cell = gh("Тип")            # содержимое через ячейку() → 12pt
h_body = gh("Параметр")       # обычная ячейка тела → 14pt
c.check("cell_smaller_font", h_cell is not None and h_body is not None and h_cell < h_body,
        f"высота_ячейки={h_cell} высота_тела={h_body}")
c.done()
