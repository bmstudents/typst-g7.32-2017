"""hd2: ссылка ВПЕРЁД на рисунок (раньше объекта в тексте) и НАЗАД — обе '2'.

Инвариант: @f2 указанная до определения рисунка f2 даёт тот же номер, что и
после; оба равны '2'.
"""
import re
import helpers as h

c = h.Checks("hd2_ref_forward_fig")
pdf = h.compile("hd2_ref_forward_fig.typ")
t = " ".join(h.text(pdf).split())


def ref(pre, post):
    m = re.search(re.escape(pre) + r"\s+(.+?)\s+" + re.escape(post), t)
    return m.group(1) if m else "<нет>"


fwd = ref("впердо", "верпосле")
bwd = ref("наздо", "назпосле")

c.check("ref_forward_is_2", fwd == "2", f"ссылка вперёд = '{fwd}', ожидалось '2'")
c.check("ref_backward_is_2", bwd == "2", f"ссылка назад = '{bwd}', ожидалось '2'")
c.check("ref_fwd_eq_bwd", fwd == bwd,
        f"вперёд '{fwd}' != назад '{bwd}' для одного рисунка")

c.done()
