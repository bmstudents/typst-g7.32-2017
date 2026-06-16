"""pd normal-section-left: обычный нумерованный раздел выровнен влево, не по центру.

Из-за абзацного отступа (parIndent 1.25см) первая строка заголовка начинается с
x≈120, но это всё равно левая зона — заметно левее центра текстового поля (~319).
"""
import helpers as h

c = h.Checks("pd_normal_section_left")
pdf = h.compile("pd_normal_section_left.typ")
ws = [w for w in h.words(pdf) if w[0] == 1]
cx = 319.0

# Верхний '1' (номер заголовка, не футер-номер внизу).
nums = sorted([w for w in ws if w[5] == "1"], key=lambda t: t[2])
title = [w for w in ws if w[5] == "Анализ"]

c.check("number_present", len(nums) >= 1, "нет номера '1'")
c.check("title_present", len(title) >= 1, "нет 'Анализ'")

if nums:
    nx = nums[0][1]
    # Номер в левой зоне (≈ левое поле или абзацный отступ), но строго левее центра.
    c.check("number_left_zone",
            nx < 130,
            f"номер заголовка x={nx:.1f}, ждём левую зону (<130)")
    c.check("not_centered",
            nx < cx - 80,
            f"номер x={nx:.1f} слишком близко к центру {cx} — похоже на центрирование")
else:
    c.check("number_left_zone", False, "нет номера")
    c.check("not_centered", False, "нет номера")

# Заголовок не центрирован: центр строки заголовка заметно левее cx.
if nums and title:
    line_center = (nums[0][1] + title[0][3]) / 2
    c.check("heading_line_not_centered",
            line_center < cx,
            f"центр строки заголовка {line_center:.1f} не левее центра поля {cx}")
else:
    c.check("heading_line_not_centered", False, "нет данных строки заголовка")

c.done()
