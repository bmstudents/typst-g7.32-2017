"""hd1_toc_appendix: приложения в TOC.

- Запись вида «ПРИЛОЖЕНИЕ А <Название>» (без номера-цифры раздела, капс).
- Номер страницы записи приложения == номер ТИТУЛЬНОЙ страницы приложения,
  печатаемый в её футере (приложение использует собственную нумерацию для своего
  содержимого, но в TOC должна указываться страница титула приложения с глобальным
  номером).
- Порядок: ПРИЛОЖЕНИЕ А идёт раньше ПРИЛОЖЕНИЕ Б, номера растут.
"""
import helpers as h

c = h.Checks("hd1_toc_appendix")
pdf = h.compile("hd1_toc_appendix.typ")
ws = h.words(pdf)
n_pages = h.page_count(pdf)
toc_page = min((w[0] for w in ws if w[5] == "СОДЕРЖАНИЕ"), default=1)
toc_ws = [w for w in ws if w[0] == toc_page]
norm = " ".join(h.text(pdf).split())


def footer_number(page):
    cand = [w for w in ws if w[0] == page and w[5].isdigit() and w[2] > 600]
    return int(max(cand, key=lambda w: w[2])[5]) if cand else None


# --- Формат записи в TOC ---
c.check("app_a_format", "ПРИЛОЖЕНИЕ А Первое Приложение" in norm,
        f"нет 'ПРИЛОЖЕНИЕ А Первое Приложение' в:\n{norm[:300]}")
c.check("app_b_format", "ПРИЛОЖЕНИЕ Б Второе Приложение" in norm,
        "нет 'ПРИЛОЖЕНИЕ Б Второе Приложение'")

# Перед записью приложения НЕ должно быть цифрового номера раздела
# (приложения ненумерованные). Проверим, что слева от 'ПРИЛОЖЕНИЕ' на строке TOC
# нет цифры.
def line_words(anchor_word, letter):
    rows = [w for w in toc_ws if w[5] == "ПРИЛОЖЕНИЕ"]
    for r in rows:
        same = sorted([w for w in toc_ws if abs(w[2] - r[2]) < 2.0], key=lambda w: w[1])
        if any(w[5] == letter for w in same):
            return same
    return []

for letter in ["А", "Б"]:
    row = line_words("ПРИЛОЖЕНИЕ", letter)
    c.check(f"app_{letter}_row", len(row) > 0, f"строка приложения {letter} не найдена в TOC")
    if row:
        # первое слово строки должно быть 'ПРИЛОЖЕНИЕ', не цифра
        c.check(f"app_{letter}_no_secnum", row[0][5] == "ПРИЛОЖЕНИЕ",
                f"перед 'ПРИЛОЖЕНИЕ {letter}' стоит {row[0][5]!r} (ожидалось без номера раздела)")

# --- page-truth: номер в TOC == футер титульной страницы приложения ---
def toc_printed_for_letter(letter):
    row = line_words("ПРИЛОЖЕНИЕ", letter)
    digits = [w for w in row if w[5].isdigit()]
    return int(max(digits, key=lambda w: w[3])[5]) if digits else None


def title_page_of(letter):
    # титульная страница приложения: физ. стр. (вне TOC), где есть 'ПРИЛОЖЕНИЕ'+буква
    # и слово 'Листов' (характерно для титула приложения).
    for p in range(1, n_pages + 1):
        if p == toc_page:
            continue
        pw = [w[5] for w in ws if w[0] == p]
        if "ПРИЛОЖЕНИЕ" in pw and letter in pw and "Листов" in pw:
            return p
    return None


for letter in ["А", "Б"]:
    printed = toc_printed_for_letter(letter)
    tp = title_page_of(letter)
    logical = footer_number(tp) if tp else None
    c.check(f"app_{letter}_truth", printed is not None and logical is not None and printed == logical,
            f"приложение {letter}: TOC обещает стр.{printed}, титул приложения на физ.{tp} "
            f"с футером {logical}. Файл: gost732-2017/utils/appendix.typ + styles/toc.typ")

# Порядок номеров А <= Б
pa = toc_printed_for_letter("А")
pb = toc_printed_for_letter("Б")
if pa is not None and pb is not None:
    c.check("order_a_before_b", pa < pb, f"приложение А (стр.{pa}) должно быть раньше Б (стр.{pb})")

c.done()
