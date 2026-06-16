"""he2 EDGE-таблицы #9: вложенная таблица (table внутри ячейки).

ИНВАРИАНТЫ:
  1) компиляция не падает (compile бросит при ошибке);
  2) содержимое внешних и внутренних ячеек присутствует
     (ВНЕШНЯЯЛЕВ, ВНЕШНЯЯНИЗ, внв1..внв4);
  3) ровно ОДНА подпись: слово 'Таблица' встречается 1 раз, и нет
     'Продолжение' — внутренняя table не наследует фигурный show-rule
     (она не figure, а raw table), значит лишней подписи быть не должно.

Файл пакета при провале: gost732-2017/styles/figure.typ / styles/table.typ.
"""
import helpers as h

c = h.Checks("he2_tab_nested")
pdf = h.compile("he2_tab_nested.typ")
t = h.text(pdf)

for m in ["ВНЕШНЯЯЛЕВ", "ВНЕШНЯЯНИЗ", "внв1", "внв2", "внв3", "внв4", "обычная"]:
    c.check(f"present_{m}", m in t, f"нет содержимого {m}:\n{t}")

n_tab = t.count("Таблица")
c.check("single_caption", n_tab == 1,
        f"слово 'Таблица' встречается {n_tab} раз (ожидали 1) — вложенная "
        f"table породила лишнюю подпись/header. Файл: gost732-2017/styles/figure.typ:\n{t}")

c.check("no_continuation", "Продолжение" not in t,
        f"вложенная таблица вызвала 'Продолжение'. Файл: gost732-2017/styles/figure.typ:\n{t}")
c.done()
