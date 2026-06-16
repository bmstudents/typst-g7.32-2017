"""pb heading-numbering: подразделы нумеруются двухуровнево '1.1', '1.2'
(точка между номером раздела и подраздела), и НЕ ломают страницу (l2 pagebreak:false)."""
import helpers as h

c = h.Checks("pb_heading_subsection")
pdf = h.compile("pb_heading_subsection.typ")
t = h.text(pdf)

c.check("subsection_1_1",
        "1.1 Подраздел альфа" in t,
        f"нет '1.1 Подраздел альфа' в:\n{t[:300]}")

c.check("subsection_1_2",
        "1.2 Подраздел бета" in t,
        f"нет '1.2 Подраздел бета' в:\n{t[:300]}")

# Оба подраздела на одной странице с разделом (l2 не делает pagebreak).
pages = {w[5]: w[0] for w in h.words(pdf) if w[5] in ("альфа", "бета", "Раздел")}
c.check("subsections_no_pagebreak",
        len(pages) == 3 and len(set(pages.values())) == 1,
        f"подразделы разнесены по страницам: {pages}")

c.done()
