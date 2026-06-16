"""g1: геометрия страницы — A4, левое поле 30мм (~85pt), правое 15мм."""
import helpers as h

c = h.Checks("g1_page_geometry")
pdf = h.compile("g1_page_geometry.typ")
ws = [w for w in h.words(pdf) if w[0] == 1]

# Ширина A4 ≈ 595.3pt. Берём максимальный правый край как нижнюю оценку ширины,
# но для самой ширины ориентируемся на правое поле: max x1 ближе к правому краю.
min_x0 = min(w[1] for w in ws)        # левое поле
max_x1 = max(w[3] for w in ws)        # правый край текста
page_w = 595.276                       # A4 в pt

# Левое поле 30мм = 85.04pt. Первое слово абзаца имеет отступ 1.25см,
# но самый левый край строки (продолжения) = граница поля.
c.check("left_margin_30mm",
        abs(min_x0 - 85.04) < 4,
        f"левый край {min_x0:.1f}, ждём ~85.04 (30мм)")

# Правое поле 15мм = 42.52pt от края. Правый край текста ~552.76.
right_margin = page_w - max_x1
c.check("right_margin_15mm",
        abs(right_margin - 42.52) < 4,
        f"правое поле {right_margin:.1f}, ждём ~42.52 (15мм); max_x1={max_x1:.1f}")

# Левое поле заметно больше правого (30мм против 15мм).
c.check("left_gt_right",
        min_x0 > right_margin + 20,
        f"левое {min_x0:.1f} должно быть заметно больше правого {right_margin:.1f}")

c.done()
