"""pb font-size-14: высота глиф-бокса строки соответствует 14pt Times.
Слова с верхними и нижними выносными дают ~12.7pt (для 12pt было бы ~10.9)."""
import helpers as h

c = h.Checks("pb_font_size14_box")
pdf = h.compile("pb_font_size14_box.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 700]

box_h = max(w[4] - w[2] for w in ws)
c.check("box_height_14pt",
        12.0 <= box_h <= 14.0,
        f"высота бокса {box_h:.2f}pt вне коридора для 14pt (ждём 12.0–14.0)")

# Явно больше, чем дал бы кегль 12pt (~10.9pt).
c.check("bigger_than_12pt",
        box_h > 11.5,
        f"высота {box_h:.2f}pt слишком мала — похоже на 12pt, а не 14pt")

c.done()
