"""pe_terms_ru: русский алиас #термины_и_определения даёт 'Термины и определения'."""
import helpers as h

c = h.Checks("pe_terms_ru")
pdf = h.compile("pe_terms_ru.typ")
norm = " ".join(h.text(pdf).split())

# Структурный элемент из белого списка → рендерится капсом.
c.check("heading_upper", "ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ" in norm,
        f"нет 'ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ' в:\n{norm[:200]}")
c.check("heading_ci", "термины и определения" in norm.lower(),
        "нет заголовка 'Термины и определения' (без учёта регистра)")
c.done()
