"""hd2: @ref на таблицу В ПРИЛОЖЕНИИ должен печатать 'Б.1' (с буквой).

Подтверждает, что баг хардкода numbering('1') в styles/page.typ
проявляется не только для image, но и для table-figure в приложении.
Подпись таблицы выводится как 'Таблица Б.1', ссылка обязана совпадать.
"""
import re
import helpers as h

c = h.Checks("hd2_ref_appendix_table")
pdf = h.compile("hd2_ref_appendix_table.typ")
t = " ".join(h.text(pdf).split())


def ref(pre, post):
    m = re.search(re.escape(pre) + r"\s+(.+?)\s+" + re.escape(post), t)
    return m.group(1) if m else "<нет>"


rmain = ref("осндо", "оснпосле")
rapp = ref("прилдо", "прилпосле")

c.check("ref_main_table_is_1", rmain == "1",
        f"ссылка на основную таблицу = '{rmain}', ожидалось '1'")

c.check("appendix_caption_has_letter",
        re.search(r"Таблица\s+Б\.\s*1", t) is not None,
        f"нет подписи 'Таблица Б.1'; текст: {t[:400]}")

c.check("ref_appendix_table_has_letter", rapp == "Б.1",
        f"ссылка на таблицу приложения = '{rapp}', ожидалось 'Б.1' "
        f"(styles/page.typ хардкодит numbering('1'), теряет букву приложения)")

c.done()
