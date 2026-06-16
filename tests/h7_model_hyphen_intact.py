"""h7_model_hyphen_intact: название модели «ESP32-S2» не рвётся по внутреннему
дефису при переносе строки (флаг неразрывных величин).

Механизм пакета: литеральный дефис '-' внутри модели заменяется на
неразрывный U+2011 ('‑'), который запрещает разрыв строки. Ширина box (34pt)
подобрана компиляцией:
  - БЕЗ флага: 'ESP32-' / 'S2' на двух строках (yMin 56.3 / 80.4) — разрыв.
  - С флагом:  'ESP32‑S2' — ОДИН токен на одной строке (yMin 56.3).
Жёстко: токен целый, дефис именно неразрывный (U+2011, не обычный U+002D),
и нет осколков 'ESP32-' / 'S2' на разных строках.
"""
import helpers as h

c = h.Checks("h7_model_hyphen_intact")
pdf = h.compile("h7_model_hyphen_intact.typ")
ws = [w for w in h.words(pdf) if not (w[5].isdigit() and w[2] > 700)]
names = [w[5] for w in ws]

NB = "ESP32‑S2"  # с неразрывным дефисом U+2011

# Целый токен присутствует (с неразрывным дефисом).
whole = next((w for w in ws if w[5] == NB), None)
c.check("model_single_token",
        whole is not None,
        f"нет целого токена 'ESP32‑S2' (U+2011); токены: {names}")

# Дефис именно неразрывный U+2011, а не обычный U+002D.
c.check("hyphen_is_nonbreaking_u2011",
        whole is not None and "-" not in whole[5] and "‑" in whole[5],
        f"дефис не заменён на U+2011: токен={None if whole is None else whole[5]!r}")

# Не разорвано на 'ESP32-' / 'S2'.
broken = ("ESP32-" in names or "ESP32" in names) and "S2" in names
c.check("not_split_into_pieces",
        not broken,
        f"модель разорвана на осколки: {names}")

# Целый токен лежит на одной строке (yMin == yMax-диапазон одной строки) и
# выше нет переноса внутри него — проверяем, что предшествующее 'ппп' на
# другой (верхней) строке, а сам токен не делит yMin с осколком.
ппп = next((w for w in ws if w[5] == "ппп"), None)
if whole and ппп:
    c.check("wrapped_as_whole_below_prefix",
            whole[2] > ппп[2] + 1.0,
            f"токен не перенёсся целиком ниже 'ппп': yMin ппп={ппп[2]:.2f} "
            f"модель={whole[2]:.2f}")
else:
    c.check("wrapped_as_whole_below_prefix", False,
            f"нет 'ппп' или целого токена: {names}")

c.done()
