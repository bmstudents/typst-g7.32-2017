"""g2: флаг фича-отступ-перед-подразделом=да добавляет пустую строку
перед ВТОРЫМ подразделом, но НЕ перед первым после заголовка раздела.

Сравниваем две компиляции одного документа: с флагом (on) и без (off).
"""
import helpers as h

c = h.Checks("g2_subsection_spacing")
pdf_on = h.compile("g2_subsection_spacing_on.typ")
pdf_off = h.compile("g2_subsection_spacing_off.typ")

y1_on = h.y_of(pdf_on, "Первый")
y1_off = h.y_of(pdf_off, "Первый")
y2_on = h.y_of(pdf_on, "Второй")
y2_off = h.y_of(pdf_off, "Второй")

c.check("found_all",
        None not in (y1_on, y1_off, y2_on, y2_off),
        f"не нашли подзаголовки: on=({y1_on},{y2_on}) off=({y1_off},{y2_off})")

# Первый подраздел сразу после раздела — флаг НЕ должен сдвигать его.
c.check("first_subsection_unchanged",
        abs(y1_on - y1_off) < 1.0,
        f"первый подраздел сдвинулся: on={y1_on:.2f} off={y1_off:.2f} (ждём равенство)")

# Второй подраздел с флагом ниже (добавлена пустая строка ≈ 14.8pt).
c.check("second_subsection_lower_with_flag",
        y2_on - y2_off > 8.0,
        f"второй подраздел не опустился: on={y2_on:.2f} off={y2_off:.2f} "
        f"(дельта {y2_on - y2_off:.2f}, ждём >8)")

c.done()
