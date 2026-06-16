"""he2 EDGE-таблицы #7: спецсимволы/юникод (± × № —) + числовой столбец.

ИНВАРИАНТЫ:
  1) все спецсимволы дошли до текстового слоя: № ± × — (не превратились в
     mojibake / не выпали);
  2) символы внутри ячеек, а не в подписи: '±5', '8 × 8', '10 — 20' видны;
  3) числовой столбец № (1, 2, 3) выровнен по левому краю своей колонки
     (один x0 у '1','2','3') — числа в столбце стоят колонкой, не «гуляют».

Файл пакета при провале: gost732-2017/styles/typography.typ (если включён) /
styles/table.typ.
"""
import helpers as h

c = h.Checks("he2_tab_unicode")
pdf = h.compile("he2_tab_unicode.typ")
t = h.text(pdf)
ws = h.words(pdf)

for ch, name in [("№", "numero"), ("±", "plusminus"), ("×", "times"), ("—", "emdash")]:
    c.check(f"char_{name}", ch in t, f"символ {ch!r} (U+{ord(ch):04X}) потерян в тексте:\n{t!r}")

# числовой столбец № : '1','2','3' в первой колонке тела таблицы.
# Тело начинается ниже шапки '№' (y≈121). Исключаем номер раздела/подписи
# (y<100) и номер страницы (y>700) по вертикали.
y_head = next((w[2] for w in ws if w[0] == 1 and w[5] == "№"), None)
nums = [w for w in ws if w[0] == 1 and w[5] in {"1", "2", "3"}
        and y_head is not None and w[2] > y_head and w[2] < 700]
xs = sorted(set(round(w[1], 1) for w in nums))
c.check("numeric_column_aligned", len(nums) >= 3 and (max(xs) - min(xs)) <= 1.5,
        f"числовой столбец № не выровнен: найдено {len(nums)} чисел, x-координаты {xs} "
        f"(разброс > 1.5pt). Файл: gost732-2017/styles/table.typ")
# и числа столбца стоят под заголовком '№' (один x0)
x_head = next((w[1] for w in ws if w[0] == 1 and w[5] == "№"), None)
c.check("numeric_under_header", xs and x_head is not None and abs(xs[0] - x_head) <= 1.5,
        f"числа столбца (x={xs}) не под заголовком '№' (x={x_head}). "
        f"Файл: gost732-2017/styles/table.typ")
c.done()
