"""pd struct-no-number: '= ВВЕДЕНИЕ' без числового префикса (нет '1 ВВЕДЕНИЕ')."""
import helpers as h

c = h.Checks("pd_struct_nonumber_basic")
pdf = h.compile("pd_struct_nonumber_basic.typ")
t = h.text(pdf)
ws = h.words(pdf)

c.check("vvedenie_present",
        "ВВЕДЕНИЕ" in t,
        f"нет 'ВВЕДЕНИЕ' в:\n{t[:300]!r}")

c.check("no_number_prefix",
        "1 ВВЕДЕНИЕ" not in t and "1ВВЕДЕНИЕ" not in t,
        f"ВВЕДЕНИЕ пронумеровано:\n{t[:300]!r}")

# Перед словом ВВЕДЕНИЕ на той же строке нет слова-числа.
vv = [w for w in ws if w[5] == "ВВЕДЕНИЕ"]
if vv:
    y = vv[0][2]
    same_line_left = [w for w in ws if w[0] == vv[0][0] and abs(w[2] - y) < 3
                      and w[1] < vv[0][1] and w[5].rstrip(".").isdigit()]
    c.check("no_number_left_of_heading",
            len(same_line_left) == 0,
            f"слева от ВВЕДЕНИЕ есть число: {same_line_left}")
else:
    c.check("no_number_left_of_heading", False, "нет ВВЕДЕНИЕ")

c.done()
