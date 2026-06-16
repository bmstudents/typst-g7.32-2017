"""pf_toc_excludes_abstract: 'Реферат' печатается как заголовок в документе, но НЕ появляется записью в оглавлении."""
import helpers as h

c = h.Checks("pf_toc_excludes_abstract")
pdf = h.compile("pf_toc_excludes_abstract.typ")
t = h.text(pdf)

# 'Реферат' рендерится как структурный заголовок (капсом РЕФЕРАТ) где-то в документе.
c.check("abstract_rendered", "РЕФЕРАТ" in t, f"заголовок реферата не отрисован:\n{t[:120]!r}")

# Страница оглавления = та, где есть 'СОДЕРЖАНИЕ'.
toc_page = next((w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ"), None)
c.check("toc_page_found", toc_page is not None, "не найдена страница оглавления")

# На странице оглавления НЕТ записи 'РЕФЕРАТ'/'Реферат' (исключена should_be_ignored_heading).
if toc_page is not None:
    toc_words = [w[5] for w in h.words(pdf) if w[0] == toc_page]
    c.check("no_abstract_entry",
            "РЕФЕРАТ" not in toc_words and "Реферат" not in toc_words,
            f"реферат попал в оглавление: слова стр.{toc_page} = {toc_words[:12]}")
    # Запись реального раздела при этом в оглавлении есть.
    c.check("section_entry_present", "1 Раздел один" in t,
            "запись настоящего раздела отсутствует в оглавлении")

c.done()
