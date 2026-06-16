"""pg_enum_sequence: 3 пункта нумерованного списка → «1)» «2)» «3)» по порядку сверху вниз."""
import helpers as h

c = h.Checks("pg_enum_sequence")
pdf = h.compile("pg_enum_sequence.typ")
W = h.words(pdf)

def marker(tok):
    return next((w for w in W if w[5] == tok), None)

m1, m2, m3 = marker("1)"), marker("2)"), marker("3)")

# Все три маркера присутствуют.
c.check("all_three", all(m is not None for m in (m1, m2, m3)),
        f"не все маркеры найдены: 1)={m1 is not None} 2)={m2 is not None} 3)={m3 is not None}")

# Идут по порядку сверху вниз (Y растёт вниз).
if all(m is not None for m in (m1, m2, m3)):
    c.check("top_to_bottom", m1[2] < m2[2] < m3[2],
            f"порядок маркеров нарушен: y1={m1[2]:.1f} y2={m2[2]:.1f} y3={m3[2]:.1f}")

c.done()
