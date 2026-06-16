"""pb table-inset-10: содержимое ячейки отстоит от левой границы таблицы на
инсет 10pt. Таблица в 1fr на всю ширину поля: левая граница = 85.04, текст у 95.04."""
import helpers as h

c = h.Checks("pb_table_inset_left")
pdf = h.compile("pb_table_inset_left.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 700]

cell = [w for w in ws if w[5] == "Я"]
c.check("cell_visible", len(cell) == 1, f"текст ячейки 'Я' не найден: {[w[5] for w in ws]}")

if cell:
    x0 = cell[0][1]
    table_left = 85.04  # таблица 1fr от левого поля
    inset = x0 - table_left
    c.check("left_inset_10pt",
            abs(inset - 10) < 2,
            f"инсет слева {inset:.2f}pt, ждём ~10 (текст x0={x0:.2f}, граница {table_left})")

    # Текст НЕ прижат к границе таблицы (отступ заметно больше нуля).
    c.check("not_flush_left",
            inset > 5,
            f"текст ячейки прижат к границе: инсет {inset:.2f}pt")

c.done()
