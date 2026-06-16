"""h6: собственная-нумерация:да на многостраничном приложении —
футер на страницах КОНТЕНТА приложения отсчитывается заново с 1, а не
продолжает глобальную нумерацию.

Документ: 4 страницы основного текста (футеры 1..4), затем приложение В.
Внутренняя реализация (appendix.typ): label(begin) ставится после титула
приложения, поэтому страницы контента приложения нумеруются как
global - begin, то есть 1, 2, 3...

Жёсткие инварианты:
  1. документ ровно 8 страниц (4 текста + 1 титул приложения + 3 контента);
  2. первая страница контента приложения (top-word 'Первая') имеет футер '1' —
     малое число, при том что её глобальный индекс страницы = 6;
  3. футеры трёх страниц контента образуют строгую возрастающую с 1
     последовательность [1, 2, 3] — то есть своя нумерация, а не глобальная
     [6, 7, 8].
"""
import helpers as h

c = h.Checks("h6_appendix_own_numbering")
pdf = h.compile("h6_appendix_own_numbering.typ")
n = h.page_count(pdf)

c.check("page_count_8", n == 8, f"ожидалось 8 страниц, получено {n}")

# Найдём страницы контента приложения по верхнему слову.
def page_with_top(word):
    for p in range(1, n + 1):
        fw = h.first_word(pdf, p)
        if fw and fw[1] == word:
            return p
    return None

p_first = page_with_top("Первая")
p_second = page_with_top("Вторая")
p_third = page_with_top("Третья")

c.check("content_pages_found",
        None not in (p_first, p_second, p_third),
        f"не нашёл страницы контента: Первая={p_first} Вторая={p_second} Третья={p_third}")

if None not in (p_first, p_second, p_third):
    f1 = h.footer_word(pdf, p_first)
    # 2. первая страница контента: футер '1', а глобальный индекс > 1.
    c.check("first_content_footer_reset",
            f1 == "1" and p_first > 1,
            f"футер первой стр. контента={f1!r} на глоб.странице {p_first}; "
            f"ожидалось '1' (своя нумерация сброшена)")

    # 3. последовательность футеров контента строго [1,2,3], не глобальная.
    seq = [h.footer_word(pdf, p) for p in (p_first, p_second, p_third)]
    glob = [str(p) for p in (p_first, p_second, p_third)]
    c.check("footer_sequence_reset",
            seq == ["1", "2", "3"],
            f"футеры контента приложения={seq}, ожидалось ['1','2','3'] "
            f"(глобальные были бы {glob})")
c.done()
