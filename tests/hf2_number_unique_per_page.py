"""hf2: номер НЕ дублируется — ровно один номер в нижнем поле каждой страницы,
и каждое значение встречается во всём документе ровно один раз.
"""
import helpers as h

c = h.Checks("hf2_number_unique_per_page")
pdf = h.compile("hf2_number_unique_per_page.typ")

n = h.page_count(pdf)
c.check("three_pages", n == 3, f"страниц {n}, ждём 3")

all_footers = []
for p in range(1, n + 1):
    nums = [w for w in h.words(pdf) if w[0] == p and w[2] > 700 and w[5].isdigit()]
    # На странице ровно ОДИН номер в нижнем поле.
    c.check(f"p{p}_exactly_one_footer",
            len(nums) == 1,
            f"стр.{p}: номеров в нижнем поле {len(nums)}: {[w[5] for w in nums]}")
    if nums:
        all_footers.append(nums[0][5])

# Все номера документа уникальны (нет повторов одного значения на разных стр.).
c.check("footers_unique_across_doc",
        len(all_footers) == len(set(all_footers)),
        f"есть повторяющиеся номера страниц: {all_footers}")

c.done()
