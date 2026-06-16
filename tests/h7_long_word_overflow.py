"""h7_long_word_overflow: дефис мягкого переноса очень длинного слова не должен
свисать за правую границу набора (552.76pt = правое поле 15мм на A4).

ИЗВЕСТНЫЙ БАГ (этот тест его ловит → ожидаемый FAIL): при переносе длинного
слова дефис мягкого переноса (U+00AD в текстовом слое) выходит за правое поле
примерно на ~2.5pt. Жёстко: измеряем xMax токена, заканчивающегося мягким
переносом, и сравниваем с правой границей. Допуск 0.5pt — это перенос, а не
обычный justify-«хвостик».

Тест намеренно не подгоняется под баг: критерий — «дефис НЕ должен свисать».
Если пакет починят (дефис прижат к полю), тест станет PASS автоматически.
"""
import helpers as h

RIGHT = 552.76          # правая граница набора, pt
TOL = 0.5               # допуск на округление координат poppler

c = h.Checks("h7_long_word_overflow")
pdf = h.compile("h7_long_word_overflow.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and not (w[5].isdigit() and w[2] > 700)]

# Найти токен, заканчивающийся мягким переносом U+00AD (точка переноса слова).
hyph = [w for w in ws if w[5].endswith("­")]

c.check("hyphenation_happened",
        len(hyph) >= 1,
        f"перенос длинного слова не сработал — нет токена с мягким переносом "
        f"(U+00AD); токены строки: {[w[5] for w in ws]}")

if hyph:
    # Самый правый перенос — кандидат на свисание.
    worst = max(hyph, key=lambda w: w[3])
    overshoot = worst[3] - RIGHT
    # ОСНОВНОЙ инвариант: дефис переноса НЕ заходит за правое поле.
    c.check("hyphen_within_right_margin",
            worst[3] <= RIGHT + TOL,
            f"дефис мягкого переноса свисает за правое поле: xMax={worst[3]:.3f} "
            f"> {RIGHT} на {overshoot:+.3f}pt (слово {worst[5].rstrip(chr(0x00ad))!r}-)")
    # Доп. диагностика: показать величину свеса даже если она в пределах.
    c.check("overshoot_reported",
            True,
            f"диагностика: overshoot={overshoot:+.3f}pt (xMax={worst[3]:.3f}, "
            f"граница {RIGHT})")
else:
    c.check("hyphen_within_right_margin", False, "нет переноса для замера свеса")

# Контроль: НЕ-переносные слова строк держатся в пределах поля (justify прижат
# к 552.76, не дальше) — отделяет баг переноса от общей поломки полей.
non_hyph_max = max((w[3] for w in ws if not w[5].endswith("­")), default=0.0)
c.check("regular_words_within_margin",
        non_hyph_max <= RIGHT + TOL,
        f"обычные слова тоже свисают (поля сломаны, не только перенос): "
        f"max xMax={non_hyph_max:.3f} > {RIGHT}")

c.done()
