"""hd1_toc_many_twodigit: 14 разделов, проверка двузначных номеров и монотонности.

- Все 14 записей попали в TOC.
- Номера страниц в TOC монотонно НЕ убывают (1<=2<=3...).
- Двузначные номера (>9) выровнены по правому краю так же, как однозначные:
  правый край (xMax) номера одинаков для всех строк (не «съезжают» влево/вправо).
- Номер из TOC == реальная логическая страница заголовка.
"""
import helpers as h

c = h.Checks("hd1_toc_many_twodigit")
pdf = h.compile("hd1_toc_many_twodigit.typ")
ws = h.words(pdf)
n_pages = h.page_count(pdf)

SECTIONS = [
    "Один", "Два", "Три", "Четыре", "Пять", "Шесть", "Семь",
    "Восемь", "Девять", "Десять", "Одиннадцать", "Двенадцать",
    "Тринадцать", "Четырнадцать",
]

toc_page = min((w[0] for w in ws if w[5] == "СОДЕРЖАНИЕ"), default=1)


def footer_number(page):
    cand = [w for w in ws if w[0] == page and w[5].isdigit() and w[2] > 600]
    return int(max(cand, key=lambda w: w[2])[5]) if cand else None


footers = {p: footer_number(p) for p in range(1, n_pages + 1)}


def toc_line(section):
    """Возвращает (printed_page:int, page_word_xmax:float) для записи раздела."""
    hits = [w for w in ws if w[5] == section and w[0] == toc_page]
    if not hits:
        return None, None
    y = hits[0][2]
    digits = [w for w in ws if w[0] == toc_page and abs(w[2] - y) < 2.0 and w[5].isdigit()]
    if not digits:
        return None, None
    rm = max(digits, key=lambda w: w[3])
    return int(rm[5]), rm[3]


def real_logical(section):
    hits = [w for w in ws if w[5] == section and w[0] != toc_page]
    if not hits:
        return None
    return footers.get(min(hits, key=lambda w: w[0])[0])


printed_pages = []
right_edges = []
for sec in SECTIONS:
    printed, xmax = toc_line(sec)
    c.check(f"{sec}_in_toc", printed is not None, f"раздел {sec!r} нет в TOC")
    if printed is not None:
        printed_pages.append(printed)
        right_edges.append((sec, printed, xmax))

c.check("all_14_present", len(printed_pages) == 14,
        f"в TOC найдено {len(printed_pages)} из 14 разделов")

# Монотонность номеров страниц
mono = all(printed_pages[i] <= printed_pages[i + 1] for i in range(len(printed_pages) - 1))
c.check("monotone_pages", mono, f"номера в TOC не монотонны: {printed_pages}")

# Должны встречаться двузначные номера (документ заведомо >9 страниц)
has_two_digit = any(p > 9 for p in printed_pages)
c.check("has_two_digit", has_two_digit, f"нет двузначных номеров: {printed_pages}")

# Выравнивание по правому краю: xMax всех номеров близок (разброс < 1.5pt).
if right_edges:
    xs = [e[2] for e in right_edges]
    spread = max(xs) - min(xs)
    worst = max(right_edges, key=lambda e: abs(e[2] - (sum(xs) / len(xs))))
    c.check("right_aligned", spread < 1.5,
            f"номера страниц съезжают по горизонтали: разброс xMax={spread:.2f}pt; "
            f"худшая запись {worst[0]!r} стр.{worst[1]} xMax={worst[2]:.1f}. "
            f"Файл: gost732-2017/styles/toc.typ (grid right+bottom)")

# Page-truth для всех
for sec in SECTIONS:
    printed, _ = toc_line(sec)
    logical = real_logical(sec)
    if printed is not None and logical is not None:
        c.check(f"{sec}_truth", printed == logical,
                f"TOC обещает стр.{printed}, реально логическая стр.{logical}")

c.done()
