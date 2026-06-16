"""pa_flag-subheading-on: фича-отступ-перед-подразделом=да → перед ВТОРЫМ
подразделом добавляется пустая строка, поэтому его заголовок опускается ниже,
чем без флага. Сравниваем y 'ПодразделБета' в да-компиляции и нет-компиляции."""
import helpers as h

c = h.Checks("pa_subheading_second")
pdf_on = h.compile("pa_subheading_on.typ")
pdf_off = h.compile("pa_subheading_off.typ")

y2_on = h.y_of(pdf_on, "ПодразделБета")
y2_off = h.y_of(pdf_off, "ПодразделБета")

c.check("found_second", y2_on is not None and y2_off is not None,
        f"второй подраздел не найден: on={y2_on} off={y2_off}")

# С флагом второй подраздел ниже (добавлена пустая строка ≈ 1 интервал).
c.check("second_lower_with_flag",
        y2_on is not None and y2_off is not None and (y2_on - y2_off) > 8.0,
        f"второй подраздел не опустился: on={y2_on} off={y2_off} "
        f"(дельта {None if y2_on is None else y2_on - y2_off}, ждём >8)")
c.done()
