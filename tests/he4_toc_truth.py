"""he4: содержание ПОСЛЕ реферата, перед введением. Все заголовки
(включая подразделы 1.1 и 1.1.1) попадают в TOC с ВЕРНЫМИ страницами.
Для каждой записи TOC сверяем указанную страницу с фактической
страницей появления заголовка в теле документа.
Реферат и содержание в TOC НЕ попадают.
"""
import re
import helpers as h

c = h.Checks("he4_toc_truth")
pdf = h.compile("he4_toc_truth.typ")
n = h.page_count(pdf)
ws = h.words(pdf)

# Страница содержания — где встречается слово СОДЕРЖАНИЕ как первое слово
toc_page = None
for p in range(1, n + 1):
    fw = h.first_word(pdf, p)
    if fw and fw[1] == "СОДЕРЖАНИЕ":
        toc_page = p
        break
c.check("toc_page_found", toc_page is not None, "не нашли страницу содержания")

# Собираем строки TOC по координатам на странице содержания: каждая
# запись = слова на одной y-линии, заканчивающиеся числом (страницей).
# нижний колонтитул (номер страницы содержания) исключаем: берём самую
# нижнюю y-линию и отбрасываем её, чтобы footer не спутался с записью TOC.
toc_words = [w for w in ws if w[0] == toc_page]
max_y = max(w[2] for w in toc_words)
toc_lines = {}
for w in toc_words:
    if w[2] >= max_y - 2:   # строка футера
        continue
    toc_lines.setdefault(round(w[2]), []).append((w[1], w[5]))
# Восстанавливаем (метка_заголовка -> номер_страницы_в_TOC)
toc_entries = {}
for y, items in toc_lines.items():
    items.sort()
    tokens = [tok for _, tok in items]
    if tokens and tokens[0] == "СОДЕРЖАНИЕ":
        continue
    # настоящая запись TOC содержит точки-заполнитель и текст заголовка,
    # т.е. больше одного токена; строка из одного числа — не запись.
    if len(tokens) < 2:
        continue
    # последний токен — номер страницы
    if tokens and tokens[-1].isdigit():
        page = int(tokens[-1])
        # ключ — первый осмысленный токен (номер раздела или слово)
        key = tokens[0]
        toc_entries[key] = page

# Ожидаемые ключи и фактические страницы заголовков в теле.
# Фактическая страница = первая страница (после страницы TOC), где данный
# заголовок-маркер встречается как слово.
def actual_page(marker, after):
    for p in range(after + 1, n + 1):
        page_words = [w[5] for w in ws if w[0] == p]
        if marker in page_words:
            return p
    return None

# Записи: маркер в TOC (первый токен) -> маркер в теле для поиска
# Числовые заголовки начинаются с номера (1, 1.1, ...), структурные — со слова.
expected = {
    "ВВЕДЕНИЕ": "ВВЕДЕНИЕ",
    "1": "1",        # 1 Теоретическая часть
    "1.1": "1.1",
    "1.1.1": "1.1.1",
    "1.2": "1.2",
    "2": "2",
    "2.1": "2.1",
    "2.2": "2.2",
    "ЗАКЛЮЧЕНИЕ": "ЗАКЛЮЧЕНИЕ",
}

c.check("all_headings_in_toc",
        all(k in toc_entries for k in expected),
        f"не все заголовки в TOC: есть {sorted(toc_entries)}, ждали {sorted(expected)}")

# Реферат и Содержание НЕ в TOC
c.check("abstract_not_in_toc",
        "РЕФЕРАТ" not in toc_entries and "Реферат" not in toc_entries,
        f"реферат попал в TOC: {sorted(toc_entries)}")

mismatches = []
for toc_key, body_marker in expected.items():
    if toc_key not in toc_entries:
        continue
    ap = actual_page(body_marker, toc_page)
    tp = toc_entries[toc_key]
    if ap != tp:
        mismatches.append(f"{toc_key}: TOC={tp} факт={ap}")

c.check("toc_pages_match_body", not mismatches,
        f"страницы в TOC не совпадают с телом: {mismatches}")

# Монотонность номеров TOC (страницы не убывают по порядку документа)
order = ["ВВЕДЕНИЕ", "1", "1.1", "1.1.1", "1.2", "2", "2.1", "2.2", "ЗАКЛЮЧЕНИЕ"]
seq = [toc_entries[k] for k in order if k in toc_entries]
c.check("toc_pages_monotonic", seq == sorted(seq),
        f"номера страниц в TOC не монотонны: {seq}")

c.done()
