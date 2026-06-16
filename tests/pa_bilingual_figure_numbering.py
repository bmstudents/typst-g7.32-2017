"""pa_bilingual-figure (аспект 2): рисунки от #img и #рис делят общий счётчик и
формат подписи 'Рисунок N – подпись'. Первый (#img) → 'Рисунок 1', второй
(#рис) → 'Рисунок 2'; разделитель ' – ' присутствует."""
import helpers as h

c = h.Checks("pa_bilingual_figure_numbering")
pdf = h.compile("pa_bilingual_figure_numbering.typ")
t = h.text(pdf)

c.check("img_is_1", "Рисунок 1 – Первая" in t,
        f"подпись #img не 'Рисунок 1 – Первая':\n{t!r}")
c.check("ris_is_2", "Рисунок 2 – Вторая" in t,
        f"подпись #рис не 'Рисунок 2 – Вторая' (общий счётчик):\n{t!r}")
c.done()
