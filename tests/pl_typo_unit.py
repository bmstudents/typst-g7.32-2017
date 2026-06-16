"""pl point 12: связка 'число + единица' ('45 Гц') не рвётся переносом.
Функциональная проверка по координатам: в узком box 40pt '45' и 'Гц' на
одной строке (одинаковый yMin), а предшествующее 'яяя' — на строке выше
(доказывает, что перенос был возможен, но связка 45+Гц осталась цельной)."""
import helpers as h

c = h.Checks("pl_typo_unit")
pdf = h.compile("pl_typo_unit.typ")
ws = [w for w in h.words(pdf) if not (w[5].isdigit() and w[2] > 700)]

n45 = next((w for w in ws if w[5] == "45"), None)
гц = next((w for w in ws if w[5] == "Гц"), None)
яяя = next((w for w in ws if w[5] == "яяя"), None)

c.check("all_present", n45 is not None and гц is not None and яяя is not None,
        f"нет '45'/'Гц'/'яяя': {[w[5] for w in ws]}")
if n45 and гц and яяя:
    c.check("value_unit_same_line", abs(n45[2] - гц[2]) < 1.0,
            f"'45' и 'Гц' на разных строках: yMin 45={n45[2]:.1f} Гц={гц[2]:.1f}")
    c.check("wrapped_as_unit", n45[2] > яяя[2] + 1.0,
            f"перенос не сработал (связка не отдельной строкой): "
            f"yMin яяя={яяя[2]:.1f} 45={n45[2]:.1f}")
else:
    c.check("value_unit_same_line", False, "нет слов для проверки")
    c.check("wrapped_as_unit", False, "нет слов для проверки")
c.done()
