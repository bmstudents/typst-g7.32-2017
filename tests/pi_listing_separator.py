"""pi п.2 listing-caption-separator: подпись вида 'Листинг 1 – Код' (тире-разделитель)."""
import helpers as h

c = h.Checks("pi_listing_separator")
pdf = h.compile("pi_listing_separator.typ")
t = h.text(pdf)

# pdftotext рендерит en-dash как '–' (U+2013), как в g6_table_pagebreak_top.
full = "Листинг 1 – Подпись через тире"
c.check("full_caption", full in t,
        f"нет полной подписи '{full}' в:\n{t[:300]}")

# Разделитель именно тире (–), а не дефис (-) и не двойной дефис (--)
import re
c.check("dash_separator", re.search(r"Листинг 1\s*–\s*Подпись", t) is not None,
        f"между номером и подписью нет тире '–':\n{t[:300]}")

# В bbox '–' присутствует отдельным токеном между 'Листинг' и 'Подпись'
ws = [w for w in h.words(pdf) if w[5] in ("–", "Листинг", "Подпись")]
xs = {w[5]: w[1] for w in ws}
c.check("dash_between", "–" in xs and "Листинг" in xs and "Подпись" in xs
        and xs["Листинг"] < xs["–"] < xs["Подпись"],
        f"тире не расположено между 'Листинг' и 'Подпись': {ws}")
c.done()
