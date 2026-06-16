"""pb margin-left-30: первое слово абзаца с красной строкой стоит у x≈120pt
(поле 85.04 + отступ 35.43), а не у самого поля."""
import helpers as h

c = h.Checks("pb_margin_left_redline")
pdf = h.compile("pb_margin_left_redline.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 700]

# Самое верхнее слово — первое слово первой строки абзаца.
first = min(ws, key=lambda t: (t[2], t[1]))
c.check("first_word_indented",
        abs(first[1] - 120.47) < 2,
        f"первое слово на x={first[1]:.2f}, ждём ~120.47 (поле 85.04 + красная 35.43); слово={first[5]!r}")

# И этот сдвиг заметно правее левого поля (не прижат к 85).
c.check("redline_offset",
        first[1] > 85.04 + 25,
        f"первое слово не сдвинуто красной строкой: x={first[1]:.2f}, поле=85.04")

c.done()
