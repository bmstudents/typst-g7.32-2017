"""pg_fig_caption: #рис(rect(...))[Схема] даёт подпись с «Рисунок 1» и названием «Схема»."""
import helpers as h

c = h.Checks("pg_fig_caption")
pdf = h.compile("pg_fig_caption.typ")
t = h.text(pdf)
toks = {w[5] for w in h.words(pdf)}

# Слово-supplement и номер.
c.check("supplement_word", "Рисунок" in toks, f"нет слова «Рисунок» в токенах: {sorted(toks)}")
c.check("number_one", "Рисунок 1" in t, f"нет «Рисунок 1» в тексте:\n{t}")

# Название рисунка присутствует.
c.check("title_present", "Схема" in toks, f"название «Схема» не найдено в токенах: {sorted(toks)}")

c.done()
