"""g7: подпись листинга 'Листинг 1 – ...' + моноширинное тело."""
import helpers as h

c = h.Checks("g7_listing_caption")
pdf = h.compile("g7_listing_caption.typ")
t = h.text(pdf)

c.check("listing_caption", "Листинг 1" in t and "Пример кода на Python" in t,
        f"нет 'Листинг 1 ... Пример кода' в:\n{t[:200]}")

# Тело листинга присутствует
c.check("listing_body", "print(&apos;hello&apos;)".replace("&apos;", "'") in t.replace("&apos;", "'") or "hello" in t,
        f"нет тела листинга в:\n{t[:200]}")

# Моноширинность: две строки одинаковой длины ("print('hello')" и "print('world')")
# имеют идентичную ширину (x0 и x1 совпадают).
ws = [w for w in h.words(pdf) if w[5].startswith("print")]
mono = (len(ws) == 2
        and abs(ws[0][1] - ws[1][1]) < 0.5   # одинаковый левый край
        and abs(ws[0][3] - ws[1][3]) < 0.5)  # одинаковая правая граница => моноширинный
c.check("monospace", mono, f"строки листинга не выровнены как моноширинные: {ws}")
c.done()
