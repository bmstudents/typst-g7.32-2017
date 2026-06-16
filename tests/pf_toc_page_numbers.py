"""pf_toc_page_numbers: у каждой записи оглавления справа стоит номер страницы (число, xMax > 540)."""
import helpers as h
from collections import defaultdict

c = h.Checks("pf_toc_page_numbers")
pdf = h.compile("pf_toc_page_numbers.typ")

toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
toc = [w for w in h.words(pdf) if w[0] == toc_page]

# Группируем по строкам; строки-записи — те, что содержат слово 'Раздел' или 'Подраздел'.
lines = defaultdict(list)
for w in toc:
    lines[round(w[2], 0)].append(w)

entry_ys = [y for y, ws in lines.items()
            if any(x[5] in ("Раздел", "Подраздел") for x in ws)]
c.check("entries_found", len(entry_ys) >= 3,
        f"ожидалось >=3 записи (2 раздела + подраздел), найдено {len(entry_ys)}")

# Каждая запись завершается числом у правого края (x > 540).
all_have_pageno = True
detail = ""
for y in entry_ys:
    rightmost = max(lines[y], key=lambda w: w[3])
    if not (rightmost[5].isdigit() and rightmost[3] > 540):
        all_have_pageno = False
        detail = f"строка y={y}: правый='{rightmost[5]}' x1={rightmost[3]:.1f}"
        break
c.check("each_entry_has_pageno_right", all_have_pageno,
        f"не у каждой записи номер страницы справа: {detail}")

# Номера страниц монотонно не убывают сверху вниз (раздел2 на стр >= подраздела).
nums = []
for y in sorted(entry_ys):
    rightmost = max(lines[y], key=lambda w: w[3])
    if rightmost[5].isdigit():
        nums.append(int(rightmost[5]))
c.check("page_numbers_nondecreasing", nums == sorted(nums) and len(nums) >= 3,
        f"номера страниц не по возрастанию: {nums}")

c.done()
