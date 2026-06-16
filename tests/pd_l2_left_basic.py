"""pd l2-left: подраздел '1.1 Подраздел' выровнен влево (левая зона, не по центру)."""
import helpers as h

c = h.Checks("pd_l2_left_basic")
pdf = h.compile("pd_l2_left_basic.typ")
ws = h.words(pdf)
cx = 319.0

# Номер подраздела '1.1'.
num = [w for w in ws if w[5] == "1.1"]
title = [w for w in ws if w[5] == "Подраздел"]

c.check("subsection_number_present",
        len(num) >= 1,
        f"нет номера '1.1': {num}")

c.check("subsection_title_present",
        len(title) >= 1,
        f"нет 'Подраздел': {title}")

if num:
    nx = num[0][1]
    c.check("left_zone",
            nx < 130,
            f"номер подраздела x={nx:.1f}, ждём левую зону (<130)")
    c.check("not_centered",
            nx < cx - 80,
            f"номер подраздела x={nx:.1f} слишком близко к центру {cx}")
else:
    c.check("left_zone", False, "нет номера")
    c.check("not_centered", False, "нет номера")

c.done()
