"""hd2: @ref на формулу даёт '(N)'. Вторая формула -> '(2)'. Ссылка вперёд верна.

Инвариант: ссылка на блочную формулу печатается как номер в скобках,
совпадает с номером справа от формулы; ссылка вперёд (раньше объекта в
тексте) даёт верный номер.
"""
import re
import helpers as h

c = h.Checks("hd2_ref_equations")
pdf = h.compile("hd2_ref_equations.typ")
t = " ".join(h.text(pdf).split())


def ref(pre, post):
    m = re.search(re.escape(pre) + r"\s+(.+?)\s+" + re.escape(post), t)
    return m.group(1) if m else "<нет>"


fwd = ref("фвпердо", "фвперпосле")   # ссылка вперёд на eq2
r1 = ref("ф1до", "ф1после")
r2 = ref("ф2до", "ф2после")

c.check("ref_eq1_parens", r1 == "(1)", f"ссылка на формулу1 = '{r1}', ожидалось '(1)'")
c.check("ref_eq2_parens", r2 == "(2)", f"ссылка на формулу2 = '{r2}', ожидалось '(2)'")
c.check("ref_forward_eq2", fwd == "(2)",
        f"ссылка вперёд на формулу2 = '{fwd}', ожидалось '(2)'")
c.check("ref_forward_eq_match", fwd == r2,
        f"ссылка вперёд '{fwd}' != ссылка назад '{r2}' на ту же формулу")

c.done()
