"""12 tab-pagebreak-top (что именно у верхнего поля): на перетёкшей странице
самое верхнее слово — это подпись таблицы ('Таблица'), и её yMin ≈ 56.25."""
import helpers as h

c = h.Checks("ph_tab_pagebreak_caption_top")
pdf = h.compile("ph_tab_pagebreak_caption_top.typ")

c.check("pushed_to_page2", h.page_count(pdf) >= 2,
        f"таблица не ушла на стр.2: {h.page_count(pdf)} стр.")

fw = h.first_word(pdf, 2)
c.check("caption_is_topmost", fw is not None and fw[1] == "Таблица",
        f"верхнее слово стр.2 = '{fw[1] if fw else None}', ждём 'Таблица'")
y_top = fw[0] if fw else None
c.check("at_top_margin", y_top is not None and abs(y_top - 56.25) <= 2,
        f"подпись стр.2 yMin={y_top}, ждём ≈56.25")
c.done()
