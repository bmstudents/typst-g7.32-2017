"""pa_flag-nonbreaking-off: по умолчанию (фича-неразрывные-величины=нет)
'8x8x8' остаётся с латинской x, знака умножения '×' в тексте НЕТ."""
import helpers as h

c = h.Checks("pa_nonbreaking_off_times")
pdf = h.compile("pa_nonbreaking_off_times.typ")  # без флага → нет по умолчанию
t = h.text(pdf)

c.check("latin_x_kept", "8x8x8" in t, f"исходная связка '8x8x8' пропала:\n{t!r}")
c.check("no_times_sign", "×" not in t, f"в тексте появился '×' без флага:\n{t!r}")
c.done()
