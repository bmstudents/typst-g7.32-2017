"""h1 ТАБЛИЦЫ #5 — ПРОДОЛЖЕНИЕ НА СТР.2: ЛЕВЫЙ КРАЙ ТЕЛА == «Продолжение».

Длинная таблица (50 строк) разрывается на страницы. На продолжающей
странице сверху печатается «Продолжение таблицы N» (header), а ниже —
перетёкшее тело. По ГОСТ левая граница тела на стр.2 должна совпадать с
левым краем шапки «Продолжение» (общая левая граница таблицы).

Измеримый инвариант: на первой продолжающей странице
  min(x0) ячеек тела ≈ x0(«Продолжение») (±5pt, либо ±5pt с учётом inset).

ОЖИДАЕМЫЙ БАГ: «Продолжение» прижато к полю (x0≈85, через h(-1.25cm)),
а тело центрировано (x0≈274) — расхождение ~190pt. Баг центрирования тела
(styles/figure.typ) проявляется и на странице продолжения.
"""
import helpers as h

c = h.Checks("h1_continuation_left_aligned")
pdf = h.compile("h1_continuation_left_aligned.typ")
ws = h.words(pdf)

pages = h.page_count(pdf)
c.check("multipage", pages >= 2, f"таблица не разорвана: pages={pages}")

prod = [w for w in ws if w[5] == "Продолжение"]
cont_pages = sorted({w[0] for w in prod})
c.check("continuation_header_present", len(cont_pages) >= 1,
        f"шапка «Продолжение» не найдена ни на одной странице")

if cont_pages:
    pg = cont_pages[0]
    prod_x0 = min(w[1] for w in prod if w[0] == pg)

    # Тело на этой странице — повторяющееся слово «Строка».
    body = [w for w in ws if w[0] == pg and w[5] == "Строка"]
    c.check("body_on_continuation", len(body) > 0,
            f"тело таблицы не найдено на стр.{pg}")

    if body:
        body_x0 = min(w[1] for w in body)
        INSET = 10.0
        delta = body_x0 - prod_x0
        aligned = abs(delta) <= 5 or abs((body_x0 - INSET) - prod_x0) <= 5
        c.check(
            "body_left_eq_continuation_left",
            aligned,
            f"стр.{pg}: левый край тела НЕ под «Продолжение»: "
            f"«Продолжение» x0={prod_x0:.2f}, тело min x0={body_x0:.2f} "
            f"(Δтекст={delta:+.2f}, Δграница={body_x0 - INSET - prod_x0:+.2f}); вне ±5pt. "
            f"Тело центрировано на продолжении. Файл: gost732-2017/styles/figure.typ.",
        )
        # Тело не должно уезжать в правую половину полосы.
        c.check(
            "continuation_body_not_centered",
            body_x0 < 200,
            f"стр.{pg}: тело продолжения x0={body_x0:.2f} (>200) — центрировано, "
            f"не у левого поля.",
        )

c.done()
