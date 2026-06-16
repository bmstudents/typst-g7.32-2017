"""pc heading-numbering-style: разделы 1-го уровня нумеруются '1','2' (стиль numbering='1')."""
import helpers as h

c = h.Checks("pc_heading_numbering_one")
pdf = h.compile("pc_heading_numbering_one.typ")
t = h.text(pdf)

c.check("section_one",
        "1 Введение в предмет" in t,
        f"нет '1 Введение в предмет':\n{t[:300]}")

c.check("section_two",
        "2 Основная часть" in t,
        f"нет '2 Основная часть':\n{t[:300]}")

# Не должно быть точечной нумерации '1.' у раздела верхнего уровня.
c.check("no_dotted_top",
        "1. Введение" not in t and "1.1 " not in t,
        f"раздел получил точечный номер вместо '1':\n{t[:300]}")

c.done()
