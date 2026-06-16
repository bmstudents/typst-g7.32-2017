"""11 tab-hyphenate-off (фича A2): в обычной таблице БЕЗ ячейка() длинное слово
в узкой колонке не разрывается дефисом — show table: set text(hyphenate:false)."""
import helpers as h

c = h.Checks("ph_tab_hyphenate_off")
pdf = h.compile("ph_tab_hyphenate_off.typ")
t = h.text(pdf)
ws = h.words(pdf)

word = "Электроэнцефалографический"
c.check("word_intact", word in t,
        f"слово разорвано переносом — целого '{word}' нет в:\n{t}")
# Токенов с висячим дефисом (перенос по слогам) быть не должно.
hyph = [w[5] for w in ws if w[5].endswith("-") and len(w[5]) > 1]
c.check("no_trailing_hyphen", len(hyph) == 0,
        f"есть токены с висячим дефисом (перенос): {hyph}")
c.done()
