"""h7_times_sign: с флагом неразрывных величин латинская 'x' между цифрами
в размерах ('8x8x8', '16x16') заменяется на знак умножения '×' (U+00D7).

Жёстко:
  - '8×8×8' и '16×16' собраны в текстовом слое (× = U+00D7 сохраняется);
  - ни одной латинской 'x' между цифрами не осталось (точные подстроки);
  - '×' стоит МЕЖДУ цифрами на одной строке (один токен в bbox → не разорвано).
× (U+00D7) — это НЕ латинская 'x' (U+0078); различаем по кодпойнту.
"""
import helpers as h

c = h.Checks("h7_times_sign")
pdf = h.compile("h7_times_sign.typ")
t = h.text(pdf)

# Знак умножения присутствует и это именно U+00D7, не латиница.
c.check("times_sign_u00d7_present",
        "×" in t,
        f"нет '×' (U+00D7) в тексте:\n{t!r}")

# Обе связки собраны целиком.
c.check("8x8x8_converted",
        "8×8×8" in t,
        f"нет '8×8×8' в тексте:\n{t!r}")
c.check("16x16_converted",
        "16×16" in t,
        f"нет '16×16' в тексте:\n{t!r}")

# Латинской x между цифрами не осталось (ни '8x', ни 'x8', ни '6x', ни 'x1').
import re
leftover = re.findall(r"[0-9]x[0-9]", t)
c.check("no_latin_x_between_digits",
        not leftover,
        f"осталась латинская x между цифрами: {leftover} в:\n{t!r}")

# Связка не разорвана: токен с × присутствует целиком в координатном слое.
ws = [w for w in h.words(pdf) if not (w[5].isdigit() and w[2] > 700)]
token = next((w for w in ws if w[5] == "8×8×8"), None)
c.check("token_intact_one_line",
        token is not None,
        f"токен '8×8×8' не цельный в bbox: {[w[5] for w in ws]}")

c.done()
