"""pd normal-section-left: контраст — структурный ВВЕДЕНИЕ по центру,
обычный раздел 'Анализ' заметно левее (выровнен влево)."""
import helpers as h

c = h.Checks("pd_normal_section_vs_struct")
pdf = h.compile("pd_normal_section_vs_struct.typ")
ws = h.words(pdf)
cx = 319.0

vv = [w for w in ws if w[5] == "ВВЕДЕНИЕ"]
an = [w for w in ws if w[5] == "Анализ"]

c.check("both_present",
        len(vv) == 1 and len(an) == 1,
        f"ВВЕДЕНИЕ={vv}, Анализ={an}")

if vv and an:
    vv_left = vv[0][1]
    an_left = an[0][1]
    # Структурный центрируется -> начинается значительно правее обычного.
    c.check("struct_centered",
            abs((vv[0][1] + vv[0][3]) / 2 - cx) < 15,
            f"ВВЕДЕНИЕ не по центру: cx_word={(vv[0][1]+vv[0][3])/2:.1f}")
    c.check("normal_left_of_struct",
            an_left < vv_left - 50,
            f"'Анализ' x={an_left:.1f} не заметно левее ВВЕДЕНИЕ x={vv_left:.1f}")
else:
    c.check("struct_centered", False, "нет слов")
    c.check("normal_left_of_struct", False, "нет слов")

c.done()
