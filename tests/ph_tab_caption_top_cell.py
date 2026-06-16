"""2 tab-caption-top (через ячейку): и со вспомогат. ячейкой подпись остаётся
сверху — y('Подпись') < y('Содержимое')."""
import helpers as h

c = h.Checks("ph_tab_caption_top_cell")
pdf = h.compile("ph_tab_caption_top_cell.typ")

y_cap = h.y_of(pdf, "Подпись")
y_cell = h.y_of(pdf, "Содержимое")
c.check("found_both", y_cap is not None and y_cell is not None,
        f"yПодпись={y_cap} yСодержимое={y_cell}")
c.check("caption_above_cell", y_cap is not None and y_cell is not None and y_cap < y_cell,
        f"подпись не выше ячейки: yПодпись={y_cap} yСодержимое={y_cell}")
c.done()
