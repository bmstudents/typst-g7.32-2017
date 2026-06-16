"""pi п.5 listing-breakable: длинный листинг (70 строк) разрывается/перетекает на 2+ страниц."""
import helpers as h

c = h.Checks("pi_listing_breakable")
pdf = h.compile("pi_listing_breakable.typ")

c.check("multipage", h.page_count(pdf) >= 2,
        f"листинг из 70 строк не перетёк на новую страницу: {h.page_count(pdf)} стр.")

# Тело распределилось по страницам: ранние строки на стр.1, поздние — дальше.
ws = h.words(pdf)
pages_line0 = [w[0] for w in ws if w[5] == "line_0"]
pages_line69 = [w[0] for w in ws if w[5] == "line_69"]
c.check("body_split", bool(pages_line0) and bool(pages_line69)
        and min(pages_line0) < max(pages_line69),
        f"строки листинга не разнесены по страницам: line_0={pages_line0}, line_69={pages_line69}")

# Подпись с номером по-прежнему присутствует
c.check("caption", "Листинг 1" in h.text(pdf), "пропала подпись 'Листинг 1'")
c.done()
