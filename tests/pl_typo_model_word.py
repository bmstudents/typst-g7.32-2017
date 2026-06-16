"""pl point 15: название модели не отрывается от предшествующего слова —
'драйвер L298N' держатся на одной строке (неразрывная связка). Box 95pt:
'ааааааааа' уходит на строку выше, 'драйвер' и 'L298N' имеют одинаковый
yMin (одна строка). Без флага typst рвал бы 'драй-вер'/'L298N'."""
import helpers as h

c = h.Checks("pl_typo_model_word")
pdf = h.compile("pl_typo_model_word.typ")
ws = [w for w in h.words(pdf) if not (w[5].isdigit() and w[2] > 700)]

драйвер = next((w for w in ws if w[5] == "драйвер"), None)
модель = next((w for w in ws if w[5] == "L298N"), None)
филлер = next((w for w in ws if w[5] == "ааааааааа"), None)

c.check("both_present", драйвер is not None and модель is not None,
        f"нет 'драйвер'/'L298N' (возможно перенос 'драй-вер'): {[w[5] for w in ws]}")
if драйвер and модель:
    c.check("word_model_same_line", abs(драйвер[2] - модель[2]) < 1.0,
            f"'драйвер' и 'L298N' на разных строках: "
            f"yMin драйвер={драйвер[2]:.1f} L298N={модель[2]:.1f}")
    # связка реально перенеслась целиком: филлер выше связки
    if филлер:
        c.check("wrapped_as_pair", драйвер[2] > филлер[2] + 1.0,
                f"перенос не сработал: yMin филлер={филлер[2]:.1f} драйвер={драйвер[2]:.1f}")
    else:
        c.check("wrapped_as_pair", False, "нет филлера для проверки переноса")
else:
    c.check("word_model_same_line", False, "нет слов для проверки")
    c.check("wrapped_as_pair", False, "нет слов для проверки")
c.done()
