"""pi п.4 listing-monospace: тело листинга моноширинное (равные x-шаги / Courier-шрифт)."""
import os
import subprocess
import helpers as h

c = h.Checks("pi_listing_monospace")
pdf = h.compile("pi_listing_monospace.typ")
ws = h.words(pdf)

# Две строки 'aaaa = 1111' и 'bbbb = 2222' — равное число символов.
# Слова 'aaaa' и 'bbbb' должны иметь одинаковый левый край (одна колонка)
# и одинаковую ширину (4 символа моноширинного шрифта).
a = [w for w in ws if w[5] == "aaaa"]
b = [w for w in ws if w[5] == "bbbb"]
c.check("both_lines", len(a) == 1 and len(b) == 1,
        f"не найдены обе строки кода: aaaa={a}, bbbb={b}")

if a and b:
    same_left = abs(a[0][1] - b[0][1]) < 0.5
    same_width = abs((a[0][3] - a[0][1]) - (b[0][3] - b[0][1])) < 0.5
    c.check("aligned_left", same_left,
            f"левые края строк не совпадают: aaaa.x0={a[0][1]}, bbbb.x0={b[0][1]}")
    c.check("equal_width", same_width,
            f"ширина 4-символьных слов различна: aaaa={a[0][3]-a[0][1]:.2f}, "
            f"bbbb={b[0][3]-b[0][1]:.2f} (не моноширинный)")
else:
    c.check("aligned_left", False, "нет строк для проверки")
    c.check("equal_width", False, "нет строк для проверки")

# Доп. подтверждение: pdffonts показывает моноширинный шрифт (Courier).
fonts = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
c.check("courier_font", "Courier" in fonts,
        f"моноширинный шрифт Courier не встроен:\n{fonts}")
c.done()
