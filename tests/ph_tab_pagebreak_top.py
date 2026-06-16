"""12 tab-pagebreak-top (фикс B1): #v(700pt) выталкивает таблицу на стр.2,
и она начинается от верхнего поля — первое слово стр.2 yMin ≈ 56.25 (±2)."""
import helpers as h

c = h.Checks("ph_tab_pagebreak_top")
pdf = h.compile("ph_tab_pagebreak_top.typ")

c.check("pushed_to_page2", h.page_count(pdf) >= 2,
        f"таблица не ушла на стр.2: {h.page_count(pdf)} стр.")

fw = h.first_word(pdf, 2)
y_top = fw[0] if fw else None
c.check("starts_at_top_margin", y_top is not None and abs(y_top - 56.25) <= 2,
        f"первое слово стр.2 yMin={y_top} (ждём ≈56.25), это '{fw[1] if fw else None}'")
c.done()
