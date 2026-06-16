"""pa_flag-subheading-first (аспект 2): в ОДНОЙ компиляции с флагом 'да'
эффект избирательный — первый подраздел не сдвинут (= как без флага), а
второй сдвинут вниз. Проверяем оба факта в одном тесте: дельта первого ≈ 0,
дельта второго заметная."""
import helpers as h

c = h.Checks("pa_subheading_first_vs_second")
pdf_on = h.compile("pa_subheading_first_on.typ")
pdf_off = h.compile("pa_subheading_first_off.typ")

d1 = h.y_of(pdf_on, "ПервыйПодраздел") - h.y_of(pdf_off, "ПервыйПодраздел")
d2 = h.y_of(pdf_on, "ВторойПодраздел") - h.y_of(pdf_off, "ВторойПодраздел")

c.check("first_delta_zero", abs(d1) < 1.0,
        f"первый подраздел сдвинут флагом на {d1:.2f} (ждём ~0)")
c.check("second_delta_positive", d2 > 8.0,
        f"второй подраздел сдвинут лишь на {d2:.2f} (ждём >8)")
c.check("selective_effect", d2 - d1 > 8.0,
        f"эффект не избирательный: d1={d1:.2f} d2={d2:.2f}")
c.done()
