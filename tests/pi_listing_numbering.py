"""pi п.3 listing-numbering: два листинга -> 'Листинг 1' и 'Листинг 2'."""
import helpers as h

c = h.Checks("pi_listing_numbering")
pdf = h.compile("pi_listing_numbering.typ")
t = h.text(pdf)

c.check("listing1", "Листинг 1" in t, f"нет 'Листинг 1' в:\n{t[:400]}")
c.check("listing2", "Листинг 2" in t, f"нет 'Листинг 2' в:\n{t[:400]}")

# Порядок: 'Листинг 1' раньше 'Листинг 2' в тексте
i1, i2 = t.find("Листинг 1"), t.find("Листинг 2")
c.check("order", i1 != -1 and i2 != -1 and i1 < i2,
        f"порядок нумерации нарушен: idx1={i1}, idx2={i2}")

# Нет третьего лишнего номера
c.check("no_listing3", "Листинг 3" not in t, "появился лишний 'Листинг 3'")
c.done()
