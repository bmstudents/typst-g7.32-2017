"""hd1_toc_structural: структурные элементы в TOC и исключённые.

Включаются (ВВЕДЕНИЕ, ЗАКЛЮЧЕНИЕ, СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ) — без номера,
капсом, с верным номером страницы. Исключаются (РЕФЕРАТ, СОДЕРЖАНИЕ): сам РЕФЕРАТ
в документе есть, но в записях оглавления его быть НЕ должно; «СОДЕРЖАНИЕ» в TOC
встречается только как заголовок самого оглавления.
"""
import helpers as h

c = h.Checks("hd1_toc_structural")
pdf = h.compile("hd1_toc_structural.typ")
ws = h.words(pdf)
n_pages = h.page_count(pdf)
toc_page = min((w[0] for w in ws if w[5] == "СОДЕРЖАНИЕ"), default=1)
toc_ws = [w for w in ws if w[0] == toc_page]


def footer_number(page):
    cand = [w for w in ws if w[0] == page and w[5].isdigit() and w[2] > 600]
    return int(max(cand, key=lambda w: w[2])[5]) if cand else None


footers = {p: footer_number(p) for p in range(1, n_pages + 1)}


def toc_printed(word):
    hits = [w for w in toc_ws if w[5] == word]
    if not hits:
        return None
    y = hits[0][2]
    digits = [w for w in toc_ws if abs(w[2] - y) < 2.0 and w[5].isdigit()]
    return int(max(digits, key=lambda w: w[3])[5]) if digits else None


def real_logical(word):
    hits = [w for w in ws if w[5] == word and w[0] != toc_page and w[2] < 300]
    if not hits:
        return None
    return footers.get(min(hits, key=lambda w: w[0])[0])


# --- ВКЛЮЧЁННЫЕ структурные элементы (page-truth) ---
for word in ["ВВЕДЕНИЕ", "ЗАКЛЮЧЕНИЕ"]:
    printed = toc_printed(word)
    logical = real_logical(word)
    c.check(f"{word}_in_toc", printed is not None, f"{word} нет в TOC")
    if printed is not None and logical is not None:
        c.check(f"{word}_truth", printed == logical,
                f"TOC: {word} -> стр.{printed}, реально стр.{logical}")

# СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ — первое слово СПИСОК
printed_list = toc_printed("СПИСОК")
logical_list = real_logical("СПИСОК")
c.check("biblio_in_toc", printed_list is not None, "СПИСОК... нет в TOC")
if printed_list is not None and logical_list is not None:
    c.check("biblio_truth", printed_list == logical_list,
            f"TOC: СПИСОК -> стр.{printed_list}, реально стр.{logical_list}")

# --- ИСКЛЮЧЁННЫЕ ---
# РЕФЕРАТ присутствует в документе, но НЕ в записях оглавления.
referat_in_doc = any(w[5] == "РЕФЕРАТ" for w in ws)
c.check("referat_exists", referat_in_doc, "РЕФЕРАТ должен быть в документе")
referat_on_toc = any(w[5] == "РЕФЕРАТ" for w in toc_ws)
c.check("referat_excluded", not referat_on_toc,
        "РЕФЕРАТ не должен попадать в записи оглавления "
        "(should_be_ignored_heading). Файл: gost732-2017/styles/toc.typ")

# СОДЕРЖАНИЕ на TOC-странице встречается ровно один раз — как заголовок оглавления,
# а не как запись.
cont_on_toc = [w for w in toc_ws if w[5] == "СОДЕРЖАНИЕ"]
c.check("soderzhanie_not_entry", len(cont_on_toc) == 1,
        f"'СОДЕРЖАНИЕ' на TOC-стр. встречается {len(cont_on_toc)} раз "
        f"(ожидался 1 — только заголовок оглавления)")

c.done()
