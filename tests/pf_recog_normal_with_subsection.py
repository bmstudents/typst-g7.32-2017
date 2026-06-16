"""pf_recog_normal_with_subsection: обычные разделы с произвольными названиями нумеруются 1, 1.1, 2 (не приняты за структурные)."""
import helpers as h

c = h.Checks("pf_recog_normal_with_subsection")
pdf = h.compile("pf_recog_normal_with_subsection.typ")
t = h.text(pdf)

# Раздел '1 Методика', подраздел '1.1 Этап подготовки', раздел '2 Результаты'.
c.check("section1_numbered", "1 Методика" in t, "'Методика' не получила номер '1'")
c.check("subsection_numbered", "1.1 Этап подготовки" in t,
        "подраздел не получил номер '1.1'")
c.check("section2_numbered", "2 Результаты" in t, "'Результаты' не получили номер '2'")

# Ни один обычный заголовок не капсован в оглавлении.
toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
toc_words = [w[5] for w in h.words(pdf) if w[0] == toc_page]
c.check("no_unexpected_caps",
        "Методика" in toc_words and "Результаты" in toc_words
        and "МЕТОДИКА" not in toc_words and "РЕЗУЛЬТАТЫ" not in toc_words,
        f"обычные разделы ошибочно капсованы как структурные: {toc_words[:14]}")

c.done()
