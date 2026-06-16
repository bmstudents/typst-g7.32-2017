"""pf_toc_pagebreak_newpage: после оглавления идёт разрыв страницы — контент начинается на новой странице."""
import helpers as h

c = h.Checks("pf_toc_pagebreak_newpage")
pdf = h.compile("pf_toc_pagebreak_newpage.typ")

# Документ занимает минимум 2 страницы: страница оглавления + страница(ы) контента.
n = h.page_count(pdf)
c.check("multi_page", n >= 2, f"ожидалось >=2 страниц, найдено {n}")

# 'СОДЕРЖАНИЕ' (заголовок оглавления) — на странице 1.
toc_pages = {w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ"}
c.check("toc_on_page1", toc_pages == {1}, f"'СОДЕРЖАНИЕ' не только на стр.1: {toc_pages}")

# Заголовок первого раздела ('Раздел один') как РАЗДЕЛ (не запись оглавления) — на стр.2.
# На стр.1 'Раздел' встречается как запись оглавления; на стр.2 — как сам заголовок раздела.
razdel_pages = sorted({w[0] for w in h.words(pdf) if w[5] == "Раздел"})
c.check("section_starts_page2", 2 in razdel_pages and 1 in razdel_pages,
        f"раздел не появился на новой странице (2): страницы со словом 'Раздел' = {razdel_pages}")

# Первое слово страницы 2 — начало контента, а не запись оглавления (точек-заполнителей там нет).
p2_words = [w for w in h.words(pdf) if w[0] == 2]
c.check("page2_has_content", len(p2_words) > 0 and any(w[5] == "Раздел" for w in p2_words),
        f"на стр.2 нет заголовка раздела: {[w[5] for w in p2_words][:8]}")

c.done()
