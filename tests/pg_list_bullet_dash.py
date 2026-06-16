"""pg_list_bullet_dash: маркер маркированного списка — тире «–» (en-dash), а НЕ bullet «•»."""
import helpers as h

c = h.Checks("pg_list_bullet_dash")
pdf = h.compile("pg_list_bullet_dash.typ")
t = h.text(pdf)

DASH = "–"  # en-dash U+2013 — маркер ГОСТ-списка (из «-- » после типографики Typst)

# Тире-маркер присутствует в текстовом слое.
c.check("dash_present", DASH in t, f"нет тире-маркера в тексте:\n{t!r}")

# Маркер — отдельное «слово» координатного слоя, по одному на каждый пункт (2 пункта).
markers = [w for w in h.words(pdf) if w[5] == DASH]
c.check("dash_per_item", len(markers) == 2,
        f"ожидали 2 тире-маркера, нашли {len(markers)}")

# Это НЕ типографский bullet «•».
c.check("not_bullet", "•" not in t, "встречен bullet «•» вместо тире")

c.done()
