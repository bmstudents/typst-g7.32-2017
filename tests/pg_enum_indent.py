"""pg_enum_indent: маркер «1)» нумерованного списка смещён на абзацный отступ ≈ поле + 1.25см ≈ 120pt."""
import helpers as h

c = h.Checks("pg_enum_indent")
pdf = h.compile("pg_enum_indent.typ")
W = h.words(pdf)

LEFT_MARGIN = 30 * 2.83464567    # 30mm -> pt ≈ 85.04
PAR_INDENT = 1.25 * 28.3464567   # 1.25cm -> pt ≈ 35.43
EXPECT = LEFT_MARGIN + PAR_INDENT  # ≈ 120.47

paren = next((w for w in W if w[5] == "1)"), None)
c.check("marker_exists", paren is not None, "маркер «1)» не найден в координатном слое")

if paren is not None:
    c.check("marker_at_indent", abs(paren[1] - EXPECT) < 2.0,
            f"x маркера «1)» {paren[1]:.2f} ≠ ожидаемому {EXPECT:.2f} (поле+отступ)")
    c.check("right_of_margin", paren[1] > LEFT_MARGIN + 20,
            f"маркер x={paren[1]:.2f} не смещён от левого поля {LEFT_MARGIN:.2f}")

c.done()
