"""hf2: номер в НИЖНЕМ поле страницы — не за краем листа и не на тексте.

A4 высота = 841.89pt. Нижнее поле 20мм = 56.69pt → полоса набора заканчивается
на y≈785.2. Номер должен стоять в нижнем поле: ниже последней строки тела,
но выше нижнего края листа. Не наезжать на текст, не вылезать за 841.89.
"""
import helpers as h

c = h.Checks("hf2_footer_in_bottom_field")
pdf = h.compile("hf2_footer_in_bottom_field.typ")

PAGE_H = 841.89

for p in (1, 2):
    pws = [w for w in h.words(pdf) if w[0] == p]
    nums = [w for w in pws if w[2] > 700 and w[5].isdigit()]
    c.check(f"p{p}_footer_present", len(nums) >= 1,
            f"стр.{p}: нижний номер не найден")
    if not nums:
        continue
    foot = max(nums, key=lambda t: t[2])

    # Номер ниже середины листа.
    c.check(f"p{p}_in_lower_half",
            foot[2] > PAGE_H / 2,
            f"стр.{p}: y0 номера={foot[2]:.1f}, ждём >420.9")

    # Нижний край номера НЕ вылезает за край листа.
    c.check(f"p{p}_inside_sheet",
            foot[4] < PAGE_H,
            f"стр.{p}: y1 номера={foot[4]:.1f} >= высоты листа {PAGE_H}")

    # Номер не наезжает на тело: между низом самой нижней СТРОКИ ТЕЛА и верхом
    # номера есть зазор. Тело — все слова кроме самого номера.
    body = [w for w in pws if not (w is foot)]
    if body:
        body_bottom = max(w[4] for w in body)
        c.check(f"p{p}_below_body",
                foot[2] >= body_bottom - 1,
                f"стр.{p}: номер (y0={foot[2]:.1f}) налезает на тело (низ тела y1={body_bottom:.1f})")

c.done()
