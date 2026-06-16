"""he2 EDGE-таблицы #6: таблица сразу ПОСЛЕ таблицы (без текста между).

ИНВАРИАНТЫ:
  1) обе подписи присутствуют: «Таблица 1» и «Таблица 2» (сквозная нумерация
     не сбита соседством);
  2) НЕТ «Продолжение таблицы» — это две отдельные таблицы, а не разрыв одной
     (проверка логики continuation-счётчика, который сбрасывается после каждой);
  3) обе подписи прижаты влево к левому полю (одинаковый x0 == 85pt);
  4) есть положительный вертикальный зазор между концом 1-й таблицы и подписью
     2-й (>= 6pt) — таблицы не слиплись.

Файл пакета при провале: gost732-2017/styles/figure.typ (continuation update/get).
"""
import helpers as h

c = h.Checks("he2_tab_after_tab")
pdf = h.compile("he2_tab_after_tab.typ")
t = h.text(pdf)
ws = h.words(pdf)

LEFT = 30 / 25.4 * 72.0
TOL = 1.5

c.check("tab1_numbered", "Таблица 1" in t, f"нет 'Таблица 1':\n{t}")
c.check("tab2_numbered", "Таблица 2" in t, f"нет 'Таблица 2' — нумерация соседних таблиц сбита:\n{t}")
c.check("no_continuation", "Продолжение" not in t,
        f"появилось 'Продолжение таблицы' для двух отдельных таблиц подряд — "
        f"continuation-счётчик не сброшен. Файл: gost732-2017/styles/figure.typ:\n{t}")

caps = [w for w in ws if w[5] == "Таблица" and w[0] == 1]
c.check("two_captions", len(caps) == 2, f"найдено {len(caps)} слов 'Таблица' (ожидали 2)")

if len(caps) == 2:
    caps_sorted = sorted(caps, key=lambda w: w[2])
    x_top, x_bot = caps_sorted[0][1], caps_sorted[1][1]
    c.check("both_left_aligned",
            abs(x_top - LEFT) <= TOL and abs(x_bot - LEFT) <= TOL,
            f"подписи не выровнены к левому полю {LEFT:.1f}: x1={x_top:.1f} x2={x_bot:.1f}. "
            f"Файл: gost732-2017/styles/figure.typ")

    # зазор между низом последней ячейки первой таблицы и подписью второй
    y_cap2 = caps_sorted[1][2]
    end_t1 = max((w[4] for w in ws if w[0] == 1 and w[5] in {"перваяА", "перваяБ"}), default=None)
    if end_t1 is not None:
        gap = y_cap2 - end_t1
        c.check("gap_between_tables", gap >= 6.0,
                f"зазор между таблицами {gap:.1f}pt < 6pt — таблицы слиплись. "
                f"Файл: gost732-2017/styles/figure.typ")
c.done()
