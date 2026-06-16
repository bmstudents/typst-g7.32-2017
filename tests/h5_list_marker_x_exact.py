"""h5_list_marker_x_exact: левый край маркера «–» списка стоит на красной строке —
x ≈ левое поле (30мм≈85.04) + абзацный отступ (1.25см≈35.43) ≈ 120.47pt, ±4pt.

Жёсткость: проверяем АБСОЛЮТНУЮ x-координату маркера против значения, вычисленного
из config (page.margin.left + page.parIndent), а не «маркер просто правее поля».
Все три маркера обязаны стоять на одном x (выровнены по красной строке).
"""
import helpers as h

c = h.Checks("h5_list_marker_x_exact")
pdf = h.compile("h5_list_marker_x_exact.typ")
W = h.words(pdf)

LEFT_MARGIN = 30 * 2.83464567       # 30mm → pt ≈ 85.04 (config.page.margin.left)
PAR_INDENT = 1.25 * 28.3464567      # 1.25cm → pt ≈ 35.43 (config.page.parIndent)
EXPECT = LEFT_MARGIN + PAR_INDENT   # ≈ 120.47
TOL = 4.0

DASH = "–"
markers = [w for w in W if w[5] == DASH]

c.check("three_markers", len(markers) == 3,
        f"ожидали 3 тире-маркера, нашли {len(markers)}")

if markers:
    xs = [m[1] for m in markers]
    # 1) Абсолютная позиция левого края маркера ≈ 120.47 ± 4.
    bad = [round(x, 2) for x in xs if abs(x - EXPECT) >= TOL]
    c.check("marker_x_at_redline", not bad,
            f"x маркеров {[round(x,2) for x in xs]} ∉ [{EXPECT-TOL:.2f}, {EXPECT+TOL:.2f}]; "
            f"выбиваются: {bad}")

    # 2) Маркер заведомо правее голого левого поля (смещён на отступ, не на поле).
    c.check("right_of_bare_margin", all(x > LEFT_MARGIN + 25 for x in xs),
            f"маркеры x={[round(x,2) for x in xs]} стоят у поля {LEFT_MARGIN:.2f}, "
            f"а не на красной строке")

    # 3) Все маркеры строго выровнены между собой (разброс < 0.5pt).
    c.check("markers_x_aligned", max(xs) - min(xs) < 0.5,
            f"маркеры не выровнены по x: разброс {max(xs)-min(xs):.2f}pt ({[round(x,2) for x in xs]})")

c.done()
