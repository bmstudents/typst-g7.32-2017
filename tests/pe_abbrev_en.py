"""pe_abbrev_en: англ алиас #abbreviations_and_designations даёт тот же заголовок 'Перечень сокращений и ссылок'."""
import helpers as h

c = h.Checks("pe_abbrev_en")
pdf = h.compile("pe_abbrev_en.typ")
norm = " ".join(h.text(pdf).split())

c.check("heading_text", "перечень сокращений и ссылок" in norm.lower(),
        f"нет заголовка 'Перечень сокращений и ссылок' (англ алиас) в:\n{norm[:200]}")
c.done()
