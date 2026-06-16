"""he4: МЕГА-документ — всё сразу (реферат+счётчики, содержание, введение,
2 раздела с подразделами/рисунками/таблицами/формулами/листингом,
заключение со ссылками, библиография, два приложения А и Б).
Проверяем что сквозные инварианты держатся ОДНОВРЕМЕННО (баг может
вылезать только в комбинации):
 - реферат-счётчики == фактические (рисунки/таблицы только тела, прил=2);
 - разделы 1,2 + подразделы;
 - рисунки/таблицы/формулы/листинг сквозные в теле; в приложениях — буквенные;
 - содержание содержит все разделы И оба приложения с верными глоб. страницами;
 - @ref в заключении дают верные номера;
 - библиография нумерована.
"""
import re
import helpers as h

c = h.Checks("he4_mega_document")
pdf = h.compile("he4_mega_document.typ")
n = h.page_count(pdf)
ws = h.words(pdf)
t = " ".join(h.text(pdf).split())

# --- реферат-счётчики == фактическим (тело: 2 рис, 2 табл; прил=2) ---
def marker(tag):
    m = re.search(rf"{tag} (\d+) {tag}", t)
    return int(m.group(1)) if m else None
abs_fig, abs_tab, abs_src, abs_app = (marker("РИС"), marker("ТАБ"),
                                      marker("ИСТ"), marker("ПРИЛ"))
# фактические рисунки/таблицы тела = с числовой подписью (не буквенной)
body_figs = re.findall(r"Рисунок (\d+) —", t)
body_tabs = re.findall(r"Таблица (\d+) —", t)
c.check("abstract_figs", abs_fig == len(body_figs) == 2,
        f"реферат рис={abs_fig}, тело={body_figs}")
c.check("abstract_tabs", abs_tab == len(body_tabs) == 2,
        f"реферат табл={abs_tab}, тело={body_tabs}")
c.check("abstract_src", abs_src == 2, f"реферат источников={abs_src}, ожидалось 2")
c.check("abstract_app", abs_app == 2, f"реферат приложений={abs_app}, ожидалось 2")

# --- сквозные счётчики тела ---
c.check("body_figs_seq", body_figs == ["1", "2"], f"рисунки тела: {body_figs}")
c.check("body_tabs_seq", body_tabs == ["1", "2"], f"таблицы тела: {body_tabs}")
# Номера блочных формул берём ДО заключения (в заключении есть ref "(1)",
# который тоже match-ится \((\d+)\)). Отрезаем по маркеру ЗАКЛЮЧЕНИЕ.
body_part = t.rsplit("ЗАКЛЮЧЕНИЕ", 1)[0]
eqs = [e for e in re.findall(r"\((\d+)\)", body_part) if e in ("1", "2")]
c.check("body_eqs_seq", eqs == ["1", "2"],
        f"формулы тела не сквозные (1),(2): {eqs}")
c.check("body_listing", "Листинг 1 — Главный цикл" in t, "листинг тела не Листинг 1")

# --- приложения: буквенная нумерация ---
c.check("appA_fig", "Рисунок А.1" in t, "нет Рисунок А.1")
c.check("appA_tab", "Таблица А.1" in t, "нет Таблица А.1")
c.check("appB_listing", "Листинг Б.1" in t, "нет Листинг Б.1 (листинг в приложении не лит.)")

# --- содержание: все разделы + оба приложения, верные глобальные страницы ---
toc_page = next((p for p in range(1, n + 1)
                 if (fw := h.first_word(pdf, p)) and fw[1] == "СОДЕРЖАНИЕ"), None)
toc_words = [w for w in ws if w[0] == toc_page]
max_y = max(w[2] for w in toc_words)
lines = {}
for w in toc_words:
    if w[2] >= max_y - 2:   # футер
        continue
    lines.setdefault(round(w[2]), []).append((w[1], w[5]))
entries = {}
for y, items in lines.items():
    items.sort()
    toks = [tk for _, tk in items]
    if not toks or toks[0] == "СОДЕРЖАНИЕ" or len(toks) < 2 or not toks[-1].isdigit():
        continue
    entries[" ".join(toks[:-1]).split(".")[0].strip()] = int(toks[-1])

# глобальная страница появления заголовков
def gpage(marker):
    for p in range(toc_page + 1, n + 1):
        if marker in [w[5] for w in ws if w[0] == p]:
            return p
    return None

# Раздел 1,2 и приложения в TOC
toc_keys = list(entries.keys())
c.check("toc_has_sections",
        any(k.startswith("1") for k in toc_keys) and any(k.startswith("2") for k in toc_keys),
        f"в TOC нет разделов 1/2: {toc_keys}")
c.check("toc_has_appendices",
        sum(1 for k in toc_keys if "ПРИЛОЖЕНИЕ" in k) == 2,
        f"в TOC не два приложения: {toc_keys}")

# страницы приложений в TOC == глобальной странице титула приложения
appA_global = next((p for p in range(toc_page + 1, n + 1)
                    if (fw := h.first_word(pdf, p)) and fw[1] == "ПРИЛОЖЕНИЕ"
                    and "А" in [w[5] for w in ws if w[0] == p and abs(w[2] - fw[0]) < 2]), None)
appB_global = None
seen = 0
for p in range(toc_page + 1, n + 1):
    fw = h.first_word(pdf, p)
    if fw and fw[1] == "ПРИЛОЖЕНИЕ":
        letters = [w[5] for w in ws if w[0] == p and abs(w[2] - fw[0]) < 2]
        if "Б" in letters:
            appB_global = p
toc_A = next((v for k, v in entries.items() if "ПРИЛОЖЕНИЕ А" in k or (k.startswith("ПРИЛОЖЕНИЕ") and "А" in k)), None)
toc_B = next((v for k, v in entries.items() if k.startswith("ПРИЛОЖЕНИЕ") and "Б" in k), None)
c.check("toc_appA_page", toc_A == appA_global,
        f"TOC прил.А={toc_A}, факт глоб.страница={appA_global}")
c.check("toc_appB_page", toc_B == appB_global,
        f"TOC прил.Б={toc_B}, факт глоб.страница={appB_global}")

# --- @ref в заключении: 1, 1, (1), 2 ---
m = re.search(r"Ссылки на (\d+), (\d+), \((\d+)\), (\d+) подтверждают", t)
c.check("refs_in_conclusion", m is not None and m.groups() == ("1", "1", "1", "2"),
        f"ссылки в заключении неверны: {m.groups() if m else None}, ждали (1,1,(1),2)")

# --- библиография нумерована ---
c.check("bib_numbered", "1. Кузнецов" in t and "2. Морозова" in t,
        "библиография не пронумерована 1./2.")

c.done()
