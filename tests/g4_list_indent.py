"""g4_list_indent: маркеры списков смещены на отступ ≈1.25см от левого поля (x первого пункта ≈ левое поле + отступ)."""
import helpers as h

c = h.Checks("g4_list_indent")
pdf = h.compile("g4_list_indent.typ")
W = h.words(pdf)

# Геометрические константы пакета.
LEFT_MARGIN = 30 * 2.83464567   # 30mm -> pt ≈ 85.04 (config.page.margin.left)
PAR_INDENT = 1.25 * 28.3464567  # 1.25cm -> pt ≈ 35.43 (config.page.parIndent)
EXPECT = LEFT_MARGIN + PAR_INDENT  # ≈ 120.47

dash = next(w for w in W if w[5] == "–")          # маркер маркированного списка
paren = next(w for w in W if w[5] == "1)")         # маркер нумерованного списка

# Маркер маркированного списка смещён на ≈1.25см от левого поля.
c.check("bullet_indent",
        abs(dash[1] - EXPECT) < 2.0,
        f"x тире-маркера {dash[1]:.2f} ≠ ожидаемому {EXPECT:.2f} (поле+отступ)")

# Маркер нумерованного списка на том же отступе.
c.check("enum_indent",
        abs(paren[1] - EXPECT) < 2.0,
        f"x маркера '1)' {paren[1]:.2f} ≠ ожидаемому {EXPECT:.2f}")

# Оба типа списков выровнены по одному левому отступу.
c.check("aligned_markers",
        abs(dash[1] - paren[1]) < 0.5,
        f"маркеры списков не выровнены: тире x={dash[1]:.2f} '1)' x={paren[1]:.2f}")

c.done()
