"""pc heading-numbering-style: одиночный раздел получает номер '1' слева от заголовка."""
import re
import helpers as h

c = h.Checks("pc_heading_numbering_single")
pdf = h.compile("pc_heading_numbering_single.typ")
t = " ".join(h.text(pdf).split())

c.check("heading_prefixed_one",
        "1 Единственныйраздел" in t,
        f"нет '1 Единственныйраздел':\n{t[:300]}")

# Номер '1' стоит левее текста заголовка (выравнивание раздела по левому краю).
num = [w for w in h.words(pdf) if w[5] == "1"]
head = [w for w in h.words(pdf) if w[5] == "Единственныйраздел"]
ok = bool(num) and bool(head) and min(n[1] for n in num) < head[0][1]
c.check("number_left_of_title", ok,
        f"номер не левее заголовка: num_x={[round(n[1],1) for n in num]}, head_x={head[0][1] if head else None}")

c.done()
