"""xc_appendix_rotated_break: приложение А с повёрнутым рисунком 18×10см и
текстом после. Граничные проверки:
  1) компилируется без ошибок/overflow (compile бросает иначе);
  2) присутствует структурный элемент «ПРИЛОЖЕНИЕ А»;
  3) присутствует подпись «Рисунок А.1» (нумерация приложения с буквой),
     и подпись горизонтальна (читается слева-направо, ширина bbox > высоты);
  4) текст после повёрнутого рисунка реально присутствует и идёт НИЖЕ
     подписи на той же странице — поток не поглощён повёрнутым блоком.
"""
import helpers as h

c = h.Checks("xc_appendix_rotated_break")
pdf = h.compile("xc_appendix_rotated_break.typ")  # бросит при overflow-ошибке
ws = h.words(pdf)

# 1) приложение всегда уезжает на новые страницы -> минимум 3 страницы
c.check(
    "compiles_multipage",
    h.page_count(pdf) >= 3,
    f"ожидали >=3 страниц (раздел / титул приложения / тело), получили {h.page_count(pdf)}",
)

# 2) «ПРИЛОЖЕНИЕ А»
prilozh = [w for w in ws if w[5] == "ПРИЛОЖЕНИЕ"]
# буква 'А' рядом справа на той же строке
letter_ok = any(
    any(b[5] == "А" and b[0] == p[0] and abs(b[2] - p[2]) < 3 and b[1] > p[1]
        for b in ws)
    for p in prilozh
)
c.check(
    "appendix_heading",
    bool(prilozh) and letter_ok,
    f"нет структурного элемента 'ПРИЛОЖЕНИЕ А': ПРИЛОЖЕНИЕ={prilozh}",
)

# 3) подпись «Рисунок А.1»
ris = [w for w in ws if w[5] == "Рисунок"]
ad1 = [w for w in ws if w[5] == "А.1"]
cap_ok = bool(ris) and bool(ad1) and any(
    r[0] == a[0] and abs(r[2] - a[2]) < 3 for r in ris for a in ad1
)
c.check(
    "figure_caption_A1",
    cap_ok,
    f"нет подписи 'Рисунок А.1': Рисунок={ris}, А.1={ad1}",
)

# подпись горизонтальна: слово 'Рисунок' шире, чем выше
if ris:
    _, x0, y0, x1, y1, _ = ris[0]
    c.check(
        "caption_horizontal",
        (x1 - x0) > (y1 - y0),
        f"подпись 'Рисунок' не горизонтальна: w={x1-x0:.1f} h={y1-y0:.1f}",
    )
else:
    c.check("caption_horizontal", False, "нет слова 'Рисунок' для проверки ориентации")

# 4) текст после рисунка ниже подписи на той же странице (поток цел)
fig_pg = ris[0][0] if ris else None
cap_bottom = max(r[4] for r in ris) if ris else None
after = [w for w in ws if w[5] == "продолжать" and w[0] == fig_pg]
c.check(
    "text_after_figure_flows",
    fig_pg is not None and bool(after) and min(a[2] for a in after) > cap_bottom,
    f"текст после повёрнутого рисунка не идёт ниже подписи на стр.{fig_pg}: "
    f"подпись низ yMax={cap_bottom}, текст={[(a[0], round(a[2],1)) for a in [w for w in ws if w[5]=='продолжать']]}",
)

c.done()
