"""pl point 5: вставить-лист создаёт отдельную страницу, page_count растёт.
Функция доступна из главного импорта пакета."""
import helpers as h

c = h.Checks("pl_insert_basic")
pdf = h.compile("pl_insert_basic.typ")

# текст-до / лист / текст-после => 3 физические страницы
c.check("three_pages", h.page_count(pdf) == 3,
        f"ожидали 3 страницы, получили {h.page_count(pdf)}")

# содержимое листа ('скан') присутствует на отдельной странице 2
fw = h.first_word(pdf, 2)
c.check("sheet_on_page2", fw is not None and fw[1] == "скан",
        f"на стр.2 не лист: {fw}")
c.done()
