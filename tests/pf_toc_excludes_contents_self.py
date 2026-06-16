"""pf_toc_excludes_contents_self: ни 'Аннотация', ни сам заголовок 'СОДЕРЖАНИЕ' не попадают записями в оглавление."""
import helpers as h

c = h.Checks("pf_toc_excludes_contents_self")
pdf = h.compile("pf_toc_excludes_contents_self.typ")

toc_page = next((w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ"), None)
c.check("toc_page_found", toc_page is not None, "не найдена страница оглавления")

toc_words = [w[5] for w in h.words(pdf) if w[0] == toc_page]

# 'Аннотация' исключена из записей оглавления.
c.check("no_annotation_entry",
        "АННОТАЦИЯ" not in toc_words and "Аннотация" not in toc_words,
        f"аннотация попала в оглавление: {toc_words[:12]}")

# 'СОДЕРЖАНИЕ' встречается на странице оглавления ровно один раз — как заголовок,
# а не как собственная запись (само оглавление не выводит запись 'СОДЕРЖАНИЕ').
cnt = toc_words.count("СОДЕРЖАНИЕ")
c.check("contents_not_self_entry", cnt == 1,
        f"'СОДЕРЖАНИЕ' встречается {cnt} раз на стр. оглавления (ожидалось 1 — только заголовок)")

# Настоящие разделы при этом присутствуют как записи.
t = h.text(pdf)
c.check("real_sections_present", "1 Раздел один" in t and "2 Раздел два" in t,
        "настоящие разделы отсутствуют в оглавлении")

c.done()
