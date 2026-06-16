"""he4 КОМБО: длинная таблица первого раздела перетекает на несколько
страниц («Продолжение таблицы 1»), затем начинается новый раздел.
Инварианты: продолжение подписано номером ИДУЩЕЙ таблицы (1, не 2);
следующая таблица в разделе 2 -> Таблица 2 (сквозной счётчик);
заголовок «Второй раздел» начинается с новой страницы (l1 pagebreak),
а не приклеивается к продолжению таблицы; разделы 1,2,3 сквозные;
номера страниц растут.
"""
import re
import helpers as h

c = h.Checks("he4_table_overflow_section")
pdf = h.compile("he4_table_overflow_section.typ")
n = h.page_count(pdf)
t = " ".join(h.text(pdf).split())
ws = h.words(pdf)

# --- таблица перетекла: есть продолжения ---
conts = set(re.findall(r"Продолжение таблицы (\d+)", t))
c.check("table_overflowed", len(conts) >= 1,
        "длинная таблица не перетекла (нет 'Продолжение таблицы')")
c.check("continuation_is_current_number", conts == {"1"},
        f"продолжение подписано неверным номером: {conts}, ожидался идущий '1' (а не будущий '2')")

# --- сквозная нумерация таблиц 1 затем 2 ---
tabs = re.findall(r"Таблица (\d+) —", t)
c.check("tables_sequential", tabs == ["1", "2"],
        f"таблицы не сквозные 1,2: {tabs}")

# --- разделы сквозные ---
c.check("sections_seq",
        "1 Первый раздел" in t and "2 Второй раздел" in t and "3 Третий раздел" in t,
        f"разделы не сквозные 1,2,3: {t[:200]}")

# --- 'Второй раздел' начинается на странице, где он первое слово ---
sec2_pages = sorted({w[0] for w in ws if w[5] == "Второй"})
c.check("section2_found", len(sec2_pages) >= 1, "не нашли 'Второй' раздел")
if sec2_pages:
    p = sec2_pages[0]
    fw = h.first_word(pdf, p)
    # На странице раздела 2 продолжения таблицы 1 быть не должно
    page_words = [w[5] for w in ws if w[0] == p]
    c.check("section2_not_glued_to_continuation",
            "Продолжение" not in page_words,
            f"заголовок раздела 2 на стр {p} склеен с продолжением таблицы 1")
    c.check("section2_starts_page",
            fw is not None and fw[1] in ("2", "Второй"),
            f"раздел 2 не начинает свою страницу: первое слово стр {p} = {fw}")

# --- номера страниц растут 1..n ---
footers = [int(h.footer_word(pdf, p)) for p in range(1, n + 1)
           if h.footer_word(pdf, p) and h.footer_word(pdf, p).isdigit()]
c.check("page_numbers_increasing", footers == list(range(1, n + 1)),
        f"номера страниц не 1..{n}: {footers}")

c.done()
