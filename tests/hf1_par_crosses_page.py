"""hf1 абзац через границу страницы: один абзац начинается с красной строки
(x0≈120.47) у нижнего края страницы N и перетекает на страницу N+1. Его
ПРОДОЛЖЕНИЕ обязано начинаться у ВЕРХНЕГО ПОЛЯ (y≈57, align top) и БЕЗ красной
строки (x0≈85.04), потому что отступ ставится только у первой строки абзаца.

Маркер CROSSPAR — первое слово целевого абзаца. Тест устойчив к тому, на
какой именно странице произошёл разрыв (находим страницу маркера).
"""
import helpers as h

c = h.Checks("hf1_par_crosses_page")
pdf = h.compile("hf1_par_crosses_page.typ")

LEFT = 85.04
REDLINE = 120.47
TOP = 56.26  # верхнее поле текста (20мм), yMin первой строки

ws = [w for w in h.words(pdf)]

# Страница и координаты маркера CROSSPAR.
mark = [w for w in ws if w[5] == "CROSSPAR"]
c.check("marker_present", len(mark) == 1, f"маркер CROSSPAR найден {len(mark)} раз")

if mark:
    pg0, mx0, my0 = mark[0][0], mark[0][1], mark[0][2]

    # Первая строка абзаца — с красной строкой.
    c.check("first_line_has_redline",
            abs(mx0 - REDLINE) < 1.5,
            f"первая строка абзаца x0={mx0:.2f}, ждём {REDLINE} (красная строка)")

    # Должен быть разрыв страницы: на следующей странице есть текст абзаца.
    npg = h.page_count(pdf)
    c.check("paragraph_spans_to_next_page",
            pg0 < npg,
            f"абзац-маркер на стр.{pg0} из {npg}; ожидали перенос на следующую")

    if pg0 < npg:
        cont_pg = pg0 + 1
        cont = [w for w in ws if w[0] == cont_pg and w[2] < 760]
        # Верхняя строка страницы-продолжения.
        top_y = min(w[2] for w in cont)
        top_line = [w for w in cont if abs(w[2] - top_y) < 3]
        top_x0 = min(w[1] for w in top_line)

        # Продолжение прижато к верхнему полю.
        c.check("continuation_at_top_margin",
                abs(top_y - TOP) < 3,
                f"верхняя строка продолжения y={top_y:.2f}, ждём {TOP} "
                f"(align top, начинать от верхнего поля)")

        # Продолжение БЕЗ красной строки — у левого поля.
        c.check("continuation_no_redline",
                abs(top_x0 - LEFT) < 1.5,
                f"продолжение абзаца x0={top_x0:.2f}, ждём {LEFT} (без красной "
                f"строки); если ≈{REDLINE} — баг: отступ на строке-продолжении")

c.done()
