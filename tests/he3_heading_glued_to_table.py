"""he3_heading_glued_to_table: заголовок подраздела у нижнего поля, сразу
под ним таблица. Заголовок (sticky-блок в styles/heading.typ) не должен
отрываться от таблицы на границе страницы.

Инварианты:
1. Слово заголовка «Подраздел» и подпись таблицы «Таблица», и первая
   строка тела «A»/«B» — на ОДНОЙ странице (заголовок не сирота).
2. Заголовок выше подписи таблицы, подпись выше тела (правильный порядок).
"""
import helpers as h

c = h.Checks("he3_heading_glued_to_table")
pdf = h.compile("he3_heading_glued_to_table.typ")
ws = h.words(pdf)

head = [w for w in ws if w[5] == "Подраздел"]
cap = [w for w in ws if w[5] == "Таблица"]
body = [w for w in ws if w[5] in ("A", "B")]

c.check("all_present",
        head and cap and body,
        f"не всё отрисовано: head={bool(head)} cap={bool(cap)} body={bool(body)}")

if head and cap and body:
    hp = head[0][0]
    cp = cap[0][0]
    bp = body[0][0]
    c.check("heading_table_same_page",
            hp == cp == bp,
            f"заголовок оторван от таблицы: заголовок стр.{hp}, "
            f"подпись стр.{cp}, тело стр.{bp}")

    # Порядок по вертикали на их общей странице.
    c.check("vertical_order",
            head[0][2] < cap[0][2] < body[0][2],
            f"порядок нарушен: y(заголовок)={head[0][2]:.1f} "
            f"y(подпись)={cap[0][2]:.1f} y(тело)={body[0][2]:.1f}")

c.done()
