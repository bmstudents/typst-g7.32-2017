"""pa_flag-hyphenate-on (аспект 2): значение по умолчанию совпадает с явным 'да'.
Документ без флага и документ с фича-переносы-слов=да дают одинаковое число
строк-фрагментов узкого box — значит по умолчанию перенос включён (да)."""
import helpers as h

c = h.Checks("pa_hyphenate_on_default")
pdf_default = h.compile("pa_hyphenate_on.typ")            # без флага
pdf_explicit = h.compile("pa_hyphenate_on_default.typ")  # явно да


def n_lines(pdf):
    return len([l for l in h.text(pdf).splitlines()
                if l.strip() and not l.strip().isdigit()])


nd = n_lines(pdf_default)
ne = n_lines(pdf_explicit)

c.check("default_hyphenates", nd > 1, f"по умолчанию слово не перенесено: строк={nd}")
c.check("default_equals_explicit_da", nd == ne,
        f"умолчание != явное да: default={nd} explicit_da={ne}")
c.done()
