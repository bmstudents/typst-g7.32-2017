"""3 tab-caption-separator (порядок и тип разделителя): между 'Таблица 1' и
подписью стоит тире '—', и номер идёт раньше подписи на одной y-строке."""
import helpers as h

c = h.Checks("ph_tab_separator_order")
pdf = h.compile("ph_tab_separator_order.typ")
t = h.text(pdf)

# Разделитель — именно тире (en-dash), не дефис-минус '-'.
c.check("dash_separator", "Таблица 1 — Характеристики" in t,
        f"нет тире-разделителя в подписи:\n{t}")

# Номер и подпись лежат на одной строке: y('Таблица') ≈ y('Характеристики').
y_num = h.y_of(pdf, "Таблица")
y_cap = h.y_of(pdf, "Характеристики")
same_line = (y_num is not None and y_cap is not None and abs(y_num - y_cap) <= 3)
c.check("same_baseline", same_line,
        f"номер и подпись не на одной строке: yТаблица={y_num} yХарактеристики={y_cap}")
c.done()
