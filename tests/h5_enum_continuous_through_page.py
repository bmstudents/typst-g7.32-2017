"""h5_enum_continuous_through_page: нумерованный список из 40 пунктов, пересекающий
границу страницы — нумерация ПРОДОЛЖАЕТСЯ на стр.2 (…, не сбрасывается на 1).

Жёсткость: измеримые инварианты по координатному слою —
  1) документ занимает ровно 2 страницы (40 пунктов гарантированно не влезают в одну);
  2) ровно 40 маркеров вида «N)», множество значений == {1..40} без дыр и дублей;
  3) первый маркер на стр.2 — НЕ «1)», и его номер строго больше последнего номера стр.1
     ровно на 1 (непрерывность через разрыв).
НЕ хардкодим точку разрыва — она зависит от вёрстки; проверяем сам инвариант непрерывности.
"""
import re
import helpers as h

c = h.Checks("h5_enum_continuous_through_page")
pdf = h.compile("h5_enum_continuous_through_page.typ")
W = h.words(pdf)

c.check("spans_two_pages", h.page_count(pdf) == 2,
        f"ожидали ровно 2 страницы, получили {h.page_count(pdf)}")

PAT = re.compile(r"^(\d+)\)$")
markers = [(w[0], int(PAT.match(w[5]).group(1))) for w in W if PAT.match(w[5])]
nums = sorted(n for _, n in markers)

# Ровно 40 маркеров, значения == полный диапазон 1..40 без сброса/дублей.
c.check("forty_markers_no_gaps", nums == list(range(1, 41)),
        f"ожидали маркеры ровно {{1..40}}, получили {nums}")

p1 = sorted(n for pg, n in markers if pg == 1)
p2 = sorted(n for pg, n in markers if pg == 2)

c.check("both_pages_have_items", len(p1) >= 1 and len(p2) >= 1,
        f"маркеры не распределены по двум страницам: стр1={p1}, стр2={p2}")

if p1 and p2:
    first_p2 = p2[0]
    last_p1 = p1[-1]
    # Стр.2 НЕ начинается с 1 — нумерация не сброшена.
    c.check("page2_not_reset", first_p2 != 1,
            f"стр.2 начинается с {first_p2}) — нумерация СБРОШЕНА на 1 (баг непрерывности)")
    # Непрерывность через границу: первый на стр.2 = последний на стр.1 + 1.
    c.check("continuous_across_break", first_p2 == last_p1 + 1,
            f"разрыв нумерации на границе: стр.1 кончается на {last_p1}), "
            f"стр.2 начинается с {first_p2}) (ожидали {last_p1 + 1}))")

c.done()
