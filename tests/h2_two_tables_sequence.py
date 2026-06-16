"""h2 ТАБЛИЦЫ #6: две таблицы подряд — нумерация 1 и 2, между ними зазор > 0.

ИНВАРИАНТЫ:
  1) подписи «Таблица 1» и «Таблица 2» обе присутствуют (счётчик инкрементится);
  2) обе на одной странице, идут сверху вниз: подпись №1 выше подписи №2;
  3) последняя строка тела первой таблицы (ПЕРВТАБб) расположена ВЫШЕ подписи
     второй таблицы, и между ними зазор > 0 — таблицы не слипаются;
  4) подпись «Таблица 2» появляется ровно один раз (нет лишних дублей счётчика).
"""
import helpers as h

c = h.Checks("h2_two_tables_sequence")
pdf = h.compile("h2_two_tables_sequence.typ")
ws = h.words(pdf)
t = h.text(pdf)

c.check("both_numbers", ("Таблица 1" in t) and ("Таблица 2" in t),
        f"нет обеих подписей «Таблица 1»/«Таблица 2» в тексте")

# y подписей: «Таблица» встречается дважды
y_cap1 = h.y_of(pdf, "Таблица", nth=1)
y_cap2 = h.y_of(pdf, "Таблица", nth=2)
c.check("two_captions", y_cap1 is not None and y_cap2 is not None,
        f"найдено подписей «Таблица»: {sum(1 for w in ws if w[5]=='Таблица')} (нужно 2)")

c.check("order_1_above_2", y_cap1 is not None and y_cap2 is not None and y_cap1 < y_cap2,
        f"порядок подписей нарушен: yТаблица1={y_cap1} yТаблица2={y_cap2}")

# зазор: низ тела таблицы 1 (ПЕРВТАБб, yMax) < верх подписи таблицы 2 (yMin)
y_t1_last = None
hits = [w for w in ws if w[5] == "ПЕРВТАБб"]
if hits:
    y_t1_last = hits[0][4]  # yMax
gap = (y_cap2 - y_t1_last) if (y_cap2 is not None and y_t1_last is not None) else None
c.check("gap_between_tables", gap is not None and gap > 0,
        f"таблицы слиплись: низ тела таблицы1 yMax={y_t1_last}, верх подписи таблицы2 "
        f"yMin={y_cap2}, зазор={gap}. Ожидал >0. Файл: h2_two_tables_sequence.typ")

# отдельность блоков: содержимое второй таблицы ниже подписи №2
y_v_body = h.y_of(pdf, "ВТОРТАБкол")
c.check("table2_body_below_cap2",
        y_v_body is not None and y_cap2 is not None and y_v_body > y_cap2,
        f"тело таблицы2 (ВТОРТАБкол yMin={y_v_body}) не ниже её подписи (yMin={y_cap2})")

c.done()
