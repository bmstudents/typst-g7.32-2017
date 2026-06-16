"""pk: в разделе определения сортируются по алфавиту (Адрес 'А' выше Буфера 'Б'),
хотя 'буфер' введён первым в тексте."""
import helpers as h

c = h.Checks("pk_def_sorted")
pdf = h.compile("pk_def_sorted.typ")
norm = " ".join(h.text(pdf).split())

c.check("both_present", "Адрес" in norm and "Буфер" in norm,
        f"нет обоих терминов в:\n{norm[:400]}")

# Определения-абзацы в разделе начинаются со слов "Адрес"/"Буфер".
# Берём последнее вхождение — оно в самом разделе (ниже тела документа).
y_adres = h.y_of(pdf, "Адрес", nth=1)
y_bufer = h.y_of(pdf, "Буфер", nth=1)
c.check("coords_found", y_adres is not None and y_bufer is not None,
        f"не нашёл координаты: Адрес={y_adres} Буфер={y_bufer}")

c.check("alpha_order",
        y_adres is not None and y_bufer is not None and y_adres < y_bufer,
        f"Адрес(y={y_adres}) должен быть выше Буфера(y={y_bufer})")
c.done()
