"""pe_abstract_en: англ алиас #abstract даёт тот же заголовок 'Реферат'."""
import helpers as h

c = h.Checks("pe_abstract_en")
pdf = h.compile("pe_abstract_en.typ")
norm = " ".join(h.text(pdf).split())

c.check("heading_upper", "РЕФЕРАТ" in norm,
        f"нет 'РЕФЕРАТ' (англ алиас) в:\n{norm[:200]}")
c.check("heading_ci", "реферат" in norm.lower(),
        "нет заголовка 'Реферат' (без учёта регистра)")
c.done()
