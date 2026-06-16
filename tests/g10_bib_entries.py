"""g10: два источника рендерятся как пронумерованные записи 1. 2."""
import re
import helpers as h

c = h.Checks("g10_bib_entries")
pdf = h.compile("g10_bib_entries.typ")
t = " ".join(h.text(pdf).split())

c.check("both_authors", "Кузнецов" in t and "Морозова" in t,
        f"нет обоих авторов в:\n{t[:500]}")

# Нумерация записей "1." и "2." в списке.
c.check("numbering",
        re.search(r"1\.\s*Кузнецов", t) is not None
        and re.search(r"2\.\s*Морозова", t) is not None,
        "нет нумерации '1. Кузнецов' / '2. Морозова'")

c.check("two_pages_min", h.page_count(pdf) >= 1, "документ пуст")
c.done()
