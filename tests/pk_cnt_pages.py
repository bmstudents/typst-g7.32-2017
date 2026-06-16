"""pk: #колво-страниц в многостраничном документе выводит число > 1."""
import re
import helpers as h

c = h.Checks("pk_cnt_pages")
pdf = h.compile("pk_cnt_pages.typ")
t = " ".join(h.text(pdf).split())

# Документ реально многостраничный (заголовки l1 начинают новую страницу).
n_pages = h.page_count(pdf)
c.check("doc_multipage", n_pages > 1,
        f"документ не многостраничный: страниц={n_pages}")

m = re.search(r"маркерстраниц\s+(\d+)\s+маркерстраниц", t)
val = int(m.group(1)) if m else None
c.check("counter_emitted", val is not None,
        f"маркер #колво-страниц не нашёлся в:\n{t[:200]}")
c.check("counter_gt_1", val is not None and val > 1,
        f"#колво-страниц = {val}, ожидалось > 1")
c.check("counter_matches_pages", val == n_pages,
        f"#колво-страниц = {val}, а реальных страниц {n_pages}")
c.done()
