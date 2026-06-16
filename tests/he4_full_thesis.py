"""he4: полный мини-диплом (реферат+содержание+введение+3 раздела с
подразделами, рисунками, таблицами, формулами + заключение + список).
Сквозные инварианты: разделы 1,2,3; рисунки 1,2,3; таблицы 1,2,3;
формулы (1),(2),(3); номера страниц растут; библиография нумерована.
"""
import re
import helpers as h

c = h.Checks("he4_full_thesis")
pdf = h.compile("he4_full_thesis.typ")
t = " ".join(h.text(pdf).split())

# --- структурные элементы на месте ---
for el in ["РЕФЕРАТ", "СОДЕРЖАНИЕ", "ВВЕДЕНИЕ", "ЗАКЛЮЧЕНИЕ",
           "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ"]:
    c.check(f"has_{el.split()[0]}", el in t, f"нет структурного элемента {el!r}")

# --- сквозная нумерация разделов 1,2,3 ---
c.check("sections_seq",
        "1 Аналитический раздел" in t and "2 Конструкторский раздел" in t
        and "3 Технологический раздел" in t,
        f"нет сквозной нумерации разделов 1,2,3: {t[:300]}")

# подразделы 1.1 1.2 2.1 2.2
for sub in ["1.1 Обзор", "1.2 Постановка", "2.1 Аппаратная", "2.2 Программная"]:
    c.check(f"sub_{sub.split()[0]}", sub in t, f"нет подраздела {sub!r}")

# --- сквозные рисунки 1,2,3 (по одному в каждом разделе) ---
figs = re.findall(r"Рисунок (\d+) –", t)
c.check("figures_sequential", figs == ["1", "2", "3"],
        f"рисунки не сквозные 1,2,3: {figs}")

# --- сквозные таблицы 1,2,3 ---
tabs = re.findall(r"Таблица (\d+) –", t)
c.check("tables_sequential", tabs == ["1", "2", "3"],
        f"таблицы не сквозные 1,2,3: {tabs}")

# --- сквозные формулы (1),(2),(3) ---
eqs = re.findall(r"\((\d+)\)", t)
# отфильтруем только номера формул (1..3); прочих скобок в доке нет
eqs = [e for e in eqs if e in ("1", "2", "3")]
c.check("equations_sequential", eqs == ["1", "2", "3"],
        f"формулы не сквозные (1),(2),(3): {eqs}")

# --- библиография нумерована [1],[2] и записи отрендерены ---
c.check("bib_refs_in_text", "[1]" in t and "[2]" in t,
        "цитаты [1]/[2] не отрендерены в тексте")
c.check("bib_entries",
        "Кузнецов" in t and "Морозова" in t and "1. Кузнецов" in t and "2. Морозова" in t,
        f"записи библиографии не пронумерованы: {t[-200:]}")

# --- номера страниц монотонно растут по верху страниц (footer last word) ---
n = h.page_count(pdf)
footers = []
for p in range(1, n + 1):
    fw = h.footer_word(pdf, p)
    if fw and fw.isdigit():
        footers.append(int(fw))
c.check("page_numbers_present", len(footers) == n,
        f"не на всех страницах есть номер: {footers} из {n}")
c.check("page_numbers_increasing",
        footers == sorted(footers) and footers == list(range(1, n + 1)),
        f"номера страниц не растут 1..{n}: {footers}")

# --- TOC: страницы заголовков в содержании совпадают с фактическими ---
# В содержании указано: ВВЕДЕНИЕ на p3, разделы дальше. Проверим, что
# номер страницы напротив ВВЕДЕНИЯ в TOC == странице, где реально ВВЕДЕНИЕ.
toc_text = h.text(pdf)
m = re.search(r"ВВЕДЕНИЕ\s*[\. ]+(\d+)", " ".join(toc_text.split()))
toc_intro_page = int(m.group(1)) if m else None
# фактическая страница ВВЕДЕНИЯ как структурного раздела: первая страница,
# где первое слово == 'ВВЕДЕНИЕ' и это НЕ страница содержания.
intro_page = None
for p in range(1, n + 1):
    fw = h.first_word(pdf, p)
    if fw and fw[1] == "ВВЕДЕНИЕ":
        intro_page = p
        break
c.check("toc_intro_page_matches",
        toc_intro_page is not None and intro_page is not None
        and toc_intro_page == intro_page,
        f"в TOC ВВЕДЕНИЕ на стр {toc_intro_page}, фактически на {intro_page}")

c.done()
