"""hf3_enum_pagebreak_numbering: ИНВАРИАНТ — нумерация большого перечисления,
разорванного границей страницы, продолжается непрерывно (… 30) на стр.1,
31) … на стр.2), без сброса и без пропусков. Регресс-гард.
"""
import helpers as h

c = h.Checks("hf3_enum_pagebreak_numbering")
pdf = h.compile("hf3_enum_pagebreak_numbering.typ")

c.check("two_pages", h.page_count(pdf) >= 2,
        f"ожидали 2+ страницы, получили {h.page_count(pdf)}")

W = h.words(pdf)
# Собираем номера маркеров в порядке (page, y).
markers = []
for w in sorted(W, key=lambda t: (t[0], t[2])):
    m = w[5]
    if m.endswith(")") and m[:-1].isdigit():
        markers.append((w[0], int(m[:-1])))

nums = [n for _, n in markers]
c.check("all_45_present", nums == list(range(1, 46)),
        f"нумерация нарушена/неполна: {nums}")

# Перечисление реально разорвано: маркеры есть на 2+ страницах.
pages_with_markers = sorted({p for p, _ in markers})
c.check("split_across_pages", len(pages_with_markers) >= 2,
        f"маркеры только на страницах {pages_with_markers} — перечисление не разорвано")

# На границе нет сброса: первый маркер второй страницы > последнего на первой.
if len(pages_with_markers) >= 2:
    p1_last = max(n for p, n in markers if p == pages_with_markers[0])
    p2_first = min(n for p, n in markers if p == pages_with_markers[1])
    c.check("no_reset_at_break", p2_first == p1_last + 1,
            f"нумерация сбилась на границе: стр.1 кончилась на {p1_last}, "
            f"стр.2 началась с {p2_first}")

c.done()
