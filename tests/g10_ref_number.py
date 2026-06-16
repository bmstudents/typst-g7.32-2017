"""g10: @-ссылка на рисунок печатает только номер; ссылка на формулу — номер в скобках."""
import re
import helpers as h

c = h.Checks("g10_ref_number")
pdf = h.compile("g10_ref_number.typ")
t = " ".join(h.text(pdf).split())

# Ссылка на рисунок: между маркерами должен быть только "1", без слова "рисунок".
m_fig = re.search(r"маркердо\s+(.+?)\s+маркерпосле", t)
fig_ref = m_fig.group(1) if m_fig else ""
c.check("fig_ref_is_number", fig_ref == "1",
        f"ссылка на рисунок = '{fig_ref}', ожидалось '1'")
c.check("fig_ref_no_word", "рисунок" not in fig_ref.lower(),
        f"ссылка содержит слово 'рисунок': '{fig_ref}'")

# Ссылка на блочную формулу: номер в скобках "(1)".
m_eq = re.search(r"формуладо\s+(.+?)\s+формулапосле", t)
eq_ref = m_eq.group(1) if m_eq else ""
c.check("eq_ref_in_parens", eq_ref == "(1)",
        f"ссылка на формулу = '{eq_ref}', ожидалось '(1)'")
c.done()
