"""xc_equation_at_boundary: блочная формула вытолкнута #v к низу страницы.
Граничные проверки:
  1) формула не разрывается между страницами — все её компоненты (sum, x, y,
     пределы n / i=1) на ОДНОЙ странице;
  2) номер «(1)» на той же странице, что и тело формулы (а не оторван);
  3) текст после формулы идёт следом за ней (на той же или последующей
     странице, не выше формулы).
"""
import helpers as h

c = h.Checks("xc_equation_at_boundary")
pdf = h.compile("xc_equation_at_boundary.typ")

ws = h.words(pdf)

# компоненты формулы: символы математики (юникод-варианты) + '=' и пределы
eq_glyphs = {"=", "𝑥", "𝑦", "𝑛", "∑", "𝑖", "𝑖=1"}
eq_words = [w for w in ws if w[5] in eq_glyphs]
eq_pages = sorted({w[0] for w in eq_words})

c.check(
    "eq_found",
    len(eq_words) >= 4,
    f"не нашли тело формулы в текстовом слое: {[w[5] for w in eq_words]}",
)

# 1) тело формулы целиком на одной странице (не разорвано)
c.check(
    "eq_not_split",
    len(eq_pages) == 1,
    f"тело формулы разорвано между страницами {eq_pages}: {[(w[0],w[5]) for w in eq_words]}",
)

# 2) номер (1) на той же странице, что и тело
num = [w for w in ws if w[5] == "(1)"]
num_pages = sorted({w[0] for w in num})
c.check(
    "number_present",
    len(num) == 1,
    f"номер формулы '(1)' не найден ровно один раз: {num}",
)
c.check(
    "number_same_page_as_body",
    len(num_pages) == 1 and len(eq_pages) == 1 and num_pages[0] == eq_pages[0],
    f"номер (1) на стр.{num_pages}, тело формулы на стр.{eq_pages} — оторван",
)

# 3) текст после формулы идёт ниже неё на той же странице (или дальше)
after = [w for w in ws if w[5] == "формулы."]
after = [w for w in after if w[0] >= 2] or after  # "Текст сразу после формулы."
eq_y = max(w[4] for w in eq_words) if eq_words else None  # низ формулы (yMax)
eq_pg = eq_pages[0] if len(eq_pages) == 1 else None
after_after = [w for w in after if w[0] == eq_pg]
c.check(
    "text_after_below_eq",
    eq_pg is not None and after_after and min(a[2] for a in after_after) > eq_y,
    f"текст 'формулы.' не следует под формулой (низ формулы yMax={eq_y}, "
    f"текст={[(a[0], round(a[2],1)) for a in after]})",
)

c.done()
