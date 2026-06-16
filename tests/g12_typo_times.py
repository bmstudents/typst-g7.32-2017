"""g12_typo_times: с флагом неразрывных величин '8x8x8' в исходнике даёт '8×8×8'
в тексте — латинская x между цифрами заменена на знак умножения ×."""
import helpers as h

c = h.Checks("g12_typo_times")
pdf = h.compile("g12_typo_times.typ")
t = h.text(pdf)

# знак умножения присутствует (× = U+00D7 сохраняется в текстовом слое pdf)
c.check("times_sign_present", "×" in t, f"нет '×' в тексте:\n{t!r}")

# полная связка 8×8×8 собрана
c.check("full_8x8x8", "8×8×8" in t, f"нет '8×8×8' в тексте:\n{t!r}")

# латинская x между цифрами не осталась (была заменена)
c.check("no_latin_x_between_digits", "8x8" not in t and "x8" not in t,
        f"осталась латинская x:\n{t!r}")

c.done()
