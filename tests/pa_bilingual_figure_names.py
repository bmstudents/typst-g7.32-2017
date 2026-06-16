"""pa_bilingual-figure: #рис(...) (рус) и #img(...) (англ) оба дают подпись со
словом 'Рисунок'. Обе функции — синонимы одного API."""
import helpers as h

c = h.Checks("pa_bilingual_figure_names")
pdf = h.compile("pa_bilingual_figure_names.typ")
t = h.text(pdf)

# Две подписи 'Рисунок' (по одной от каждой функции).
c.check("two_risunok", t.count("Рисунок") == 2,
        f"ожидали 2 подписи 'Рисунок', нашли {t.count('Рисунок')}:\n{t!r}")

# Подпись от #рис.
c.check("ru_caption", "Русское имя функции" in t, f"нет подписи #рис:\n{t!r}")
# Подпись от #img.
c.check("en_caption", "Английское имя функции" in t, f"нет подписи #img:\n{t!r}")
c.done()
