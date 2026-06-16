"""pf_toc_includes_sections: нумерованные разделы появляются записями оглавления с номерами 1,2,3 и номером страницы."""
import helpers as h

c = h.Checks("pf_toc_includes_sections")
pdf = h.compile("pf_toc_includes_sections.typ")
t = h.text(pdf)

# Каждый раздел представлен записью с его номером.
c.check("entry_1", "1 Раздел один" in t, "нет записи '1 Раздел один'")
c.check("entry_2", "2 Раздел два" in t, "нет записи '2 Раздел два'")
c.check("entry_3", "3 Раздел три" in t, "нет записи '3 Раздел три'")

# На странице оглавления три строки записей разделов (по слову 'Раздел').
toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
ys = sorted({round(w[2], 0) for w in h.words(pdf) if w[0] == toc_page and w[5] == "Раздел"})
c.check("three_entry_lines", len(ys) == 3,
        f"ожидалось 3 строки разделов, найдено {len(ys)}: {ys}")

# У каждой строки записи есть числовой номер страницы у правого края.
for i, y in enumerate(ys, 1):
    line = [w for w in h.words(pdf) if w[0] == toc_page and abs(w[2] - y) < 1.0]
    rightmost = max(line, key=lambda w: w[3])
    c.check(f"page_no_line_{i}", rightmost[5].isdigit() and rightmost[3] > 540,
            f"строка {i}: правый элемент не номер страницы: {rightmost[5]!r} x1={rightmost[3]:.1f}")

c.done()
