"""pf_recog_unnumbered_intro: '= ВВЕДЕНИЕ' и '= ЗАКЛЮЧЕНИЕ' распознаются как ненумерованные — без числового префикса."""
import helpers as h

c = h.Checks("pf_recog_unnumbered_intro")
pdf = h.compile("pf_recog_unnumbered_intro.typ")
t = h.text(pdf)

# Введение/заключение без ведущей цифры.
c.check("intro_no_number", "1 ВВЕДЕНИЕ" not in t and "1 Введение" not in t,
        "введение получило числовой префикс")
c.check("conclusion_no_number", "2 ЗАКЛЮЧЕНИЕ" not in t and "ЗАКЛЮЧЕНИЕ" in t,
        f"заключение пронумеровано или отсутствует:\n{t[:200]!r}")

# Запись 'ВВЕДЕНИЕ' в оглавлении начинается со слова, а не с цифры.
toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
vved = next(w for w in h.words(pdf) if w[0] == toc_page and w[5] == "ВВЕДЕНИЕ")
y = vved[2]
line = sorted([w for w in h.words(pdf) if w[0] == toc_page and abs(w[2] - y) < 1.0],
              key=lambda w: w[1])
c.check("intro_line_starts_with_word", line[0][5] == "ВВЕДЕНИЕ",
        f"строка введения начинается не со слова: {line[0][5]!r}")

# Единственный обычный раздел между ними получает номер '1' (введение не занумеровано).
c.check("only_real_section_numbered", "1 Раздел один" in t,
        "обычный раздел не получил '1' (введение, видимо, заняло номер)")

c.done()
