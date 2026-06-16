"""pd struct-center: структурный '= ВВЕДЕНИЕ' выровнен по центру текстового поля."""
import helpers as h

c = h.Checks("pd_struct_center_vvedenie")
pdf = h.compile("pd_struct_center_vvedenie.typ")
ws = h.words(pdf)

vv = [w for w in ws if w[5] == "ВВЕДЕНИЕ"]
cx = 319.0  # центр текстового поля (85.04 .. 552.76)

c.check("vvedenie_present",
        len(vv) == 1,
        f"ждём одно слово ВВЕДЕНИЕ, нашли: {vv}")

if vv:
    center = (vv[0][1] + vv[0][3]) / 2
    c.check("centered",
            abs(center - cx) < 15,
            f"центр ВВЕДЕНИЕ {center:.1f}, ждём ~{cx} (±15)")
    c.check("not_at_left_margin",
            vv[0][1] > 150,
            f"ВВЕДЕНИЕ начинается у левого поля x={vv[0][1]:.1f} (должно быть по центру)")
else:
    c.check("centered", False, "нет ВВЕДЕНИЕ")
    c.check("not_at_left_margin", False, "нет ВВЕДЕНИЕ")

c.done()
