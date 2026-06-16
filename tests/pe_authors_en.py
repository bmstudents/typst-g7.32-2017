"""pe_authors_en: англ алиас #authors_list даёт тот же заголовок 'Список исполнителей'."""
import helpers as h

c = h.Checks("pe_authors_en")
pdf = h.compile("pe_authors_en.typ")
norm = " ".join(h.text(pdf).split())

c.check("heading_upper", "СПИСОК ИСПОЛНИТЕЛЕЙ" in norm,
        f"нет 'СПИСОК ИСПОЛНИТЕЛЕЙ' (англ алиас) в:\n{norm[:200]}")
c.check("heading_ci", "список исполнителей" in norm.lower(),
        "нет заголовка 'Список исполнителей' (без учёта регистра)")
c.done()
