"""g9: context-счётчики выводят число (2 рисунка) и колво-страниц > 0."""
import re
import helpers as h

c = h.Checks("g9_counters")
pdf = h.compile("g9_counters.typ")
t = " ".join(h.text(pdf).split())

m_fig = re.search(r"маркеррисунков\s+(\d+)\s+маркеррисунков", t)
c.check("figures_count", m_fig is not None and int(m_fig.group(1)) == 2,
        f"колво-рисунков != 2 (текст: {t[:200]})")

m_pg = re.search(r"маркерстраниц\s+(\d+)\s+маркерстраниц", t)
c.check("pages_positive", m_pg is not None and int(m_pg.group(1)) > 0,
        f"колво-страниц не положительно (текст: {t[:200]})")

c.check("two_figures_rendered",
        "Рисунок 1" in t and "Рисунок 2" in t,
        "в документе нет двух рисунков")
c.done()
