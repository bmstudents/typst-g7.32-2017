import helpers as h

c = h.Checks("xa_table_header_no_orphan")
pdf = h.compile("xa_table_header_no_orphan.typ")
ws = h.words(pdf)


def pg(word, nth=1):
    hh = [w for w in ws if w[5] == word]
    return (hh[nth - 1][0], round(hh[nth - 1][2], 1)) if len(hh) >= nth else (None, None)


cap_pg, cap_y = pg("Таблица")          # заголовок "Таблица 1 – ..."
colhdr_pg, _ = pg("Параметр")          # шапка колонок
firstrow_pg, firstrow_y = pg("ПЕРВАЯ")  # первая строка тела

c.check(
    "элементы найдены",
    cap_pg is not None and firstrow_pg is not None,
    f"cap={cap_pg} firstrow={firstrow_pg}",
)

# ГЛАВНОЕ: заголовок "Таблица 1" и первая строка тела на одной странице.
c.check(
    "заголовок таблицы не оторван от тела",
    cap_pg == firstrow_pg,
    f"заголовок 'Таблица 1' на стр.{cap_pg} (y={cap_y}), а первая строка тела "
    f"'ПЕРВАЯ' на стр.{firstrow_pg} (y={firstrow_y}) — заголовок остался внизу "
    f"страницы один (вместе лишь с шапкой колонок 'Параметр/Значение'), без "
    f"единой строки данных. На стр.{firstrow_pg} тело при этом помечено как "
    f"'Продолжение таблицы 1', хотя данных до него не было. Баг в "
    f"styles/figure.typ (kind: table): caption+шапка вынесены в table.header, "
    f"который не удерживается с первой строкой тела при разрыве.",
)

# Шапка колонок должна идти вместе с заголовком (это не баг, а контроль сетапа).
c.check(
    "шапка колонок при заголовке",
    colhdr_pg == cap_pg,
    f"заголовок стр.{cap_pg}, шапка колонок стр.{colhdr_pg}",
)

c.done()
