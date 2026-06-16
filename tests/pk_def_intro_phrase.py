"""pk: раздел определений содержит вводную фразу по ГОСТ."""
import helpers as h

c = h.Checks("pk_def_intro_phrase")
pdf = h.compile("pk_def_intro_phrase.typ")
norm = " ".join(h.text(pdf).split())

c.check("intro_phrase",
        "В настоящем отчете о НИР применяют следующие термины" in norm,
        f"нет вводной фразы в:\n{norm[:500]}")
c.check("intro_full",
        "В настоящем отчете о НИР применяют следующие термины "
        "с соответствующими определениями" in norm,
        "вводная фраза обрезана / изменена")
c.done()
