"""pf_toc_pagebreak_content_offset: даже короткое оглавление + один раздел => раздел на отдельной странице (разрыв есть)."""
import helpers as h

c = h.Checks("pf_toc_pagebreak_content_offset")
pdf = h.compile("pf_toc_pagebreak_content_offset.typ")

n = h.page_count(pdf)
c.check("at_least_two_pages", n >= 2,
        f"короткое оглавление и раздел уместились на 1 страницу — разрыв отсутствует (стр={n})")

# Слово 'Единственный' встречается и как запись оглавления (стр.1), и как заголовок (стр.2).
pages = sorted({w[0] for w in h.words(pdf) if w[5] == "Единственный"})
c.check("title_on_two_pages", pages == [1, 2],
        f"заголовок раздела не вынесен на стр.2 после оглавления: страницы={pages}")

c.done()
