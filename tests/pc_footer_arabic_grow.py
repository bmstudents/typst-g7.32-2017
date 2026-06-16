"""pc footer-arabic: номера '1','2','3' арабскими и монотонно растут."""
import helpers as h

c = h.Checks("pc_footer_arabic_grow")
pdf = h.compile("pc_footer_arabic_grow.typ")

f = [h.footer_word(pdf, p) for p in range(1, 4)]
c.check("exact_sequence", f == ["1", "2", "3"],
        f"футеры {f!r}, ждём ['1','2','3']")

# Арабские, не римские/буквенные: каждое целое и растёт на 1.
ints = [int(x) for x in f if x and x.isdigit()]
c.check("monotonic_plus_one",
        len(ints) == 3 and ints[1] == ints[0] + 1 and ints[2] == ints[1] + 1,
        f"числа {ints!r} не растут на 1")

c.done()
