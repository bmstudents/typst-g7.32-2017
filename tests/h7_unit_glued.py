"""h7_unit_glued: связка «число + единица измерения» («100 МГц») не рвётся
переносом строки (флаг неразрывных величин).

Ширина box (44pt) подобрана компиляцией: БЕЗ флага '100' и 'МГц' распадаются
на две строки (yMin 56.3 / 80.4); С флагом '100 МГц' заворачивается одной
связкой — '100' и 'МГц' на одном yMin, а 'ттт' на строке выше (доказывает,
что перенос был возможен, но связка осталась цельной). Проверка
ФУНКЦИОНАЛЬНАЯ (poppler нормализует nbsp → пробел).
"""
import helpers as h

c = h.Checks("h7_unit_glued")
pdf = h.compile("h7_unit_glued.typ")
ws = [w for w in h.words(pdf) if not (w[5].isdigit() and w[2] > 700)]

n100 = next((w for w in ws if w[5] == "100"), None)
мгц = next((w for w in ws if w[5] == "МГц"), None)
ттт = next((w for w in ws if w[5] == "ттт"), None)

c.check("all_present", all(x is not None for x in (n100, мгц, ттт)),
        f"нет '100'/'МГц'/'ттт': {[w[5] for w in ws]}")

if n100 and мгц and ттт:
    # '100' и 'МГц' на одной строке.
    c.check("value_unit_same_line",
            abs(n100[2] - мгц[2]) < 0.5,
            f"'100' и 'МГц' на разных строках: yMin 100={n100[2]:.3f} "
            f"МГц={мгц[2]:.3f}")
    # Связка реально перенеслась целиком — 'ттт' на строке ВЫШЕ.
    c.check("wrapped_as_whole_unit",
            n100[2] > ттт[2] + 1.0,
            f"перенос связки не сработал: yMin ттт={ттт[2]:.3f} 100={n100[2]:.3f} "
            f"(ждём 100 ниже ттт)")
    # Единица стоит сразу справа от числа (порядок и смежность сохранены).
    c.check("unit_right_of_value",
            мгц[1] > n100[3] - 0.5,
            f"'МГц' не справа от '100': xMax 100={n100[3]:.2f} xMin МГц={мгц[1]:.2f}")
else:
    c.check("value_unit_same_line", False, "нет слов")
    c.check("wrapped_as_whole_unit", False, "нет слов")
    c.check("unit_right_of_value", False, "нет слов")

c.done()
