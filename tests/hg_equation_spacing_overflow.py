"""Отступ формулы не перетекает на новую страницу, когда сама формула
осталась на предыдущей.

Сценарий (#v(664pt)): блочная формула влезает в КОНЕЦ страницы 1, а текст
после неё уходит на страницу 2. Текст на стр.2 обязан начинаться от верхнего
поля (yMin ≈ 56.25). Баг: нижний отступ формулы (block(below:1em) +
невидимый #par[#hide[...]]-костыль в styles/eq.typ) не схлопывается на стыке
и перетекает в начало стр.2, сдвигая текст вниз (наблюдалось yMin≈80.7,
+24.45pt пустого отступа)."""
import helpers as h

TOP = 56.25

c = h.Checks("hg_equation_spacing_overflow")
pdf = h.compile("hg_equation_spacing_overflow.typ")

ws = h.words(pdf)
eq = [w for w in ws if w[5] in ("E", "𝐸")]
post = [w for w in ws if "ОСЛЕТЕКСТ" in w[5]]

c.check("equation_on_page1", bool(eq) and eq[0][0] == 1,
        f"формула не на стр.1: {[(w[0], w[5]) for w in eq]}")
c.check("text_on_page2", bool(post) and post[0][0] == 2,
        f"текст после не на стр.2: {[(w[0], w[5]) for w in post]}")
if post and post[0][0] == 2:
    y = post[0][2]
    c.check("no_leaked_spacing_on_page2", abs(y - TOP) <= 6,
            f"текст на стр.2 начинается с yMin={y:.1f}, ожидалось ≈{TOP}: "
            f"отступ формулы перетёк на стр.2 (+{y - TOP:.1f}pt пустоты). "
            f"styles/eq.typ — below:1em + #par[#hide] не схлопываются на стыке.")
c.done()
