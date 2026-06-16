"""hd1_toc_number_unique: номера разделов в TOC уникальны и строго возрастают.

КОМБИНАЦИЯ: нумерованные разделы 1,2,3 -> приложение -> ещё нумерованный раздел.
Инвариант ГОСТ: основные разделы нумеруются сквозной возрастающей последовательностью
(1,2,3,4...). В оглавлении не может быть двух разделов с одинаковым номером.

Ожидаем prefixes [1,2,3,4]. При баге сброса счётчика приложением получаем [1,2,3,1]
— раздел после приложения повторно нумеруется как 1.
"""
import helpers as h

c = h.Checks("hd1_toc_number_unique")
pdf = h.compile("hd1_toc_number_unique.typ")
ws = h.words(pdf)
toc_page = min((w[0] for w in ws if w[5] == "СОДЕРЖАНИЕ"), default=1)

# Соберём строки TOC-страницы; для записи раздела префикс — самый левый токен,
# если это число (номер раздела). Запись приложения начинается с 'ПРИЛОЖЕНИЕ'.
rows = {}
for w in ws:
    if w[0] == toc_page:
        rows.setdefault(round(w[2], 1), []).append(w)

section_prefixes = []   # номера у записей, начинающихся с «Раздел»
for y in sorted(rows):
    wl = sorted(rows[y], key=lambda w: w[1])
    if not wl or wl[0][5] == "СОДЕРЖАНИЕ":
        continue
    # это запись основного раздела, если среди слов строки есть 'Раздел'
    has_razdel = any(w[5] == "Раздел" for w in wl)
    first = wl[0][5]
    if has_razdel and first.replace(".", "").isdigit():
        section_prefixes.append(first)

c.check("four_sections", len(section_prefixes) == 4,
        f"ожидалось 4 нумерованных раздела в TOC, найдено {len(section_prefixes)}: {section_prefixes}")

# Уникальность
unique = len(section_prefixes) == len(set(section_prefixes))
c.check("unique_numbers", unique,
        f"номера разделов в TOC НЕ уникальны: {section_prefixes}. "
        f"Раздел после приложения переполучает номер 1 — приложение сбрасывает "
        f"counter(heading) до 0 и не восстанавливает. "
        f"Файл: gost732-2017/styles/heading.typ (ветка unnumbered L1: "
        f"`context counter(heading).update(0)`).")

# Строго возрастающая последовательность 1,2,3,4
nums = [int(x) for x in section_prefixes]
expected = list(range(1, len(nums) + 1))
c.check("sequential_1234", nums == expected,
        f"номера разделов в TOC не образуют 1..N: получено {nums}, ожидалось {expected}. "
        f"Файл: gost732-2017/styles/heading.typ.")

c.done()
