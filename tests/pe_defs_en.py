"""pe_defs_en: англ алиас #terms_abbreviations_designations[..] даёт тот же заголовок + переданный текст."""
import helpers as h

c = h.Checks("pe_defs_en")
pdf = h.compile("pe_defs_en.typ")
norm = " ".join(h.text(pdf).split())

c.check("heading", "ОПРЕДЕЛЕНИЯ, ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ" in norm,
        f"нет заголовка раздела (англ алиас) в:\n{norm[:200]}")
c.check("body_text", "Custom body text for the definitions section" in norm,
        "нет переданного текста тела раздела")
c.done()
