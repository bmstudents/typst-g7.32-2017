"""pb heading-numbering: один раздел нумеруется как '1' и выровнен по левому полю."""
import helpers as h

c = h.Checks("pb_heading_section_one")
pdf = h.compile("pb_heading_section_one.typ")
t = h.text(pdf)

c.check("section_numbered_1",
        "1 Первый раздел" in t,
        f"нет '1 Первый раздел' в:\n{t[:200]}")

# Номер '1' заголовка стоит у красной строки (~120.47), как у обычного абзаца.
ws = h.words(pdf)
# '1' заголовка — на той же строке, что и слово 'Первый'
head_y = h.y_of(pdf, "Первый")
num = [w for w in ws if w[5] == "1" and head_y is not None and abs(w[2] - head_y) < 3]
c.check("number_left_aligned",
        len(num) >= 1 and abs(num[0][1] - 120.47) < 3,
        f"номер раздела не у левого края/красной строки: {[(round(w[1],1)) for w in num]}, ждём ~120.47")

c.done()
