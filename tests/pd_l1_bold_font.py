"""pd l1-bold-size: заголовок раздела жирный — в PDF встроен Bold-шрифт (pdffonts).

L1 в этом пакете 14pt (как и тело), поэтому отличие не в размере глифов, а в
жирном начертании. Проверяем, что подмножество Bold Times встроено наряду с
обычным начертанием тела.
"""
import subprocess
import helpers as h

c = h.Checks("pd_l1_bold_font")
pdf = h.compile("pd_l1_bold_font.typ")

fonts = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
low = fonts.lower()

c.check("bold_font_embedded",
        "bold" in low,
        f"в PDF нет жирного шрифта для заголовка:\n{fonts}")

c.check("regular_font_embedded",
        ("timesnewromanpsmt" in low) or ("times" in low and low.count("times") >= 2),
        f"нет обычного начертания тела:\n{fonts}")

# Заголовок и тело используют разные начертания (разные имена шрифтов).
names = [ln.split()[0] for ln in fonts.splitlines()
         if ln and not ln.startswith("name") and not ln.startswith("---")]
c.check("two_distinct_faces",
        len(set(names)) >= 2,
        f"ждём >=2 разных шрифта (жирный заголовок + обычное тело), нашли: {names}")

c.done()
