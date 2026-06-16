"""pg_list_indent: маркер списка смещён на красную строку ≈ левое поле + 1.25см ≈ 120pt."""
import helpers as h

c = h.Checks("pg_list_indent")
pdf = h.compile("pg_list_indent.typ")
W = h.words(pdf)

LEFT_MARGIN = 30 * 2.83464567    # 30mm -> pt ≈ 85.04 (config.page.margin.left)
PAR_INDENT = 1.25 * 28.3464567   # 1.25cm -> pt ≈ 35.43 (config.page.parIndent)
EXPECT = LEFT_MARGIN + PAR_INDENT  # ≈ 120.47

dash = next((w for w in W if w[5] == "–"), None)
c.check("dash_exists", dash is not None, "тире-маркер списка не найден в координатном слое")

if dash is not None:
    # Маркер на абзацном отступе (≈1.25см от левого поля).
    c.check("marker_at_indent", abs(dash[1] - EXPECT) < 2.0,
            f"x тире-маркера {dash[1]:.2f} ≠ ожидаемому {EXPECT:.2f} (поле+отступ)")
    # И уж точно правее голого левого поля.
    c.check("right_of_margin", dash[1] > LEFT_MARGIN + 20,
            f"маркер x={dash[1]:.2f} не смещён от левого поля {LEFT_MARGIN:.2f}")

c.done()
