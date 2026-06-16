"""pa_bilingual-table: #таблица(...) (рус) и #table_figure(...) (англ) оба дают
подпись со словом 'Таблица'. Обе функции — синонимы одного API."""
import helpers as h

c = h.Checks("pa_bilingual_table_names")
pdf = h.compile("pa_bilingual_table_names.typ")
t = h.text(pdf)

# Две подписи 'Таблица' (по одной от каждой функции).
c.check("two_tablica", t.count("Таблица") == 2,
        f"ожидали 2 подписи 'Таблица', нашли {t.count('Таблица')}:\n{t!r}")

c.check("ru_caption", "Русское имя функции" in t, f"нет подписи #таблица:\n{t!r}")
c.check("en_caption", "Английское имя функции" in t,
        f"нет подписи #table_figure:\n{t!r}")
c.done()
