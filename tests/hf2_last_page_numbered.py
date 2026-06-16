"""hf2: ПОСЛЕДНЯЯ страница тоже пронумерована (номер не пропадает в конце).
"""
import helpers as h

c = h.Checks("hf2_last_page_numbered")
pdf = h.compile("hf2_last_page_numbered.typ")

n = h.page_count(pdf)
c.check("four_pages", n == 4, f"страниц {n}, ждём 4")

last = h.footer_word(pdf, n)
c.check("last_page_has_number",
        last is not None and last.isdigit(),
        f"на последней стр.{n} нет числового футера: {last!r}")

c.check("last_page_number_equals_count",
        last == str(n),
        f"футер последней стр. = {last!r}, ждём {n!r}")

# В нижнем поле последней страницы действительно есть номер (а не только тело).
nums = [w for w in h.words(pdf) if w[0] == n and w[2] > 700 and w[5].isdigit()]
c.check("last_page_footer_in_field",
        len(nums) == 1 and nums[0][5] == str(n),
        f"в нижнем поле последней стр. ожидался номер {n}, найдено {[w[5] for w in nums]}")

c.done()
