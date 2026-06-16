"""pd struct-upper: константа #введение рендерит капс 'ВВЕДЕНИЕ' одним словом."""
import helpers as h

c = h.Checks("pd_struct_upper_const")
pdf = h.compile("pd_struct_upper_const.typ")
ws = h.words(pdf)
t = h.text(pdf)

c.check("upper_in_text",
        "ВВЕДЕНИЕ" in t,
        f"нет 'ВВЕДЕНИЕ' в:\n{t[:300]!r}")

vv = [w for w in ws if w[5] == "ВВЕДЕНИЕ"]
c.check("single_upper_word",
        len(vv) == 1,
        f"ждём одно слово ВВЕДЕНИЕ, нашли: {vv}")

# Все буквы заголовка — заглавные (нет строчных русских в самом слове).
c.check("all_caps",
        all(ch.upper() == ch for ch in "ВВЕДЕНИЕ"),
        "контрольная строка не вся капсом")

c.done()
