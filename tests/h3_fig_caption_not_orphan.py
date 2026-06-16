"""h3 РИСУНКИ: подпись «Рисунок N» НЕ должна отрываться от тела на разрыве страницы.

Рисунок rect(8cm×5cm) с текст-меткой МЕТКАТЕЛА внутри тела вытолкнут #v(19cm)
к самому низу стр.1: тело ОДНО влезает, но тело+зазор+подпись — уже нет.
ИНВАРИАНТ ГОСТ: рисунок и его подпись «Рисунок 1» — единый неразрывный блок,
страница метки тела == страница подписи.

ИЗВЕСТНЫЙ БАГ (figure.typ kind:image — body/v/caption три отдельных блока,
не обёрнуты в block(breakable:false)): подпись отрывается на стр.2 → FAIL.
Тело rect не даёт текста pdftotext'у, поэтому страницу тела определяем по
МЕТКАТЕЛА внутри прямоугольника.
"""
import helpers as h

c = h.Checks("h3_fig_caption_not_orphan")
pdf = h.compile("h3_fig_caption_not_orphan.typ")
ws = h.words(pdf)


def find(word):
    return [w for w in ws if w[5] == word]


body = find("МЕТКАТЕЛА")
cap = find("Рисунок")

# 1. И тело (метка), и подпись присутствуют в документе.
c.check("body_marker_present", len(body) == 1,
        f"метка тела встречается {len(body)} раз, ожидалась 1; слова={[w[5] for w in ws]}")
c.check("caption_present", len(cap) == 1,
        f"«Рисунок» встречается {len(cap)} раз, ожидалось 1")

if body and cap:
    body_page = body[0][0]
    cap_page = cap[0][0]
    # 2. КЛЮЧЕВОЙ ИНВАРИАНТ: тело и подпись на одной странице.
    c.check("same_page", body_page == cap_page,
            f"ОТРЫВ ПОДПИСИ: тело МЕТКАТЕЛА на стр.{body_page} (y={body[0][2]:.1f}), "
            f"«Рисунок 1» на стр.{cap_page} (y={cap[0][2]:.1f}). "
            f"figure kind:image выводит body/v/caption отдельными блоками — "
            f"на разрыве страницы подпись осиротела.")
    # 3. Если они на одной странице, подпись обязана быть НИЖЕ тела (под рисунком).
    if body_page == cap_page:
        c.check("caption_below_body", cap[0][2] > body[0][4],
                f"подпись yMin={cap[0][2]:.1f} не ниже низа тела yMax={body[0][4]:.1f}")
    else:
        c.check("caption_below_body", False,
                "не проверить порядок: подпись на другой странице (см. same_page)")

c.done()
