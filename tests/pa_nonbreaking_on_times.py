"""pa_flag-nonbreaking-on: фича-неразрывные-величины=да → '8x8x8' из исходника
превращается в '8×8×8' (латинская x → знак умножения U+00D7)."""
import helpers as h

c = h.Checks("pa_nonbreaking_on_times")
pdf = h.compile("pa_nonbreaking_on_times.typ")
t = h.text(pdf)

c.check("times_sign_present", "×" in t, f"нет '×' (U+00D7) в тексте:\n{t!r}")
c.check("full_8x8x8", "8×8×8" in t, f"нет связки '8×8×8':\n{t!r}")
c.check("no_latin_x", "8x8" not in t and "x8" not in t,
        f"осталась латинская x:\n{t!r}")
c.done()
