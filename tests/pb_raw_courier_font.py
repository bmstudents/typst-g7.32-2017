"""pb raw-courier: тело листинга набрано Courier New (моноширинный), а основной
текст — Times New Roman. Оба шрифта присутствуют в pdf (pdffonts)."""
import subprocess

import helpers as h

c = h.Checks("pb_raw_courier_font")
pdf = h.compile("pb_raw_courier_font.typ")

fonts = subprocess.run([h.PDFFONTS, pdf], capture_output=True, text=True).stdout
flat = fonts.replace(" ", "")

c.check("courier_present",
        "CourierNew" in flat,
        f"нет Courier New в шрифтах:\n{fonts}")

c.check("times_present",
        "TimesNewRoman" in flat,
        f"нет Times New Roman в шрифтах:\n{fonts}")

# Это два разных шрифта (код != основной текст).
c.check("two_distinct_fonts",
        "CourierNew" in flat and "TimesNewRoman" in flat,
        f"ожидаем оба шрифта одновременно:\n{fonts}")

c.done()
