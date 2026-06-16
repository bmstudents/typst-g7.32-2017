"""xc_list_across_pages: нумерованный список 40 пунктов через границу страницы.
Граничные проверки:
  1) все 40 пунктов присутствуют;
  2) нумерация сквозная и последовательная 1..40 (по порядку появления);
  3) список реально пересекает границу — пункты есть минимум на 2 страницах;
  4) на 2-й странице списка нумерация НЕ сбрасывается на 1 (первый пункт
     2-й страницы продолжает счёт, его номер > числа пунктов 1-й страницы).
"""
import re
import helpers as h

c = h.Checks("xc_list_across_pages")
pdf = h.compile("xc_list_across_pages.typ")
ws = h.words(pdf)

# токены вида 'N)' — это маркеры пунктов enum
items = [(int(w[5][:-1]), w[0], w[2]) for w in ws if re.fullmatch(r"\d+\)", w[5])]
nums = [it[0] for it in items]

c.check("all_40_items", len(items) == 40, f"ожидали 40 пунктов, нашли {len(items)}: {nums}")

c.check(
    "sequential_1_to_40",
    nums == list(range(1, 41)),
    f"нумерация не сквозная/не по порядку: {nums}",
)

item_pages = sorted({it[1] for it in items})
c.check(
    "crosses_page_boundary",
    len(item_pages) >= 2,
    f"список не пересёк границу страницы — пункты только на {item_pages}",
)

# 4) первый пункт первой «продолжающей» страницы не равен 1 (нет сброса)
first_page = item_pages[0]
n_on_first = sum(1 for it in items if it[1] == first_page)
second_page = item_pages[1] if len(item_pages) >= 2 else None
# самый верхний пункт второй страницы
sp_items = sorted([it for it in items if it[1] == second_page], key=lambda t: t[2])
first_num_on_second = sp_items[0][0] if sp_items else None
c.check(
    "no_reset_on_page2",
    first_num_on_second is not None and first_num_on_second == n_on_first + 1,
    f"нумерация сбилась на разрыве: на стр.{first_page} было {n_on_first} пунктов, "
    f"первый пункт стр.{second_page} = {first_num_on_second} (ожидали {n_on_first + 1})",
)

c.done()
