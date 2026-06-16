"""pd num-section: '= Раздел' -> в тексте появляется '1 Раздел' с номером."""
import helpers as h

c = h.Checks("pd_num_section_basic")
pdf = h.compile("pd_num_section_basic.typ")
t = h.text(pdf)

c.check("section_numbered",
        "1 Раздел" in t,
        f"нет '1 Раздел' в тексте:\n{t[:300]!r}")

# Сам заголовок без номера ('Раздел' как отдельное слово после числа) тоже есть.
c.check("title_word_present",
        "Раздел" in t,
        f"нет слова 'Раздел':\n{t[:300]!r}")

c.done()
