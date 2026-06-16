"""xc_long_table_continuation: таблица 60 строк с многострочными (2-строчными)
ячейками — разрывается на несколько страниц. Граничные проверки:
  1) все 60 строк присутствуют;
  2) таблица реально длинная — разорвана минимум на 3 страницы
     (ТЗ: «разрывается на 3 страницы»; при inset=10pt/строку 60 двойных
     строк фактически дают 5 страниц — это >=3, инвариант тот же);
  3) на КАЖДОЙ продолжающей странице есть шапка «Продолжение таблицы 1»
     (а на первой — обычная подпись «Таблица 1 – …», без «Продолжение»);
  4) номер таблицы во всех шапках продолжения один и тот же ('1') —
     нумерация таблицы не сбивается на разрывах;
  5) ячейки действительно многострочные (две строки на разных y).

Примечание по ТЗ: ровно 3 страницы при 60 строках с реально многострочными
ячейками недостижимо из-за inset=10pt у каждой строки (config.figure.inset),
поэтому проверяем инвариант «>=3 страниц», не подгоняя ячейки под одну строку.
"""
import re
import helpers as h

c = h.Checks("xc_long_table_continuation")
pdf = h.compile("xc_long_table_continuation.typ")
ws = h.words(pdf)

# 1) 60 строк (по слову-маркеру 'Параметр' в каждой ячейке)
rows = [w for w in ws if w[5] == "Параметр"]
c.check("all_60_rows", len(rows) == 60, f"ожидали 60 строк, нашли {len(rows)}")

# 2) минимум 3 страницы
pages = h.page_count(pdf)
c.check("at_least_3_pages", pages >= 3, f"таблица не разорвана на >=3 страницы: pages={pages}")

# 3) шапка продолжения на каждой продолжающей странице
row_pages = sorted({w[0] for w in rows})
cont_pages = sorted({w[0] for w in ws if w[5] == "Продолжение"})
continued = [p for p in row_pages if p != row_pages[0]]
c.check(
    "continuation_on_every_continued_page",
    all(p in cont_pages for p in continued) and len(continued) >= 2,
    f"не на всех продолжающих страницах есть «Продолжение»: "
    f"строки на {row_pages}, «Продолжение» на {cont_pages}",
)

# первая страница таблицы несёт обычную подпись «Таблица 1 – Длинная таблица»,
# а НЕ «Продолжение»
first_pg = row_pages[0]
c.check(
    "first_page_normal_caption",
    any(w[5] == "Таблица" and w[0] == first_pg for w in ws)
    and first_pg not in cont_pages,
    f"на первой странице таблицы (стр.{first_pg}) нет обычной подписи «Таблица» "
    f"или присутствует «Продолжение»",
)

# 4) номер таблицы во всех шапках продолжения == '1'
def header_seq(pg):
    cont = [w for w in ws if w[5] == "Продолжение" and w[0] == pg]
    head_y = min(w[2] for w in cont)
    band = sorted(
        [w for w in ws if w[0] == pg and abs(w[2] - head_y) < 8],
        key=lambda t: t[1],
    )
    return " ".join(t[5] for t in band)

headers = {pg: header_seq(pg) for pg in cont_pages}
all_table1 = all(s.startswith("Продолжение таблицы 1") for s in headers.values())
c.check(
    "table_number_stable_1",
    bool(headers) and all_table1,
    f"номер таблицы в шапках продолжения сбился: {headers}",
)

# 5) ячейки многострочные: 'первая' и 'вторая' в строке 1 на разных y
pervaya = [w for w in ws if w[5] == "первая"]
vtoraya = [w for w in ws if w[5] == "вторая"]
multiline = (
    bool(pervaya) and bool(vtoraya)
    and pervaya[0][0] == vtoraya[0][0]
    and abs(vtoraya[0][2] - pervaya[0][2]) > 8
)
c.check(
    "cells_are_multiline",
    multiline,
    f"ячейка не двухстрочная: первая={pervaya[:1]}, вторая={vtoraya[:1]}",
)

c.done()
