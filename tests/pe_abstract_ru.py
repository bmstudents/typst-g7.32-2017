"""pe_abstract_ru: русский алиас #реферат даёт заголовок 'Реферат'."""
import helpers as h

c = h.Checks("pe_abstract_ru")
pdf = h.compile("pe_abstract_ru.typ")
norm = " ".join(h.text(pdf).split())

# 'Реферат' — структурный элемент из белого списка → верхний регистр.
c.check("heading_upper", "РЕФЕРАТ" in norm,
        f"нет 'РЕФЕРАТ' в:\n{norm[:200]}")
c.check("heading_ci", "реферат" in norm.lower(),
        "нет заголовка 'Реферат' (без учёта регистра)")
c.done()
