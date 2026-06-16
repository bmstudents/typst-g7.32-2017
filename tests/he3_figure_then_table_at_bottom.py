"""he3_figure_then_table_at_bottom: рисунок + длинная таблица оба у нижнего
поля.

Инварианты:
1. Рисунок — неразрывный блок: подпись «Рисунок» и тело на одной странице
   (подпись не сирота).
2. Таблица переносится корректно: есть «Продолжение» (одна таблица → все
   продолжения с номером 1).
3. Хвостовой текст и все строки таблицы присутствуют (ничего не потеряно).
"""
import re
import helpers as h

c = h.Checks("he3_figure_then_table_at_bottom")
pdf = h.compile("he3_figure_then_table_at_bottom.typ")
ws = h.words(pdf)

fig = [w for w in ws if w[5] == "Рисунок"]
c.check("figure_present", bool(fig), "нет подписи 'Рисунок'")

# Рисунок целиком на одной странице (все вхождения «Рисунок» на одной стр.).
if fig:
    fig_pages = {w[0] for w in fig}
    c.check("figure_caption_single_page",
            len(fig_pages) == 1,
            f"подпись рисунка размазана по страницам: {fig_pages}")

# Таблица продолжается, номер стабилен (== 1).
t = " ".join(h.text(pdf).split())
conts = re.findall(r"Продолжение таблицы\s*([0-9]+)", t)
c.check("table_continues_number_1",
        conts and all(x == "1" for x in conts),
        f"таблица не перенеслась корректно, продолжения: {conts}")

# Все 29 строк данных присутствуют.
rows = [w[5] for w in ws if re.match(r"^стр[0-9]+$", w[5])]
c.check("all_rows_present",
        len(set(rows)) == 29,
        f"строк таблицы {len(set(rows))}, ожидали 29")

c.check("tail_present",
        any(w[5] == "Хвост" for w in ws),
        "хвостовой текст потерян")

c.done()
