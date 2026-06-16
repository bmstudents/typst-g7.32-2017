"""h4_section_always_newpage: каждый раздел (ур.1) начинается с НОВОЙ страницы,
даже когда между разделами есть текст, который мог бы уместиться рядом.

Жёсткость: проверяем страницы по уникальным словам-маркерам заголовков
(«Альфа»/«Бета»/«Гамма»), требуем строгого монотонного возрастания
page(Альфа) < page(Бета) < page(Гамма) И что заголовок — самое верхнее
слово своей страницы (раздел реально открывает страницу, а не просто
оказался на ней из-за переполнения предыдущей).
"""
import helpers as h

c = h.Checks("h4_section_always_newpage")
pdf = h.compile("h4_section_always_newpage.typ")
ws = h.words(pdf)


def page_of(word):
    hits = [w for w in ws if w[5] == word]
    return hits[0][0] if hits else None


pA, pB, pG = page_of("Альфа"), page_of("Бета"), page_of("Гамма")

c.check("found_all_three",
        None not in (pA, pB, pG),
        f"не нашли все три маркера: Альфа={pA} Бета={pB} Гамма={pG}")

# Строгое возрастание страниц: 2-й раздел дальше 1-го, 3-й дальше 2-го.
c.check("strictly_increasing_pages",
        pA is not None and pB is not None and pG is not None and pA < pB < pG,
        f"страницы разделов не строго возрастают: {pA} / {pB} / {pG}")

# Каждый раздел открывает свою страницу: номер раздела ('1'/'2'/'3') —
# самое верхнее слово этой страницы.
tops = {p: h.first_word(pdf, p)[1] for p in (pA, pB, pG) if p}
c.check("each_section_tops_its_page",
        tops.get(pA) in ("1", "Раздел") and
        tops.get(pB) in ("2", "Раздел") and
        tops.get(pG) in ("3", "Раздел"),
        f"раздел не открывает страницу сверху, верхние слова страниц: {tops}")

c.done()
