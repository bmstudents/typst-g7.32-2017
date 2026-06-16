"""pl point 6: вставить-лист со 'скрыть-номер: да' компилируется,
лист-страница есть. Номер остаётся в текстовом слое (печатается белым),
визуально скрыт — поэтому проверяем сам факт страницы и содержимого."""
import helpers as h

c = h.Checks("pl_insert_hide_number")
pdf = h.compile("pl_insert_hide_number.typ")

c.check("three_pages", h.page_count(pdf) == 3,
        f"ожидали 3 страницы, получили {h.page_count(pdf)}")
fw = h.first_word(pdf, 2)
c.check("sheet_on_page2", fw is not None and fw[1] == "скан",
        f"на стр.2 не лист: {fw}")
# номер по-прежнему в текстовом слое (TestVkr его видит): footer стр.2 = '2'
c.check("number_in_text_layer", h.footer_word(pdf, 2) == "2",
        f"номер листа не в текстовом слое: footer={h.footer_word(pdf, 2)!r}")
c.done()
