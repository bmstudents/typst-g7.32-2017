"""g1: нумерация страниц — арабские цифры внизу по центру, растут по страницам."""
import helpers as h

c = h.Checks("g1_page_numbering")
pdf = h.compile("g1_page_numbering.typ")

c.check("three_pages", h.page_count(pdf) == 3, f"страниц {h.page_count(pdf)}, ждём 3")

f1, f2, f3 = h.footer_word(pdf, 1), h.footer_word(pdf, 2), h.footer_word(pdf, 3)
# Нижнее слово каждой страницы — это её номер (арабская цифра).
c.check("footer_is_number",
        f1.isdigit() and f2.isdigit() and f3.isdigit(),
        f"футеры не числа: {f1!r} {f2!r} {f3!r}")

c.check("footer_grows",
        f2 == "2" and f3 == "3",
        f"номера не растут: стр2={f2!r} стр3={f3!r}")

# Номер внизу по центру текстового поля (между полями 30мм/15мм):
# центр поля = (85.04 + 552.76)/2 ≈ 318.9pt. Это и есть "по центру" по ГОСТ.
nums = [w for w in h.words(pdf) if w[0] == 2 and w[5] == "2"]
# самый нижний "2" — это футер
foot = max(nums, key=lambda t: t[2])
cx = (foot[1] + foot[3]) / 2
content_center = (85.04 + (595.276 - 42.52)) / 2
c.check("footer_centered",
        abs(cx - content_center) < 15,
        f"центр номера x={cx:.1f}, ждём ~{content_center:.1f} (центр текст. поля)")

# И номер действительно внизу страницы (ниже середины листа по Y).
c.check("footer_at_bottom",
        foot[2] > 841.89 / 2,
        f"номер на y={foot[2]:.1f}, ждём в нижней половине листа (>420.9)")

c.done()
