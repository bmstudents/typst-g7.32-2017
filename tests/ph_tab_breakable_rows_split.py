"""5 tab-breakable (строки распределены по страницам): первые строки тела на
стр.1, последние — на стр.2; обе содержат строки таблицы (разрыв реальный)."""
import helpers as h

c = h.Checks("ph_tab_breakable_rows_split")
pdf = h.compile("ph_tab_breakable_rows_split.typ")

pc = h.page_count(pdf)
c.check("multipage", pc > 1, f"таблица не разорвалась: страниц {pc}")

# Первая строка тела на стр.1, последняя — на последней странице.
p_first = [w for w in h.words(pdf) if w[5] == "s1"]
p_last = [w for w in h.words(pdf) if w[5] == "s70"]
c.check("first_row_page1", len(p_first) > 0 and p_first[0][0] == 1,
        f"строка s1 не на стр.1: {[w[0] for w in p_first]}")
c.check("last_row_later_page", len(p_last) > 0 and p_last[0][0] == pc,
        f"строка s70 не на последней стр.{pc}: {[w[0] for w in p_last]}")
c.done()
