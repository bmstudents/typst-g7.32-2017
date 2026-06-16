"""pg_list_multiple_items: 3 пункта маркированного списка → ровно 3 тире-маркера, по одному на пункт."""
import helpers as h

c = h.Checks("pg_list_multiple_items")
pdf = h.compile("pg_list_multiple_items.typ")
W = h.words(pdf)

DASH = "–"
markers = [w for w in W if w[5] == DASH]

# Ровно три тире-маркера на три пункта.
c.check("three_dashes", len(markers) == 3,
        f"ожидали 3 тире-маркера, нашли {len(markers)}")

# Маркеры выровнены по одному x (все на одном отступе).
if len(markers) == 3:
    xs = [m[1] for m in markers]
    c.check("aligned", max(xs) - min(xs) < 0.5,
            f"маркеры не выровнены по x: {[round(x,1) for x in xs]}")

# Каждый пункт идёт со своим словом-телом справа от маркера.
bodies = {w[5] for w in W}
c.check("bodies_present", {"альфа", "бета", "гамма"} <= bodies,
        f"не все тела пунктов в тексте: {bodies}")

c.done()
