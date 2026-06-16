"""pa_flag-nonbreaking-off (аспект 2): прямое сравнение нет vs да на одном
исходнике '8x8x8'. Без флага — латинская x и нет '×'; с флагом — '×' и нет
латинской 'x'. Состояния взаимоисключающие."""
import helpers as h

c = h.Checks("pa_nonbreaking_off_vs_on")
pdf_off = h.compile("pa_nonbreaking_off_times.typ")
pdf_on = h.compile("pa_nonbreaking_on_times.typ")

t_off = h.text(pdf_off)
t_on = h.text(pdf_on)

c.check("off_latin_no_times", ("8x8x8" in t_off) and ("×" not in t_off),
        f"off-состояние неверно:\n{t_off!r}")
c.check("on_times_no_latin", ("8×8×8" in t_on) and ("8x8x8" not in t_on),
        f"on-состояние неверно:\n{t_on!r}")
c.check("states_differ", t_off != t_on,
        "тексты нет/да совпали — флаг не повлиял")
c.done()
