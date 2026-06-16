"""hd1_toc_page_truth: КЛЮЧЕВОЙ инвариант.

Номер страницы в записи TOC == реальная страница, где находится заголовок.
Разделы разнесены по разным страницам через #pagebreak. Сравниваем номер,
напечатанный в записи оглавления, с фактическим номером страницы (из футера),
на которой реально стоит заголовок раздела.

ГОСТ: оглавление обязано указывать страницу, на которой действительно
расположен раздел. Если выводимый в TOC номер не совпадает с реальным —
оглавление врёт.
"""
import helpers as h

c = h.Checks("hd1_toc_page_truth")
pdf = h.compile("hd1_toc_page_truth.typ")
ws = h.words(pdf)
n_pages = h.page_count(pdf)

SECTIONS = ["Альфа", "Бета", "Гамма", "Дельта"]

# --- 1. Найдём страницу TOC: ту, где есть слово "СОДЕРЖАНИЕ".
toc_pages = sorted({w[0] for w in ws if w[5] == "СОДЕРЖАНИЕ"})
c.check("toc_exists", len(toc_pages) >= 1, f"нет 'СОДЕРЖАНИЕ' в документе ({n_pages} стр.)")
toc_page = toc_pages[0] if toc_pages else 1

# --- 2. Карта футеров: номер страницы, который реально печатается внизу каждой
# физической страницы. Футер = самое нижнее слово-цифра у нижнего края (y большой).
def footer_number(page):
    cand = [w for w in ws if w[0] == page and w[5].isdigit()]
    if not cand:
        return None
    bottom = max(cand, key=lambda w: w[2])
    # футер должен быть в нижней зоне (yMin заметно ниже середины ~400)
    if bottom[2] < 600:
        return None
    return int(bottom[5])

footers = {p: footer_number(p) for p in range(1, n_pages + 1)}

# --- 3. Для каждого раздела: на какой ФИЗИЧЕСКОЙ странице реально стоит его
# заголовок (вне TOC-страницы), и какой логический номер у этой страницы (футер).
def real_logical_page(section):
    hits = [w for w in ws if w[5] == section and w[0] != toc_page]
    if not hits:
        return None, None
    phys = min(hits, key=lambda w: w[0])[0]   # первая физ. страница с заголовком
    return phys, footers.get(phys)

# --- 4. Из TOC вытаскиваем номер, напечатанный в записи раздела.
# Запись раздела — слово section на TOC-странице; номер страницы — самое
# правое слово-цифра в той же строке (та же yMin).
def toc_printed_page(section):
    hits = [w for w in ws if w[5] == section and w[0] == toc_page]
    if not hits:
        return None
    y = hits[0][2]
    same_line = [w for w in ws if w[0] == toc_page and abs(w[2] - y) < 2.0 and w[5].isdigit()]
    if not same_line:
        return None
    rightmost = max(same_line, key=lambda w: w[3])
    return int(rightmost[5])

for sec in SECTIONS:
    phys, logical = real_logical_page(sec)
    printed = toc_printed_page(sec)
    c.check(f"{sec}_in_toc", printed is not None, f"раздел {sec!r} не найден в TOC")
    c.check(f"{sec}_on_page", phys is not None, f"раздел {sec!r} не найден в теле")
    if printed is not None and logical is not None:
        c.check(
            f"{sec}_page_truth",
            printed == logical,
            f"TOC обещает стр.{printed}, а заголовок {sec!r} реально на "
            f"логической стр.{logical} (физ.{phys}). "
            f"Файл: gost732-2017/utils/toc.typ / styles/heading.typ",
        )

c.done()
