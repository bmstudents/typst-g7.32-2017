"""11 tab-hyphenate-off (контраст фичи A2): перенос выключен ИМЕННО в таблице,
а в обычном тексте сохраняется. Внутритабличное слово остаётся целым."""
import helpers as h

c = h.Checks("ph_tab_hyphenate_text_on")
pdf = h.compile("ph_tab_hyphenate_text_on.typ")
t = h.text(pdf)
ws = h.words(pdf)

# Слово в таблице — целое.
word = "Электроэнцефалографический"
c.check("table_word_intact", word in t,
        f"слово в таблице разорвано: нет '{word}' в:\n{t}")

# Слово в таблице — единственный bbox-токен (не два фрагмента из-за переноса).
hits = [w for w in ws if w[5] == word]
c.check("table_word_single_token", len(hits) >= 1,
        f"слово таблицы не найдено цельным токеном: {[w[5] for w in ws if 'Электро' in w[5]]}")
c.done()
