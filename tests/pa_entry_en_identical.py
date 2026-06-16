"""pa_entry-en (аспект 2): английское имя gost732-2017 даёт ИДЕНТИЧНЫЙ результат
русскому гост732-2017 — сравниваем текстовый слой и геометрию заголовка
одного и того же документа, скомпилированного двумя именами входа."""
import helpers as h

c = h.Checks("pa_entry_en_identical")
pdf_en = h.compile("pa_entry_en_identical.typ")
pdf_ru = h.compile("pa_entry_ru_identical.typ")

t_en = h.text(pdf_en)
t_ru = h.text(pdf_ru)

# Нумерация заголовков работает одинаково под обоими именами.
c.check("en_section_numbered", "1 Раздел" in t_en, f"нет '1 Раздел' (en):\n{t_en[:200]!r}")
c.check("en_subsection_numbered", "1.1 Подраздел" in t_en,
        f"нет '1.1 Подраздел' (en):\n{t_en[:200]!r}")

# Текстовый слой совпадает байт-в-байт с русским именем входа.
c.check("text_layer_identical", t_en == t_ru,
        f"текст не совпал:\nen={t_en[:200]!r}\nru={t_ru[:200]!r}")

# Геометрия заголовка раздела совпадает (раздел переносится на новую страницу
# одинаково — pagebreak: true для l1).
y_en = h.y_of(pdf_en, "Раздел")
y_ru = h.y_of(pdf_ru, "Раздел")
c.check("heading_geometry_identical",
        y_en is not None and y_ru is not None and abs(y_en - y_ru) < 0.5,
        f"y заголовка различается: en={y_en} ru={y_ru}")
c.done()
