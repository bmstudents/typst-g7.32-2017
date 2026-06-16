"""xb_table_caption_multiline: таблица с длинной подписью на 2+ строки.
Заголовок «Таблица 1 – ...» переносится (уникальных yMin у слов подписи >=2),
а тело таблицы (ячейки «Параметр»/«Значение») начинается НИЖЕ всей подписи —
ни одна ячейка тела не вклинивается между строк подписи."""
import helpers as h

c = h.Checks("xb_table_caption_multiline")
pdf = h.compile("xb_table_caption_multiline.typ")
ws = h.words(pdf)
t = h.text(pdf)

sup = [w for w in ws if w[5] == "Таблица"]
assert sup, "нет супплемента 'Таблица'"
cap_page, cap_y0 = sup[0][0], sup[0][2]

# Слова тела таблицы.
y_param = h.y_of(pdf, "Параметр", page=cap_page)
y_value = h.y_of(pdf, "Значение", page=cap_page)
assert y_param is not None and y_value is not None, "нет ячеек тела таблицы"
body_top = min(y_param, y_value)

# Слова подписи: на cap_page, от cap_y0 и до начала тела (исключая футер).
caption_words = [w for w in ws
                 if w[0] == cap_page and cap_y0 <= w[2] < body_top and w[2] < 700]
uniq_y = sorted({round(w[2], 1) for w in caption_words})

# 1. Подпись на 2+ строки.
c.check("caption_2plus_lines", len(uniq_y) >= 2,
        f"подпись не на 2+ строки: уникальных yMin={len(uniq_y)} ({uniq_y})")

# 2. Тело таблицы ниже ВСЕЙ подписи: верх тела > yMin самой нижней строки
#    подписи (с запасом на высоту глифа ~13pt).
last_cap_line = max(uniq_y)
c.check("body_below_caption", body_top > last_cap_line + 10,
        f"тело таблицы (y={round(body_top,1)}) не ниже последней строки "
        f"подписи (y={round(last_cap_line,1)})")

# 3. Подпись и разделитель целы (перенос не порвал «Таблица 1 – ...»).
c.check("caption_text_intact", "Таблица 1 –" in t,
        f"подпись/разделитель не найдены в тексте:\n{t[:200]}")

c.done()
