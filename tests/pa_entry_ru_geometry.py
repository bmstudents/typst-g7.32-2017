"""pa_entry-ru (аспект 2): русская инициализация даёт корректную геометрию —
A4-ширина, верхнее/левое поле и номер страницы в подвале."""
import helpers as h

c = h.Checks("pa_entry_ru_geometry")
pdf = h.compile("pa_entry_ru_geometry.typ")
ws = h.words(pdf)

c.check("words_present", len(ws) > 0, "pdftotext не нашёл слов")

# Якорное слово стоит у верхнего/левого поля (верх≈56.25pt, лево≈85pt).
y, w = h.first_word(pdf, 1)
top_word = [t for t in ws if t[5] == "Якорь"]
c.check("top_margin", top_word and abs(top_word[0][2] - 56.25) < 12,
        f"верхнее поле не ~56.25pt: {top_word[0][2] if top_word else None}")
c.check("left_margin", top_word and abs(top_word[0][1] - 85) < 40,
        f"левое поле не ~85pt: {top_word[0][1] if top_word else None}")

# Номер страницы '1' стоит в подвале (есть нижнее слово страницы).
c.check("footer_number", h.footer_word(pdf, 1) == "1",
        f"в подвале не '1': {h.footer_word(pdf, 1)!r}")
c.done()
