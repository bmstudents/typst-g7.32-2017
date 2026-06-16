"""pl point 4: текст записей (авторы и названия) реально виден в списке."""
import helpers as h

c = h.Checks("pl_bib_entries_text")
pdf = h.compile("pl_bib_entries_text.typ")
t = " ".join(h.text(pdf).split())

c.check("author_1", "Петров" in t, f"нет автора 'Петров':\n{t[:400]}")
c.check("author_2", "Сидорова" in t, f"нет автора 'Сидорова':\n{t[:400]}")
c.check("title_1", "Цифровая обработка сигналов" in t,
        f"нет названия первой книги:\n{t[:400]}")
c.check("title_2", "Методы машинного обучения" in t,
        f"нет названия второй статьи:\n{t[:400]}")
c.done()
