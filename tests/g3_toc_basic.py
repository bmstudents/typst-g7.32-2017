"""g3_toc_basic: содержание() выводит СОДЕРЖАНИЕ и записи разделов с номерами страниц."""
import helpers as h

c = h.Checks("g3_toc_basic")
pdf = h.compile("g3_toc_basic.typ")
t = h.text(pdf)

# СОДЕРЖАНИЕ как заголовок оглавления
c.check("toc_heading", "СОДЕРЖАНИЕ" in t, f"нет 'СОДЕРЖАНИЕ' в:\n{t[:120]}")

# Записи разделов с номерами (точки-заполнитель между текстом и страницей)
c.check("entry_l1", "1 Раздел один" in t, "нет записи '1 Раздел один' в оглавлении")
c.check("entry_l2", "1.1 Подраздел" in t, "нет записи '1.1 Подраздел' в оглавлении")

# Номер страницы стоит справа от записи раздела (xMax ≈ правый край ≈ 552pt).
# Берём "Раздел" из строки оглавления (page 1) и парную цифру-страницу той же строки.
toc_words = [w for w in h.words(pdf) if w[0] == 1]
razdel = next(w for w in toc_words if w[5] == "Раздел")
y = razdel[2]
# слова на той же строке оглавления (та же yMin)
same_line = [w for w in toc_words if abs(w[2] - y) < 1.0]
page_no = max(same_line, key=lambda w: w[3])  # самое правое — номер страницы
c.check("page_number_right", page_no[3] > 540 and page_no[5].isdigit(),
        f"номер страницы не у правого края: x1={page_no[3]:.1f} word={page_no[5]!r}")

c.done()
