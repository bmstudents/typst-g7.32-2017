"""g9: определения в разделе сортируются по алфавиту (Анис раньше Базилика)."""
import helpers as h

c = h.Checks("g9_definitions_sorted")
pdf = h.compile("g9_definitions_sorted.typ")
t = h.text(pdf)

c.check("both_present", "Базилик" in t and "Анис" in t,
        f"нет обоих терминов в:\n{t[:400]}")

# В разделе термины-определения начинаются со слов "Анис"/"Базилик".
# Берём последнее вхождение (в самом разделе, не в теле раздела выше).
y_anis = h.y_of(pdf, "Анис", nth=1)
y_bazilik = h.y_of(pdf, "Базилик", nth=1)
c.check("coords_found", y_anis is not None and y_bazilik is not None,
        f"не нашёл координаты: Анис={y_anis} Базилик={y_bazilik}")

# "Базилик" вводится первым в тексте, но после сортировки "Анис" (А) выше.
c.check("alpha_order", y_anis is not None and y_bazilik is not None and y_anis < y_bazilik,
        f"Анис(y={y_anis}) должен быть выше Базилика(y={y_bazilik})")
c.done()
