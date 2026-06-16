"""xc_tall_row_boundary: таблица с высокой строкой (ячейка ~6 строк) на
границе страницы. Граничные проверки:
  1) высокая ячейка не рвётся между страницами — все её слова-маркеры
     ('один,'..'шесть') на ОДНОЙ странице;
  2) при переносе на новую страницу появляется шапка «Продолжение таблицы 1»;
  3) строка после высокой ('3' / 'высокой.') идёт ниже неё на той же
     странице (порядок строк не перепутан).
"""
import helpers as h

c = h.Checks("xc_tall_row_boundary")
pdf = h.compile("xc_tall_row_boundary.typ")

ws = h.words(pdf)

# маркеры начала и конца многострочной ячейки
markers = ["один,", "два,", "три,", "четыре,", "пять,", "шесть"]
mw = {m: [w for w in ws if w[5] == m] for m in markers}
present = {m: v for m, v in mw.items() if v}
c.check(
    "cell_text_found",
    len(present) >= 5,
    f"не нашли строки высокой ячейки: {[m for m in markers if not mw[m]]}",
)

# 1) все маркеры ячейки на одной странице — ячейка не разорвана
cell_pages = sorted({v[0][0] for v in present.values()})
c.check(
    "tall_cell_not_split",
    len(cell_pages) == 1,
    f"высокая ячейка разорвана между страницами {cell_pages}: "
    f"{ {m: present[m][0][0] for m in present} }",
)
cell_pg = cell_pages[0] if len(cell_pages) == 1 else None

# 2) шапка продолжения на странице, куда переехала ячейка (если это не стр.1)
cont = [w for w in ws if w[5] == "Продолжение"]
cont_pages = sorted({w[0] for w in cont})
if cell_pg and cell_pg > 1:
    c.check(
        "continuation_header",
        cell_pg in cont_pages,
        f"на стр.{cell_pg} (куда переехала строка) нет «Продолжение таблицы»; "
        f"шапки на {cont_pages}",
    )
    # «Продолжение таблицы 1» — номер таблицы сохранён.
    # Шапка лежит в самой верхней строке (y≈56), данные строки — ниже (y≈82),
    # поэтому берём только слова из полосы шапки и читаем их слева направо.
    head_y = min(w[2] for w in cont if w[0] == cell_pg)
    band = sorted(
        [w for w in ws if w[0] == cell_pg and abs(w[2] - head_y) < 8],
        key=lambda t: t[1],
    )
    seq = " ".join(t[5] for t in band)
    c.check(
        "continuation_table_number",
        seq.startswith("Продолжение таблицы 1"),
        f"шапка продолжения не «Продолжение таблицы 1»: {seq!r}",
    )
else:
    c.check("continuation_header", False,
            f"ожидали перенос высокой строки на 2-ю страницу, ячейка на стр.{cell_pg}")
    c.check("continuation_table_number", False, "перенос не произошёл — нечего проверять")

# 3) строка '3' (после высокой) ниже последней строки ячейки на той же странице
last_cell_y = present["шесть"][0][4] if present.get("шесть") else \
    max(v[0][4] for v in present.values())
row3 = [w for w in ws if w[5] == "высокой." and w[0] == cell_pg]
c.check(
    "next_row_after_tall",
    bool(row3) and min(r[2] for r in row3) > last_cell_y,
    f"строка после высокой ('высокой.') не идёт под ячейкой на стр.{cell_pg}: "
    f"{[(r[0], round(r[2],1)) for r in [w for w in ws if w[5]=='высокой.']]}; "
    f"низ ячейки yMax={last_cell_y}",
)

c.done()
