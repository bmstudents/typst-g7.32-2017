"""hd3: вставной лист (в-нумерации: нет) не ломает сквозную нумерацию.

Документ: стр.1 (текст) -> вставной лист вне нумерации -> стр.2 -> стр.3.
Содержательные страницы после листа должны иметь футеры 2 и 3, а не 3 и 4.
Главный инвариант: множество футеров содержательных страниц = {1,2,3}
(вставной лист «не съел» номер, последующие не сдвинулись).
"""
import helpers as h

c = h.Checks("hd3_insert_not_numbered_seq")
pdf = h.compile("hd3_insert_not_numbered_seq.typ")
n = h.page_count(pdf)

c.check("has_4_physical_pages", n == 4,
        f"физических страниц {n}, ожидалось 4 (3 текста + 1 вставка)")

# найдём содержательные страницы по первому слову
def first_word(p):
    fw = h.first_word(pdf, p)
    return fw[1] if fw else None

footers = {p: h.footer_word(pdf, p) for p in range(1, n + 1)}

# страница со вставкой содержит "СКАН"/"ЗАДАНИЯ"
ins_pages = [p for p in range(1, n + 1)
             if any(w[0] == p and w[5] in ("СКАН", "ЗАДАНИЯ") for w in h.words(pdf))]
c.check("insert_page_found", len(ins_pages) == 1,
        f"страница вставного листа не определилась: {ins_pages}")

# футеры содержательных (не вставка) страниц должны быть ровно 1,2,3
content_footers = [footers[p] for p in range(1, n + 1) if p not in ins_pages]
content_ints = [int(x) for x in content_footers if x and x.isdigit()]
c.check("content_footers_1_2_3", sorted(content_ints) == [1, 2, 3],
        f"футеры содержательных страниц = {content_footers}, ожидалось 1,2,3 "
        f"(вставной лист вне нумерации не должен сдвигать последующие номера)")

# и не должно быть пропуска в номерах: max == 3, нет '4'
c.check("no_gap_no_4", "4" not in content_footers and content_ints and max(content_ints) == 3,
        f"в нумерации содержательных страниц пропуск/сдвиг: {content_footers}")
c.done()
