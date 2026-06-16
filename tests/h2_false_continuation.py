"""h2 ТАБЛИЦЫ #2: «Продолжение таблицы N» допустимо ТОЛЬКО когда выше реально
были строки данных этой таблицы.

Связано с #1: при разрыве сразу после шапки (без строк данных на 1-й странице)
пакет всё равно печатает на 2-й странице «Продолжение таблицы 1», хотя
продолжать нечего — данных на 1-й странице не было. Это ложная надпись.

ИНВАРИАНТ: на каждой странице, где есть «Продолжение таблицы», на ПРЕДЫДУЩИХ
страницах должна быть хотя бы одна числовая строка данных (СТРОКА*).
Конкретно: если «Продолжение» на стр.2, то на стр.1 обязана быть >=1 СТРОКА*.
"""
import helpers as h

c = h.Checks("h2_false_continuation")
pdf = h.compile("h2_false_continuation.typ")
ws = h.words(pdf)


def rows_on_page(pg):
    return sorted(int(w[5][6:]) for w in ws if w[0] == pg and w[5].startswith("СТРОКА"))


cont_pages = sorted({w[0] for w in ws if w[5] == "Продолжение"})

c.check("multipage", h.page_count(pdf) >= 2,
        f"таблица не разорвалась: {h.page_count(pdf)} стр. — тест бессмыслен")

c.check("continuation_exists", len(cont_pages) >= 1,
        f"нет ни одной надписи «Продолжение» — раскладка не та")

# Главный инвариант: перед каждым «Продолжение» уже должны были быть данные.
bad = []
for cp in cont_pages:
    prev_rows = []
    for p in range(1, cp):
        prev_rows += rows_on_page(p)
    if not prev_rows:
        bad.append(cp)

first_cont = cont_pages[0] if cont_pages else None
rows_before_first = []
for p in range(1, (first_cont or 1)):
    rows_before_first += rows_on_page(p)

c.check("no_false_continuation", not bad,
        f"ЛОЖНОЕ «Продолжение таблицы 1»: надпись есть на стр{bad}, "
        f"но на предыдущих страницах НЕ показано ни одной строки данных. "
        f"Перед первым «Продолжение» (стр{first_cont}) строки данных: {rows_before_first}. "
        f"Ожидал: «Продолжение» только когда выше реально были строки. "
        f"Получил: продолжать нечего, надпись фиктивна. "
        f"Файл: h2_false_continuation.typ (figure.typ: continuation-счётчик "
        f"взводится самим фактом повтора table.header, без проверки наличия данных)")

# Доп.: на самой стр. с первым «Продолжение» данные должны начинаться (т.е.
# первая строка СТРОКА1 именно тут) — подтверждает, что её оторвали от шапки.
rows_on_cont = rows_on_page(first_cont) if first_cont else []
c.check("first_row_lands_here", 1 in rows_on_cont,
        f"первая строка данных СТРОКА1 не на стр{first_cont}: строки тут {rows_on_cont[:5]}")

c.done()
