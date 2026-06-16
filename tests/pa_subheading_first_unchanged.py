"""pa_flag-subheading-first: фича-отступ-перед-подразделом=да НЕ добавляет
отступ перед ПЕРВЫМ подразделом сразу после заголовка раздела. y первого
подраздела одинаков с флагом и без него."""
import helpers as h

c = h.Checks("pa_subheading_first_unchanged")
pdf_on = h.compile("pa_subheading_first_on.typ")
pdf_off = h.compile("pa_subheading_first_off.typ")

y1_on = h.y_of(pdf_on, "ПервыйПодраздел")
y1_off = h.y_of(pdf_off, "ПервыйПодраздел")

c.check("found_first", y1_on is not None and y1_off is not None,
        f"первый подраздел не найден: on={y1_on} off={y1_off}")

# Первый подраздел не сдвигается флагом (исключение по логике пакета).
c.check("first_unchanged",
        y1_on is not None and y1_off is not None and abs(y1_on - y1_off) < 1.0,
        f"первый подраздел сдвинулся: on={y1_on} off={y1_off} (ждём равенство)")
c.done()
