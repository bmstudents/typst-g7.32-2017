"""g9: раздел определений генерится с заголовком, вводной фразой и текстом определения."""
import helpers as h

c = h.Checks("g9_definitions_section")
pdf = h.compile("g9_definitions_section.typ")
t = h.text(pdf)

c.check("heading", "ОПРЕДЕЛЕНИЯ, ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ" in t,
        f"нет заголовка раздела в:\n{t[:400]}")
c.check("intro_phrase", "В настоящем отчете о НИР применяют следующие термины" in t,
        "нет вводной фразы")
norm = " ".join(t.split())
c.check("definition_text",
        "свойство мармеладной системы сохранять форму при нагреве" in norm,
        "нет текста определения в разделе")
c.done()
