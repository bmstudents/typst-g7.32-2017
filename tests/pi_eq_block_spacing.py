"""pi п.11 eq-block-spacing: блочная формула имеет вертикальный зазор сверху/снизу
больше обычного межстрочного шага (above 2.5em / below 1em в стиле eq)."""
import helpers as h

c = h.Checks("pi_eq_block_spacing")
pdf = h.compile("pi_eq_block_spacing.typ")
ws = h.words(pdf)


def y(word):
    hits = [w for w in ws if w[5] == word]
    return hits[0][2] if hits else None


y_before = y("СтрокаДоФормулыМаркер")
y_after = y("СтрокаПослеФормулыМаркер")
y_after2 = y("Ещё")
y_eq = y("=")  # знак равенства внутри формулы

c.check("anchors_found",
        None not in (y_before, y_after, y_after2, y_eq),
        f"не найдены опорные слова: before={y_before}, after={y_after}, "
        f"after2={y_after2}, eq={y_eq}")

if None not in (y_before, y_after, y_after2, y_eq):
    base_step = y_after2 - y_after          # обычный межстрочный шаг (абзац)
    gap_above = y_eq - y_before             # зазор от текста до формулы
    gap_below = y_after - y_eq              # зазор от формулы до текста

    c.check("gap_above_larger", gap_above > base_step * 1.3,
            f"зазор над формулой {gap_above:.1f} не превышает обычный шаг "
            f"{base_step:.1f}*1.3 — нет вертикального отступа сверху")
    c.check("gap_below_larger", gap_below > base_step * 1.3,
            f"зазор под формулой {gap_below:.1f} не превышает обычный шаг "
            f"{base_step:.1f}*1.3 — нет вертикального отступа снизу")
else:
    c.check("gap_above_larger", False, "нет опорных слов")
    c.check("gap_below_larger", False, "нет опорных слов")
c.done()
