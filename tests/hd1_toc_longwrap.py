"""hd1_toc_longwrap: очень длинный заголовок переносится в TOC.

- Запись занимает несколько строк (>= 2 строки).
- Номер страницы стоит на ПОСЛЕДНЕЙ строке записи (самая нижняя yMin среди строк
  записи), у правого края.
- Номер == реальная логическая страница заголовка.
- Номер не дублируется на каждой строке переноса (ровно один номер-страница на запись).
"""
import helpers as h

c = h.Checks("hd1_toc_longwrap")
pdf = h.compile("hd1_toc_longwrap.typ")
ws = h.words(pdf)
n_pages = h.page_count(pdf)
toc_page = min((w[0] for w in ws if w[5] == "СОДЕРЖАНИЕ"), default=1)
toc_ws = [w for w in ws if w[0] == toc_page]


def footer_number(page):
    cand = [w for w in ws if w[0] == page and w[5].isdigit() and w[2] > 600]
    return int(max(cand, key=lambda w: w[2])[5]) if cand else None


footers = {p: footer_number(p) for p in range(1, n_pages + 1)}

# Строки записи длинного заголовка: всё между его первым словом 'Чрезвычайно'
# и началом следующей записи ('Второй').
y_start = min((w[2] for w in toc_ws if w[5] == "Чрезвычайно"), default=None)
y_next = min((w[2] for w in toc_ws if w[5] == "Второй"), default=None)
c.check("long_present", y_start is not None, "длинная запись не найдена в TOC")
c.check("next_present", y_next is not None, "вторая запись не найдена в TOC")

if y_start is not None and y_next is not None:
    # слова записи: yMin в [y_start, y_next)
    entry = [w for w in toc_ws if y_start - 0.5 <= w[2] < y_next - 0.5]
    rows = sorted({round(w[2], 1) for w in entry})
    c.check("multiline", len(rows) >= 2,
            f"длинный заголовок не перенёсся: строк {len(rows)} (ожидалось >=2)")

    # номера-страницы внутри записи (правый край) — ровно один
    page_digits = [w for w in entry if w[5].isdigit() and w[3] > 540]
    c.check("single_page_number", len(page_digits) == 1,
            f"в записи {len(page_digits)} номеров-страниц у правого края (ожидался 1): "
            f"{[(w[5], round(w[2],1)) for w in page_digits]}")

    if page_digits:
        pd = page_digits[0]
        last_row_y = max(rows)
        c.check("number_on_last_row", abs(pd[2] - last_row_y) < 2.0,
                f"номер страницы на строке y={pd[2]:.1f}, последняя строка записи "
                f"y={last_row_y:.1f} (номер должен быть на последней строке). "
                f"Файл: gost732-2017/styles/toc.typ")
        c.check("number_right_edge", pd[3] > 540,
                f"номер страницы не у правого края: xMax={pd[3]:.1f}")

        # page-truth
        printed = int(pd[5])
        hits = [w for w in ws if w[5] == "Чрезвычайно" and w[0] != toc_page]
        logical = footers.get(min(hits, key=lambda w: w[0])[0]) if hits else None
        c.check("page_truth", logical is not None and printed == logical,
                f"TOC обещает стр.{printed}, реально логическая стр.{logical}")

# второй раздел тоже верен
sec2 = [w for w in toc_ws if w[5] == "Второй"]
if sec2:
    y = sec2[0][2]
    digits = [w for w in toc_ws if abs(w[2] - y) < 2.0 and w[5].isdigit()]
    if digits:
        printed2 = int(max(digits, key=lambda w: w[3])[5])
        hits2 = [w for w in ws if w[5] == "Второй" and w[0] != toc_page]
        logical2 = footers.get(min(hits2, key=lambda w: w[0])[0]) if hits2 else None
        c.check("second_truth", logical2 is not None and printed2 == logical2,
                f"второй раздел: TOC стр.{printed2}, реально {logical2}")

c.done()
