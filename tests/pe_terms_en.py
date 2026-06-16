"""pe_terms_en: англ алиас #terms_and_definitions даёт тот же 'Термины и определения'."""
import helpers as h

c = h.Checks("pe_terms_en")
pdf = h.compile("pe_terms_en.typ")
norm = " ".join(h.text(pdf).split())

c.check("heading_upper", "ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ" in norm,
        f"нет 'ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ' (англ алиас) в:\n{norm[:200]}")
c.check("heading_ci", "термины и определения" in norm.lower(),
        "нет заголовка 'Термины и определения' (без учёта регистра)")
c.done()
