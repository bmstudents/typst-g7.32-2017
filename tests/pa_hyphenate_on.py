"""pa_flag-hyphenate-on: по умолчанию фича-переносы-слов=да → длинное слово в
узком #box МОЖЕТ переноситься. Функционально: слово разбито на несколько
строк-фрагментов и есть маркер переноса (мягкий перенос U+00AD на стыке)."""
import helpers as h

c = h.Checks("pa_hyphenate_on")
pdf = h.compile("pa_hyphenate_on.typ")  # без флага → да по умолчанию
t = h.text(pdf)

word = "электроэнцефалография"
body_lines = [l.strip() for l in t.splitlines()
              if l.strip() and not l.strip().isdigit()]

# Слово больше НЕ лежит целиком на одной строке.
c.check("word_not_whole", word not in body_lines,
        f"слово не перенесено (осталось целым):\n{body_lines!r}")

# Разбито более чем на одну строку.
c.check("multiple_fragments", len(body_lines) > 1,
        f"слово не разбито на фрагменты:\n{body_lines!r}")

# Есть маркер переноса: мягкий перенос U+00AD на конце фрагмента.
c.check("hyphen_marker_present", "­" in t,
        f"нет маркера переноса U+00AD:\n{t!r}")
c.done()
