"""pf_recog_appendix_no_number: '= ПРИЛОЖЕНИЕ А' распознаётся как приложение — не получает числовой номер '1'."""
import helpers as h

c = h.Checks("pf_recog_appendix_no_number")
pdf = h.compile("pf_recog_appendix_no_number.typ")
t = h.text(pdf)

# Запись приложения присутствует без ведущей цифры ('ПРИЛОЖЕНИЕ А', не '1 ПРИЛОЖЕНИЕ').
c.check("appendix_entry_present", "ПРИЛОЖЕНИЕ А" in t,
        f"нет записи 'ПРИЛОЖЕНИЕ А':\n{t[:160]!r}")
c.check("appendix_not_numbered", "1 ПРИЛОЖЕНИЕ" not in t and "1 Приложение" not in t,
        "приложение получило числовой номер '1'")

# В строке записи приложения первое слово — 'ПРИЛОЖЕНИЕ', а не цифра.
toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
prilozh = next(w for w in h.words(pdf) if w[0] == toc_page and w[5] == "ПРИЛОЖЕНИЕ")
y = prilozh[2]
line = sorted([w for w in h.words(pdf) if w[0] == toc_page and abs(w[2] - y) < 1.0],
              key=lambda w: w[1])
leftmost = line[0]
c.check("appendix_line_starts_with_word", leftmost[5] == "ПРИЛОЖЕНИЕ",
        f"строка приложения начинается не со слова: {leftmost[5]!r}")

# Обычный раздел после приложения получает номер '1' (приложение не съело номер).
c.check("normal_section_keeps_1", "1 Обычный раздел" in t,
        "обычный раздел после приложения не получил номер '1'")

c.done()
