"""xc_subsection_at_bottom: подраздел l2 у самого нижнего поля.
#v подобран в критическую точку: внизу стр.1 хватает места для заголовка
подраздела в одиночку, но НЕ для заголовка вместе с первой строкой текста.
Граничные проверки (sticky):
  1) заголовок подраздела '1.1 Подраздел …' и первое слово текста абзаца —
     на ОДНОЙ странице (заголовок не оторван от текста);
  2) заголовок не висит один внизу — он уехал на 2-ю страницу (page>1) к
     своему тексту, а не остался последним элементом стр.1;
  3) номер подраздела '1.1' идёт перед словом 'Подраздел' (нумерация l2 цела).
"""
import helpers as h

c = h.Checks("xc_subsection_at_bottom")
pdf = h.compile("xc_subsection_at_bottom.typ")
ws = h.words(pdf)

heading = [w for w in ws if w[5] == "Подраздел"]
num = [w for w in ws if w[5] == "1.1"]
first_text = [w for w in ws if w[5] == "Первый"]

c.check("heading_found", bool(heading), "не нашли заголовок 'Подраздел'")
c.check("text_found", bool(first_text), "не нашли первое слово текста 'Первый'")

h_pg = heading[0][0] if heading else None
t_pg = first_text[0][0] if first_text else None

# 1) sticky: заголовок и первый абзац на одной странице
c.check(
    "heading_with_text_same_page",
    h_pg is not None and t_pg is not None and h_pg == t_pg,
    f"заголовок (стр.{h_pg}) оторван от первого абзаца (стр.{t_pg}) — sticky сломан",
)

# 2) заголовок не повис внизу стр.1: он уехал на следующую страницу
c.check(
    "heading_pushed_not_dangling",
    h_pg is not None and h_pg >= 2,
    f"заголовок остался на стр.{h_pg}; ожидали перенос на стр.>=2 "
    f"(в критической точке #v он повис бы один без sticky)",
)

# дополнительно: на стр.1 заголовка нет вовсе (не остался обрезком)
c.check(
    "no_heading_on_page1",
    all(w[5] != "Подраздел" for w in ws if w[0] == 1),
    "слово 'Подраздел' всё-таки осталось на стр.1 — заголовок повис",
)

# 3) номер 1.1 перед словом 'Подраздел' на той же строке
num_ok = bool(num) and bool(heading) and num[0][0] == heading[0][0] \
    and abs(num[0][2] - heading[0][2]) < 3 and num[0][1] < heading[0][1]
c.check(
    "subsection_number",
    num_ok,
    f"номер '1.1' не стоит перед заголовком подраздела: 1.1={num}, Подраздел={heading}",
)

c.done()
