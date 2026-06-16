"""pf_toc_generates_entries: оглавление содержит записи всех разделов и подраздела."""
import helpers as h

c = h.Checks("pf_toc_generates_entries")
pdf = h.compile("pf_toc_generates_entries.typ")
t = h.text(pdf)

# Записи разделов и подраздела присутствуют в текстовом слое оглавления.
c.check("entry_section_1", "1 Раздел один" in t, "нет записи '1 Раздел один'")
c.check("entry_subsection", "1.1 Подраздел" in t, "нет записи '1.1 Подраздел'")
c.check("entry_section_2", "2 Раздел два" in t, "нет записи '2 Раздел два'")

# Все три записи лежат на странице 1 (страница оглавления), каждая своей строкой.
toc = [w for w in h.words(pdf) if w[0] == 1]
ys_razdel = sorted({round(w[2], 0) for w in toc if w[5] == "Раздел"})
c.check("two_section_lines", len(ys_razdel) == 2,
        f"ожидалось 2 строки разделов на стр.1, найдено: {ys_razdel}")

c.done()
