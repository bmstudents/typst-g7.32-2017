"""hf3_enum_empty_item: ИНВАРИАНТ — пустой пункт перечисления не ломает
нумерацию: маркеры остаются 1) 2) 3), пустой пункт «съедает» свой номер,
но третий пункт нумеруется как 3) (а не 2)).

Краевой случай рукописного цикла по it.children с пустым phase.body.
"""
import helpers as h

c = h.Checks("hf3_enum_empty_item")
pdf = h.compile("hf3_enum_empty_item.typ")
t = h.text(pdf)
W = h.words(pdf)

markers = [w[5] for w in sorted(W, key=lambda x: (x[0], x[2]))
           if w[5].endswith(")") and w[5][:-1].isdigit()]

c.check("three_markers_1_2_3", markers == ["1)", "2)", "3)"],
        f"пустой пункт сбил нумерацию: {markers} (ожидали 1)2)3))")

c.check("third_text_present", "третий" in t, f"текст третьего пункта пропал:\n{t!r}")
c.check("first_text_present", "первый" in t, f"текст первого пункта пропал:\n{t!r}")

c.done()
