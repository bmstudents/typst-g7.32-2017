"""pd struct-center: структурный '= ЗАКЛЮЧЕНИЕ' тоже по центру (другой структурный)."""
import helpers as h

c = h.Checks("pd_struct_center_zaklyuchenie")
pdf = h.compile("pd_struct_center_zaklyuchenie.typ")
ws = h.words(pdf)

z = [w for w in ws if w[5] == "ЗАКЛЮЧЕНИЕ"]
cx = 319.0

c.check("present",
        len(z) == 1,
        f"ждём одно слово ЗАКЛЮЧЕНИЕ, нашли: {z}")

if z:
    center = (z[0][1] + z[0][3]) / 2
    c.check("centered",
            abs(center - cx) < 15,
            f"центр ЗАКЛЮЧЕНИЕ {center:.1f}, ждём ~{cx} (±15)")
    # Не у левого поля 85 и не с абзацным отступом 120.
    c.check("not_left",
            z[0][1] > 150,
            f"ЗАКЛЮЧЕНИЕ слева x={z[0][1]:.1f}, ждём по центру")
else:
    c.check("centered", False, "нет ЗАКЛЮЧЕНИЕ")
    c.check("not_left", False, "нет ЗАКЛЮЧЕНИЕ")

c.done()
