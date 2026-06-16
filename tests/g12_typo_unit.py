"""g12_typo_unit: связка 'число единица' ('45 Гц') не рвётся переносом строки.
Функциональная проверка (poppler нормализует nbsp → пробел, проверяем по
координатам): в узком box '45' и 'Гц' на одной строке (одинаковый yMin),
а предшествующее 'яяя' — на строке выше (доказывает, что перенос был возможен,
но именно связка 45+Гц осталась цельной)."""
import helpers as h

c = h.Checks("g12_typo_unit")
pdf = h.compile("g12_typo_unit.typ")
ws = [w for w in h.words(pdf) if not (w[5].isdigit() and w[2] > 700)]  # без футера-номера

n45 = next((w for w in ws if w[5] == "45"), None)
гц = next((w for w in ws if w[5] == "Гц"), None)
яяя = next((w for w in ws if w[5] == "яяя"), None)

c.check("all_present", n45 is not None and гц is not None and яяя is not None,
        f"нет '45'/'Гц'/'яяя': {[w[5] for w in ws]}")

if n45 and гц and яяя:
    # 45 и Гц на одной строке
    c.check("value_unit_same_line", abs(n45[2] - гц[2]) < 1.0,
            f"'45' и 'Гц' на разных строках: yMin 45={n45[2]:.1f} Гц={гц[2]:.1f}")
    # связка реально перенеслась целиком: 'яяя' выше, чем '45 Гц'
    c.check("wrapped_as_unit", n45[2] > яяя[2] + 1.0,
            f"перенос не сработал (связка не на отдельной строке): "
            f"yMin яяя={яяя[2]:.1f} 45={n45[2]:.1f}")
else:
    c.check("value_unit_same_line", False, "нет слов для проверки")
    c.check("wrapped_as_unit", False, "нет слов для проверки")

c.done()
