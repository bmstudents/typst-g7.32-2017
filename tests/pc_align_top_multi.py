"""pc align-top: на обеих страницах контент стартует от верхнего поля (yMin≈56.25)."""
import helpers as h

c = h.Checks("pc_align_top_multi")
pdf = h.compile("pc_align_top_multi.typ")
top_margin = 56.25

for p in range(1, 3):
    fw = h.first_word(pdf, p)
    c.check(f"page{p}_top",
            fw is not None and abs(fw[0] - top_margin) < 10,
            f"стр.{p}: yMin первого слова {fw[0] if fw else None}, ждём ≈{top_margin}±10")

# Верх не "плавает" вниз: первое слово в верхней четверти листа.
fw1 = h.first_word(pdf, 1)
c.check("not_vertically_centered",
        fw1 is not None and fw1[0] < 841.89 / 4,
        f"первое слово на y={fw1[0] if fw1 else None}, ждём в верхней четверти (<210)")

c.done()
