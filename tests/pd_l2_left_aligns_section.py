"""pd l2-left: левый край подраздела (1.1) и пункта (1.1.1) совпадает с разделом (1) —
все заголовки в одной левой колонке, ни один не центрирован."""
import helpers as h

c = h.Checks("pd_l2_left_aligns_section")
pdf = h.compile("pd_l2_left_aligns_section.typ")
ws = [w for w in h.words(pdf) if w[0] == 1]
cx = 319.0

# Верхний '1' (номер раздела), '1.1', '1.1.1'.
sec = sorted([w for w in ws if w[5] == "1"], key=lambda t: t[2])
sub = [w for w in ws if w[5] == "1.1"]
pt = [w for w in ws if w[5] == "1.1.1"]

c.check("all_numbers_present",
        len(sec) >= 1 and len(sub) >= 1 and len(pt) >= 1,
        f"sec={sec[:1]} sub={sub} pt={pt}")

if sec and sub and pt:
    xs = [sec[0][1], sub[0][1], pt[0][1]]
    spread = max(xs) - min(xs)
    c.check("same_left_column",
            spread < 4,
            f"левые края разъезжаются: {[round(x,1) for x in xs]} (spread={spread:.1f})")
    c.check("all_left_of_center",
            all(x < cx - 80 for x in xs),
            f"какой-то заголовок близок к центру {cx}: {[round(x,1) for x in xs]}")
else:
    c.check("same_left_column", False, "нет всех номеров")
    c.check("all_left_of_center", False, "нет всех номеров")

c.done()
