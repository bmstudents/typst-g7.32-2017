"""Широкая таблица (1fr,1fr) не вылезает за поля.

После правки выравнивания (h(-1.25cm)+align(left)) узкие таблицы встают под
подпись — но полноширинная таблица не должна выехать левым краем за левое
поле. Левый текст ячейки ≈ 85 + inset(10) = 95; правый ≈ 552 − inset. Левый
край не должен быть < 85 (поле), правый не > 553."""
import helpers as h

c = h.Checks("hc_wide_table_left_edge")
pdf = h.compile("hc_wide_table_left_edge.typ")
ws = [w for w in h.words(pdf) if w[0] == 1]

lev = [w for w in ws if w[5] == "ЛЕВМАРК"]
prav = [w for w in ws if w[5] == "ПРАВМАРК"]
c.check("markers_present", len(lev) == 1 and len(prav) == 1,
        f"маркеры краёв не найдены: {[w[5] for w in ws]}")

if lev and prav:
    left_x0 = lev[0][1]
    right_x1 = prav[0][3]
    # левая линия таблицы ≈ left_x0 - inset(10); не должна быть < 85
    c.check("left_edge_in_margin", left_x0 - 10 >= 85 - 3,
            f"левый край таблицы за полем: текст x0={left_x0:.1f}, линия≈{left_x0-10:.1f} < 85")
    c.check("right_edge_in_margin", right_x1 <= 553,
            f"правый край за полем: xMax={right_x1:.1f} > 553")
c.done()
