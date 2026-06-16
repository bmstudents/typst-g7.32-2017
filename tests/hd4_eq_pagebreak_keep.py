"""hd4 РАЗРЫВ СТРАНИЦЫ: формулу выталкивают #v(660pt) на следующую страницу.
Тело формулы и её номер (1) должны оказаться на ОДНОЙ странице (номер не
отрывается от тела). Также номер должен быть ровно один.
"""
import re
import helpers as h

c = h.Checks("hd4_eq_pagebreak_keep")
pdf = h.compile("hd4_eq_pagebreak_keep.typ")
ws = h.words(pdf)
t = " ".join(h.text(pdf).split())

# Ровно один номер формулы.
nums = re.findall(r"\((\d+)\)", t)
c.check("single_number",
        nums == ["1"],
        f"ожидали единственный номер [1], получили {nums}")

# Страница номера (1).
num_pages = sorted({w[0] for w in ws if w[5] == "(1)"})
# Страница тела формулы: ищем символ '=' (часть формулы) или 'E'.
body_pages = sorted({w[0] for w in ws if w[5] in ("=", "𝐸", "E") or "𝑚" in w[5]})

c.check("number_present",
        len(num_pages) == 1,
        f"номер '(1)' найден на страницах {num_pages}")

c.check("body_present",
        len(body_pages) >= 1,
        f"тело формулы не найдено в bbox; слова: {[w[5] for w in ws]}")

c.check("number_with_body_same_page",
        len(num_pages) == 1 and len(body_pages) >= 1 and num_pages[0] in body_pages,
        f"номер '(1)' на стр.{num_pages}, тело на стр.{body_pages} — "
        f"номер оторвался от тела формулы при разрыве страницы")

c.done()
