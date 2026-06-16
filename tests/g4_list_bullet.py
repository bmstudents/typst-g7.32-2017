"""g4_list_bullet: маркированный список рендерится с тире-маркером (–), а не точкой-bullet."""
import helpers as h

c = h.Checks("g4_list_bullet")
pdf = h.compile("g4_list_bullet.typ")
t = h.text(pdf)

DASH = "–"  # – en-dash, используется как маркер ГОСТ-списка

# В тексте есть тире-маркер перед пунктами списка.
c.check("dash_marker_present", DASH in t, f"нет тире-маркера в тексте:\n{t!r}")

# Маркер — отдельное «слово» в координатном слое, по одному на каждый пункт (3 пункта).
markers = [w for w in h.words(pdf) if w[5] == DASH]
c.check("dash_per_item", len(markers) == 3,
        f"ожидали 3 тире-маркера, нашли {len(markers)}: {[w[5] for w in markers]}")

# Это НЕ типографский bullet '•' (U+2022).
c.check("not_bullet", "•" not in t, "встречен bullet '•' вместо тире")

c.done()
