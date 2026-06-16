"""pl point 10: с флагом неразрывных величин '8x8x8' даёт '8×8×8' —
латинская x между цифрами заменена на знак умножения ×."""
import helpers as h

c = h.Checks("pl_typo_times")
pdf = h.compile("pl_typo_times.typ")
t = h.text(pdf)

c.check("times_in_text", "8×8×8" in t, f"нет '8×8×8' в тексте:\n{t!r}")
c.check("no_latin_x", "8x8" not in t, f"осталась латинская x между цифрами:\n{t!r}")
c.done()
