"""pc align-top: контент начинается от верхнего поля (yMin первого слова ≈56.25)."""
import helpers as h

c = h.Checks("pc_align_top_text")
pdf = h.compile("pc_align_top_text.typ")

top_margin = 56.25  # верхнее поле 20мм ≈ 56.69pt, целевая верхняя граница строки

fw = h.first_word(pdf, 1)
c.check("first_word_marker", fw is not None and fw[1] == "ВЕРХМАРКЕР",
        f"первое слово {fw!r}, ждём 'ВЕРХМАРКЕР'")

# yMin верхнего слова близок к верхнему полю (с запасом на высоту строки).
c.check("first_word_at_top",
        fw is not None and abs(fw[0] - top_margin) < 10,
        f"yMin первого слова {fw[0] if fw else None}, ждём ≈{top_margin}±10")

c.done()
