"""g1: базовый текст — Times New Roman 14pt, первое слово на верхнем поле ≈56.25pt."""
import os
import subprocess

import helpers as h

c = h.Checks("g1_text_basics")
pdf = h.compile("g1_text_basics.typ")

# Первое слово сверху лежит на верхнем поле ~56.25pt (top margin 20мм).
fw = h.first_word(pdf, 1)
c.check("top_margin",
        fw is not None and abs(fw[0] - 56.25) < 3,
        f"верх первого слова y={None if fw is None else round(fw[0],2)}, ждём ~56.25")

# Шрифт основного текста — Times New Roman (через pdffonts).
fonts = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
c.check("font_times",
        "TimesNewRoman" in fonts.replace(" ", ""),
        f"нет TimesNewRoman в шрифтах:\n{fonts}")

# Кегль 14pt: высота глиф-бокса слова с выносными элементами ~12.7pt.
# Для 14pt Times это попадает в коридор 11.5–14pt; 12pt дал бы ~10.9.
ws = [w for w in h.words(pdf) if w[0] == 1]
box_h = max(w[4] - w[2] for w in ws)
c.check("size_14pt",
        12.0 <= box_h <= 14.0,
        f"высота бокса {box_h:.2f}pt вне коридора для 14pt (ждём 12.0–14.0)")

c.done()
