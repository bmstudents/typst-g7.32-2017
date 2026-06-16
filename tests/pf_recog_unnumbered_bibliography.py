"""pf_recog_unnumbered_bibliography: структурный 'СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ' ненумерован, обычный раздел нумеруется."""
import helpers as h

c = h.Checks("pf_recog_unnumbered_bibliography")
pdf = h.compile("pf_recog_unnumbered_bibliography.typ")
t = h.text(pdf)

# Обычный раздел получает номер '1'.
c.check("section_numbered_1", "1 Раздел один" in t, "раздел не получил '1'")

# Список источников присутствует и НЕ получил числовой префикс '2'.
c.check("bib_present", "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ" in t,
        f"нет заголовка списка источников:\n{t[:200]!r}")
c.check("bib_no_number", "2 СПИСОК" not in t,
        "список источников получил числовой префикс '2'")

# В оглавлении строка списка начинается со слова 'СПИСОК', а не с цифры.
toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
sp = next((w for w in h.words(pdf) if w[0] == toc_page and w[5] == "СПИСОК"), None)
c.check("bib_in_toc", sp is not None, "записи списка источников нет в оглавлении")
if sp is not None:
    line = sorted([w for w in h.words(pdf) if w[0] == toc_page and abs(w[2] - sp[2]) < 1.0],
                  key=lambda w: w[1])
    c.check("bib_line_starts_with_word", line[0][5] == "СПИСОК",
            f"строка списка начинается не со слова: {line[0][5]!r}")

c.done()
