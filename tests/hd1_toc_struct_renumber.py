"""hd1_toc_struct_renumber: ненумерованный структурный заголовок не должен
сбрасывать нумерацию последующих разделов.

КОМБИНАЦИЯ: Раздел(1) Раздел(2) ЗАКЛЮЧЕНИЕ Раздел(?). Любой ненумерованный
заголовок 1-го уровня (заключение/введение/приложение и т.п.) в style_heading
делает `counter(heading).update(0)`, из-за чего следующий нумерованный раздел
начинает счёт заново. Здесь «Раздел Гамма» получает номер 1 вместо 3.

Проверяем согласованность TOC <-> тело и уникальность номеров.
"""
import helpers as h

c = h.Checks("hd1_toc_struct_renumber")
pdf = h.compile("hd1_toc_struct_renumber.typ")
ws = h.words(pdf)
toc_page = min((w[0] for w in ws if w[5] == "СОДЕРЖАНИЕ"), default=1)


def section_number_in(page_pred, section_word):
    """Номер-префикс перед заголовком раздела (по слову названия) на странице."""
    cand = [w for w in ws if w[5] == section_word and page_pred(w[0])]
    if not cand:
        return None
    target = cand[0]
    row = sorted([w for w in ws if w[0] == target[0] and abs(w[2] - target[2]) < 2.0],
                 key=lambda w: w[1])
    first = row[0][5] if row else None
    return first if (first and first.replace(".", "").isdigit()) else None


# Номера в TOC
toc_nums = []
for sec in ["Альфа", "Бета", "Гамма"]:
    n = section_number_in(lambda p: p == toc_page, sec)
    c.check(f"toc_{sec}_has_num", n is not None, f"в TOC у раздела {sec} нет номера")
    if n is not None:
        toc_nums.append((sec, n))

nums = [n for _, n in toc_nums]
c.check("toc_unique", len(nums) == len(set(nums)),
        f"номера разделов в TOC не уникальны: {toc_nums}. "
        f"ЗАКЛЮЧЕНИЕ между разделами сбросило counter(heading). "
        f"Файл: gost732-2017/styles/heading.typ.")

c.check("toc_gamma_is_3", dict(toc_nums).get("Гамма") == "3",
        f"раздел Гамма в TOC имеет номер {dict(toc_nums).get('Гамма')!r}, ожидался '3' "
        f"(после Альфа=1, Бета=2). Файл: gost732-2017/styles/heading.typ.")

# Тело и TOC должны совпадать по номерам (TOC честно отражает тело — но тело уже
# битое). Проверяем согласованность, чтобы зафиксировать, что баг именно в нумерации,
# а не в рассинхроне TOC.
for sec in ["Альфа", "Бета", "Гамма"]:
    toc_n = section_number_in(lambda p: p == toc_page, sec)
    body_n = section_number_in(lambda p: p != toc_page, sec)
    if toc_n is not None and body_n is not None:
        c.check(f"consistent_{sec}", toc_n == body_n,
                f"раздел {sec}: номер в TOC={toc_n}, в теле={body_n} (рассинхрон)")

c.done()
