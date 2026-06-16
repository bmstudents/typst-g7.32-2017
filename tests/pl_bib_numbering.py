"""pl point 2: два источника дают пронумерованные записи '1.' и '2.'."""
import re
import helpers as h

c = h.Checks("pl_bib_numbering")
pdf = h.compile("pl_bib_numbering.typ")
t = " ".join(h.text(pdf).split())

# отсекаем текст до заголовка списка, чтобы '1.' из цитат не мешал
src = t.split("СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ", 1)
body = src[1] if len(src) == 2 else t

c.check("entry_1", re.search(r"\b1\.\s", body) is not None,
        f"нет записи '1.' в списке:\n{body[:300]}")
c.check("entry_2", re.search(r"\b2\.\s", body) is not None,
        f"нет записи '2.' в списке:\n{body[:300]}")
# первая запись (Петров) идёт под номером 1, вторая (Сидорова) под 2
c.check("order", re.search(r"1\.\s*Петров", body) is not None
        and re.search(r"2\.\s*Сидорова", body) is not None,
        f"нарушен порядок нумерации записей:\n{body[:300]}")
c.done()
