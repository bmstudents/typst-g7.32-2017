"""10 cell-nobreak (через bbox): длинное слово ячейки лежит как один токен
(одна bbox-запись) — не разбито на два фрагмента «слово-» / «-слово»."""
import helpers as h

c = h.Checks("ph_cell_nobreak_glyph")
pdf = h.compile("ph_cell_nobreak_glyph.typ")
ws = h.words(pdf)

word = "Высокопроизводительность"
hits = [w for w in ws if w[5] == word]
c.check("single_token", len(hits) == 1,
        f"слово найдено {len(hits)} раз(а) (ожидался 1 цельный токен): {[w[5] for w in ws]}")
# Никаких токенов, оканчивающихся на дефис (признак переноса) в ячейке.
hyph = [w[5] for w in ws if w[5].endswith("-") and len(w[5]) > 1]
c.check("no_trailing_hyphen", len(hyph) == 0,
        f"есть токены с висячим дефисом (перенос): {hyph}")
c.done()
